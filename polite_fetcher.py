# -*- coding: utf-8 -*-
"""
Transparent, rate-limited HTTP fetcher for the enrichment pipeline.

Every network call made by the scraping and enrichment scripts goes through
:class:`PoliteFetcher`. The fetcher deliberately does **not** try to look like
a browser: it sends an honest ``User-Agent`` that identifies the tool, honours
``robots.txt`` (including ``Crawl-delay``), enforces a minimum delay between
requests to the same host, and treats ``401``/``403`` as a final answer rather
than something to work around. If a site refuses automated access, the
pipeline stops for that site.

Use of fetched content is governed by the source site's terms of service; see
``DATA_NOTICE.md``.
"""

from __future__ import annotations

import logging
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

__all__ = [
    "AccessDeniedError",
    "DEFAULT_USER_AGENT",
    "FetcherConfig",
    "PoliteFetcher",
]

DEFAULT_USER_AGENT = (
    "MarketDict-Enrichment/1.0 "
    "(+https://github.com/alisadeghiaghili/market-dict; non-commercial research crawler)"
)

_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
_DENIED_STATUS = frozenset({401, 403})

logger = logging.getLogger(__name__)


class AccessDeniedError(RuntimeError):
    """Raised when a host refuses automated access (robots.txt, 401 or 403).

    The pipeline must stop fetching from that host instead of retrying with a
    different client fingerprint.
    """


@dataclass(frozen=True)
class FetcherConfig:
    """Configuration for :class:`PoliteFetcher`.

    Args:
        user_agent: Value sent in the ``User-Agent`` header. Must identify the
            tool honestly.
        min_delay_seconds: Minimum time between two requests to the same host.
            A larger ``Crawl-delay`` from ``robots.txt`` takes precedence.
        timeout_seconds: Socket timeout per request.
        max_retries: Retries for transient errors (429 and 5xx, network errors).
        backoff_factor: Multiplier applied to the wait time after each retry.
        respect_robots_txt: Whether to check ``robots.txt`` before each request.
            Only disable this for hosts you operate yourself.
        extra_headers: Additional headers. ``User-Agent`` here is ignored.

    Examples:
        >>> FetcherConfig(min_delay_seconds=5.0).min_delay_seconds
        5.0
    """

    user_agent: str = DEFAULT_USER_AGENT
    min_delay_seconds: float = 3.0
    timeout_seconds: float = 20.0
    max_retries: int = 2
    backoff_factor: float = 2.0
    respect_robots_txt: bool = True
    extra_headers: Dict[str, str] = field(default_factory=dict)


