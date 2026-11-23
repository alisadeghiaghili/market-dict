"""Offline tests for :mod:`polite_fetcher`."""

import io
import unittest
import urllib.error
import urllib.robotparser

from polite_fetcher import AccessDeniedError, FetcherConfig, PoliteFetcher


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


def _robots(text):
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(text.splitlines())
    return parser


class _FakeClock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def clock(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class PoliteFetcherTestCase(unittest.TestCase):
    def setUp(self):
        self.time = _FakeClock()
        self.requests = []

    def _fetcher(self, responses, robots="User-agent: *\nAllow: /\n", **config):
        queue = list(responses)

        def opener(request, timeout):
            self.requests.append(request)
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return _Response(item.encode("utf-8"))

        return PoliteFetcher(
            FetcherConfig(**config),
            opener=opener,
            robots_loader=lambda origin: _robots(robots),
            clock=self.time.clock,
            sleep=self.time.sleep,
        )

    @staticmethod
    def _http_error(code):
        return urllib.error.HTTPError("https://example.com/x", code, "err", {}, None)

    def test_sends_honest_user_agent_only(self):
        fetcher = self._fetcher(["ok"])
        self.assertEqual(fetcher.get("https://example.com/a"), "ok")
        headers = {k.lower(): v for k, v in self.requests[0].header_items()}
        self.assertTrue(headers["user-agent"].startswith("MarketDict-Enrichment/"))
        self.assertNotIn("referer", headers)
        self.assertFalse(any(k.startswith("sec-") for k in headers))

    def test_user_agent_cannot_be_overridden_by_extra_headers(self):
        fetcher = self._fetcher(["ok"], extra_headers={"User-Agent": "Mozilla/5.0"})
        fetcher.get("https://example.com/a")
        self.assertNotIn("Mozilla", self.requests[0].get_header("User-agent"))

    def test_robots_disallow_raises_without_request(self):
        fetcher = self._fetcher([], robots="User-agent: *\nDisallow: /terms/\n")
        with self.assertRaises(AccessDeniedError):
            fetcher.get("https://example.com/terms/x.asp")
        self.assertEqual(self.requests, [])

    def test_forbidden_stops_host_for_rest_of_run(self):
        fetcher = self._fetcher([self._http_error(403)])
        with self.assertRaises(AccessDeniedError):
            fetcher.get("https://example.com/a")
        with self.assertRaises(AccessDeniedError):
            fetcher.get("https://example.com/b")
        self.assertEqual(len(self.requests), 1)

    def test_retries_transient_errors_then_succeeds(self):
        fetcher = self._fetcher([self._http_error(503), "ok"], min_delay_seconds=1.0)
        self.assertEqual(fetcher.get("https://example.com/a"), "ok")
        self.assertEqual(len(self.requests), 2)

    def test_not_found_returns_none_without_retry(self):
        fetcher = self._fetcher([self._http_error(404)])
        self.assertIsNone(fetcher.get("https://example.com/a"))
        self.assertEqual(len(self.requests), 1)

    def test_enforces_min_delay_between_requests(self):
        fetcher = self._fetcher(["a", "b"], min_delay_seconds=4.0)
        fetcher.get("https://example.com/a")
        fetcher.get("https://example.com/b")
        self.assertEqual(self.time.sleeps, [4.0])

    def test_crawl_delay_overrides_smaller_min_delay(self):
        fetcher = self._fetcher(
            ["a", "b"], robots="User-agent: *\nCrawl-delay: 10\n", min_delay_seconds=1.0
        )
        fetcher.get("https://example.com/a")
        fetcher.get("https://example.com/b")
        self.assertEqual(self.time.sleeps, [10.0])

    def test_rejects_non_http_urls(self):
        with self.assertRaises(ValueError):
            self._fetcher([]).get("file:///etc/passwd")


if __name__ == "__main__":
    unittest.main()
