"""
MarketDict Python SDK Client
Lightweight, zero-dependency client library for MarketDict REST API.
Works with Python standard library (urllib.request) or requests.
"""

import json
import urllib.parse
import urllib.request
from typing import Any


class MarketDictError(Exception):
    """Exception raised when MarketDict API returns an error."""
    def __init__(self, message: str, code: int = 400, details: str | None = None):
        super().__init__(message)
        self.code = code
        self.details = details or message


class MarketDict:
    """
    Official Python Client for the MarketDict Financial Dictionary API.

    Example usage:
        >>> from marketdict_client import MarketDict
        >>> client = MarketDict()
        >>> results = client.search("Sharpe Ratio")
        >>> print(results["data"][0]["term_fa"])
        >>> term = client.get_term("sharperatio")
        >>> print(term["formula"])
    """

    def __init__(self, base_url: str = "http://localhost:5000/api/v1", timeout: float = 10.0):
        # Normalize base URL (strip trailing slash)
        self.base_url = base_url.rstrip("/")
        if not self.base_url.endswith("/api/v1") and "/api/" not in self.base_url:
            self.base_url += "/api/v1"
        self.timeout = timeout

    def _request(self, endpoint: str, method: str = "GET", params: dict[str, Any] | None = None, data: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query_string = urllib.parse.urlencode(filtered_params)
            if query_string:
                url = f"{url}?{query_string}"

        headers = {
            "User-Agent": "MarketDict-Python-SDK/1.0.0",
            "Accept": "application/json"
        }
        body_bytes = None
        if data is not None:
            body_bytes = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp_body = resp.read().decode("utf-8")
                return json.loads(resp_body)
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode("utf-8"))
                err_obj = err_data.get("error", {})
                msg = err_obj.get("message", f"HTTP Error {e.code}")
                details = err_obj.get("details", "")
                raise MarketDictError(msg, code=e.code, details=details) from e
            except json.JSONDecodeError:
                raise MarketDictError(f"HTTP Error {e.code}: {e.reason}", code=e.code) from e
        except urllib.error.URLError as e:
            raise MarketDictError(f"Connection failed to {url}: {e.reason}", code=0) from e

    # ------------------------------------------------------------------
    # System Methods
    # ------------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        """Check API service health and database status."""
        return self._request("health")["data"]

    def stats(self) -> dict[str, Any]:
        """Get dictionary statistics (total terms, categories, letters, formulas)."""
        return self._request("stats")["data"]

    # ------------------------------------------------------------------
    # Terms Methods
    # ------------------------------------------------------------------

    def search(
        self,
        query: str = "",
        letter: str | None = None,
        category: str | None = None,
        has_deep: bool | None = None,
        has_formula: bool | None = None,
        sort: str = "relevance",
        order: str = "asc",
        page: int = 1,
        limit: int = 20,
        fields: str | list[str] | None = None
    ) -> dict[str, Any]:
        """
        Search and filter financial terms.

        Args:
            query: Keyword in English or Persian (e.g. 'Sharpe', 'تورم').
            letter: Letter filter ('A'-'Z' or '#').
            category: Category slug ('crypto') or Persian name ('ارزهای دیجیتال و بلاک‌چین').
            has_deep: Filter comprehensive terms only.
            has_formula: Filter terms with mathematical formulas only.
            sort: 'relevance', 'term_en', 'term_fa', or 'id'.
            order: 'asc' or 'desc'.
            page: Page number (1-based).
            limit: Page size (1-100).
            fields: Comma-separated list or list of field names.

        Returns:
            Dictionary with 'status', 'data' (list of terms), and 'pagination'.
        """
        params: dict[str, Any] = {
            "page": page,
            "limit": limit,
            "sort": sort,
            "order": order
        }
        if query:
            params["q"] = query
        if letter:
            params["letter"] = letter
        if category:
            params["category"] = category
        if has_deep is not None:
            params["has_deep"] = "true" if has_deep else "false"
        if has_formula is not None:
            params["has_formula"] = "true" if has_formula else "false"
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, (list, tuple)) else fields

        return self._request("terms", params=params)

    def get_term(self, identifier: str | int, fields: str | list[str] | None = None) -> dict[str, Any]:
        """
        Retrieve full term details by numeric ID (e.g. 461) or slug (e.g. 'sharperatio').

        Returns:
            Complete term dictionary with definitions, takeaways, sections, and formula.
        """
        params = {}
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, (list, tuple)) else fields
        res = self._request(f"terms/{identifier}", params=params)
        return res["data"]

    def get_random(self, category: str | None = None, has_deep: bool | None = None, count: int = 1) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get random term(s). Great for 'Term of the Day' widgets or study cards.
        """
        params: dict[str, Any] = {"count": count}
        if category:
            params["category"] = category
        if has_deep is not None:
            params["has_deep"] = "true" if has_deep else "false"
        res = self._request("terms/random", params=params)
        return res["data"]

    def get_batch(self, identifiers: list[str | int]) -> dict[str, Any]:
        """
        Retrieve multiple terms in a single HTTP request.
        """
        return self._request("terms/batch", method="POST", data={"identifiers": [str(i) for i in identifiers]})

    def suggest(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """
        Fast autocomplete suggestions for UI search inputs.
        """
        res = self._request("suggest", params={"q": query, "limit": limit})
        return res.get("data", [])

    # ------------------------------------------------------------------
    # Categories Methods
    # ------------------------------------------------------------------

    def get_categories(self) -> list[dict[str, Any]]:
        """List all financial categories with names, icons, and term counts."""
        res = self._request("categories")
        return res.get("data", [])

    def get_category(self, category_id: str) -> dict[str, Any]:
        """Get metadata for a single category."""
        res = self._request(f"categories/{category_id}")
        return res.get("data", {})

    def get_category_terms(self, category_id: str, page: int = 1, limit: int = 20) -> dict[str, Any]:
        """Get paginated terms belonging to a category."""
        return self._request(f"categories/{category_id}/terms", params={"page": page, "limit": limit})

    # ------------------------------------------------------------------
    # Letters Methods
    # ------------------------------------------------------------------

    def get_letters(self) -> list[dict[str, Any]]:
        """List all alphabetical letters with term counts."""
        res = self._request("letters")
        return res.get("data", [])

    def get_letter_terms(self, letter: str, page: int = 1, limit: int = 20) -> dict[str, Any]:
        """Get paginated terms starting with a letter."""
        return self._request(f"letters/{letter}/terms", params={"page": page, "limit": limit})

    # ------------------------------------------------------------------
    # Formulas Methods
    # ------------------------------------------------------------------

    def get_formulas(self) -> list[dict[str, Any]]:
        """
        Get all quantitative financial formulas with LaTeX math equations and Persian definitions.
        """
        res = self._request("formulas")
        return res.get("data", [])