class PoliteFetcher:
    """Thread-safe fetcher that rate-limits per host and honours robots.txt.

    Args:
        config: Fetcher settings. Defaults to :class:`FetcherConfig`.
        opener: Callable with the signature of :func:`urllib.request.urlopen`.
            Injected for testing.
        robots_loader: Callable returning a ready ``RobotFileParser`` (or
            ``None`` when robots.txt cannot be read) for a ``scheme://host``
            origin. Injected for testing.
        clock: Monotonic clock. Injected for testing.
        sleep: Sleep function. Injected for testing.

    Examples:
        >>> fetcher = PoliteFetcher(FetcherConfig(min_delay_seconds=5.0))
        >>> html = fetcher.get("https://example.com/")  # doctest: +SKIP
    """

    def __init__(
        self,
        config: Optional[FetcherConfig] = None,
        *,
        opener: Callable[..., object] = urllib.request.urlopen,
        robots_loader: Optional[Callable[[str], Optional[urllib.robotparser.RobotFileParser]]] = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._config = config or FetcherConfig()
        self._opener = opener
        self._robots_loader = robots_loader or self._load_robots
        self._clock = clock
        self._sleep = sleep
        self._lock = threading.Lock()
        self._robots: Dict[str, Optional[urllib.robotparser.RobotFileParser]] = {}
        self._next_allowed_at: Dict[str, float] = {}
        self._denied_hosts: set = set()

    @property
    def config(self) -> FetcherConfig:
        """Return the active configuration."""
        return self._config

    def get(self, url: str) -> Optional[str]:
        """Fetch ``url`` and return the decoded body, or ``None`` on failure.

        Args:
            url: Absolute ``http`` or ``https`` URL.

        Returns:
            The response body decoded as UTF-8 for a ``200`` response, ``None``
            for other non-denied failures (404, exhausted retries).

        Raises:
            AccessDeniedError: If ``robots.txt`` disallows the URL, or the host
                answered ``401``/``403`` now or earlier in this run.
            ValueError: If ``url`` is not an absolute http(s) URL.

        Examples:
            >>> PoliteFetcher().get("ftp://example.com")
            Traceback (most recent call last):
            ...
            ValueError: Only absolute http(s) URLs are supported: 'ftp://example.com'
        """
        origin = self._origin(url)
        if origin in self._denied_hosts:
            raise AccessDeniedError(f"{origin} refused automated access earlier in this run")

        crawl_delay = self._check_robots(origin, url)
        delay = max(self._config.min_delay_seconds, crawl_delay or 0.0)

        headers = {**self._config.extra_headers, "User-Agent": self._config.user_agent}
        wait = self._config.min_delay_seconds
        for attempt in range(self._config.max_retries + 1):
            self._throttle(origin, delay)
            request = urllib.request.Request(url, headers=headers)
            try:
                with self._opener(request, timeout=self._config.timeout_seconds) as response:
                    return response.read().decode("utf-8", errors="replace")
            except urllib.error.HTTPError as exc:
                if exc.code in _DENIED_STATUS:
                    self._denied_hosts.add(origin)
                    raise AccessDeniedError(
                        f"{origin} answered HTTP {exc.code} for {url}; not retrying"
                    ) from exc
                if exc.code not in _RETRYABLE_STATUS:
                    logger.warning("HTTP %s for %s; skipping", exc.code, url)
                    return None
                logger.warning("HTTP %s for %s (attempt %d)", exc.code, url, attempt + 1)
            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
                logger.warning("Network error for %s (attempt %d): %s", url, attempt + 1, exc)
            if attempt < self._config.max_retries:
                self._sleep(wait)
                wait *= self._config.backoff_factor
        return None

    @staticmethod
    def _origin(url: str) -> str:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            raise ValueError(f"Only absolute http(s) URLs are supported: {url!r}")
        return f"{parts.scheme}://{parts.netloc.lower()}"

    def _check_robots(self, origin: str, url: str) -> Optional[float]:
        if not self._config.respect_robots_txt:
            return None
        with self._lock:
            if origin not in self._robots:
                self._robots[origin] = self._robots_loader(origin)
            parser = self._robots[origin]
        if parser is None:
            return None
        if not parser.can_fetch(self._config.user_agent, url):
            raise AccessDeniedError(f"robots.txt at {origin} disallows {url}")
        delay = parser.crawl_delay(self._config.user_agent)
        return float(delay) if delay is not None else None

    def _load_robots(self, origin: str) -> Optional[urllib.robotparser.RobotFileParser]:
        parser = urllib.robotparser.RobotFileParser(f"{origin}/robots.txt")
        request = urllib.request.Request(
            f"{origin}/robots.txt", headers={"User-Agent": self._config.user_agent}
        )
        try:
            with self._opener(request, timeout=self._config.timeout_seconds) as response:
                parser.parse(response.read().decode("utf-8", errors="replace").splitlines())
        except urllib.error.HTTPError as exc:
            if exc.code in _DENIED_STATUS:
                parser.disallow_all = True
            elif 400 <= exc.code < 500:
                parser.allow_all = True
            else:
                parser.disallow_all = True
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            logger.warning("Could not read %s/robots.txt; treating host as disallowed", origin)
            parser.disallow_all = True
        return parser

    def _throttle(self, origin: str, delay: float) -> None:
        with self._lock:
            now = self._clock()
            start = max(now, self._next_allowed_at.get(origin, now))
            self._next_allowed_at[origin] = start + delay
        if start > now:
            self._sleep(start - now)
