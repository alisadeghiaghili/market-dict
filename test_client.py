"""Deterministic unit tests for MarketDict Python SDK Client."""

import io
import json
import unittest
import urllib.error
from unittest.mock import patch

from marketdict_client import MarketDict, MarketDictError


class _MockResponse:
    def __init__(self, data: dict, status: int = 200):
        self.data_bytes = json.dumps(data).encode("utf-8")
        self.status = status

    def read(self):
        return self.data_bytes

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MarketDictClientTestCase(unittest.TestCase):
    """Test suite for MarketDict SDK client operations and error handling."""

    def setUp(self):
        self.client = MarketDict(base_url="http://testserver:5000")

    def test_init_url_normalization(self):
        c1 = MarketDict("http://localhost:5000")
        self.assertEqual(c1.base_url, "http://localhost:5000/api/v1")
        c2 = MarketDict("http://localhost:5000/api/v1/")
        self.assertEqual(c2.base_url, "http://localhost:5000/api/v1")

    @patch("urllib.request.urlopen")
    def test_health_check(self, mock_urlopen):
        mock_urlopen.return_value = _MockResponse({
            "status": "success",
            "data": {"status": "healthy", "service": "MarketDict API v1"}
        })
        res = self.client.health()
        self.assertEqual(res["status"], "healthy")

    @patch("urllib.request.urlopen")
    def test_search_terms(self, mock_urlopen):
        mock_urlopen.return_value = _MockResponse({
            "status": "success",
            "data": [{"slug": "capm", "term_en": "CAPM"}],
            "total": 1
        })
        res = self.client.search(query="capm")
        self.assertIn("data", res)
        self.assertEqual(len(res["data"]), 1)

    @patch("urllib.request.urlopen")
    def test_get_term(self, mock_urlopen):
        mock_urlopen.return_value = _MockResponse({
            "status": "success",
            "data": {"slug": "sharperatio", "term_en": "Sharpe Ratio"}
        })
        term = self.client.get_term("sharperatio")
        self.assertEqual(term["slug"], "sharperatio")

    @patch("urllib.request.urlopen")
    def test_http_error_handling(self, mock_urlopen):
        err_body = json.dumps({"error": {"message": "Term not found", "details": "No match"}}).encode("utf-8")
        err = urllib.error.HTTPError(
            url="http://testserver/api/v1/terms/missing",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=io.BytesIO(err_body)
        )
        mock_urlopen.side_effect = err

        with self.assertRaises(MarketDictError) as ctx:
            self.client.get_term("missing")
        self.assertEqual(ctx.exception.code, 404)
        self.assertEqual(str(ctx.exception), "Term not found")

    @patch("urllib.request.urlopen")
    def test_url_error_handling(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError(reason="Connection refused")
        with self.assertRaises(MarketDictError) as ctx:
            self.client.health()
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("Connection failed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
