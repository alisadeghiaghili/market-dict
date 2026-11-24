"""
Automated Test Suite for MarketDict REST API v1
"""

import unittest

from app import app


class MarketDictAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

    def test_cors_headers(self):
        """Verify CORS headers are present on API responses."""
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("Access-Control-Allow-Origin"), "*")
        self.assertIn("GET", res.headers.get("Access-Control-Allow-Methods", ""))
        self.assertEqual(res.headers.get("X-API-Version"), "1.0.0")

    def test_health_check(self):
        """Verify health check endpoint."""
        res = self.client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["service"], "MarketDict API")
        self.assertEqual(data["data"]["status"], "healthy")
        self.assertEqual(data["data"]["total_terms"], 6108)

    def test_stats(self):
        """Verify statistics endpoint."""
        res = self.client.get("/api/v1/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["total_terms"], 6108)
        self.assertEqual(data["data"]["total_categories"], 28)
        self.assertEqual(data["data"]["formulas_count"], 44)

    def test_openapi_spec(self):
        """Verify OpenAPI 3.0.3 specification."""
        res = self.client.get("/api/v1/openapi.json")
        self.assertEqual(res.status_code, 200)
        spec = res.get_json()
        self.assertEqual(spec["openapi"], "3.0.3")
        self.assertIn("/terms", spec["paths"])
        self.assertIn("/health", spec["paths"])
        self.assertIn("/formulas", spec["paths"])
        self.assertIn("/suggest", spec["paths"])

    def test_swagger_ui_docs(self):
        """Verify Swagger UI docs page."""
        res = self.client.get("/api/v1/docs")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"SwaggerUIBundle", res.data)
        self.assertIn(b"MarketDict REST API", res.data)

    def test_docs_redirect(self):
        """Verify /docs redirects to /api/v1/docs."""
        res = self.client.get("/docs")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/api/v1/docs", res.headers.get("Location", ""))

    def test_docs_guide_page(self):
        """Verify interactive bilingual guide page."""
        res = self.client.get("/docs/guide")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"MarketDict REST API", res.data)
        self.assertIn(b"lang-fa", res.data)
        self.assertIn(b"lang-en", res.data)

    def test_terms_list_pagination(self):
        """Verify terms listing with pagination."""
        res = self.client.get("/api/v1/terms?page=1&limit=15")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 15)
        self.assertEqual(data["pagination"]["page"], 1)
        self.assertEqual(data["pagination"]["limit"], 15)
        self.assertEqual(data["pagination"]["total"], 6108)
        self.assertTrue(data["pagination"]["has_next"])

    def test_terms_search_english(self):
        """Verify search in English."""
        res = self.client.get("/api/v1/terms?q=Sharpe+Ratio")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        top_term = data["data"][0]
        self.assertIn("Sharpe", top_term["term_en"])

    def test_terms_search_persian(self):
        """Verify search in Persian with text normalization."""
        res = self.client.get("/api/v1/terms?q=%D8%B4%D8%A7%D8%B1%D9%BE")  # شارپ
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)

    def test_terms_filter_category_slug(self):
        """Verify category filtering by slug (e.g. crypto)."""
        res = self.client.get("/api/v1/terms?category=crypto&limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        for term in data["data"]:
            self.assertEqual(term["category_id"], "crypto")

    def test_terms_filter_has_formula(self):
        """Verify filtering by terms with formulas."""
        res = self.client.get("/api/v1/terms?has_formula=true&limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["pagination"]["total"], 0)
        for term in data["data"]:
            self.assertTrue(term["has_formula"])

    def test_terms_field_projection(self):
        """Verify field projection (sparse fieldsets)."""
        res = self.client.get("/api/v1/terms?limit=5&fields=id,slug,term_en,term_fa")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        item = data["data"][0]
        self.assertIn("id", item)
        self.assertIn("slug", item)
        self.assertIn("term_en", item)
        self.assertIn("term_fa", item)
        self.assertNotIn("definition_fa", item)

    def test_term_detail_lookup_by_slug(self):
        """Verify retrieving term detail by slug with formula enrichment."""
        res = self.client.get("/api/v1/terms/sharperatio")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        term = data["data"]
        self.assertEqual(term["slug"], "sharperatio")
        self.assertIsNotNone(term["formula"])
        self.assertIn("Sharpe Ratio", term["formula"]["formula_en"])
        self.assertIn("نسبت شارپ", term["formula"]["formula_fa"])

    def test_term_detail_lookup_by_id(self):
        """Verify retrieving term detail by numeric ID."""
        res = self.client.get("/api/v1/terms/461")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["id"], 461)

    def test_term_not_found(self):
        """Verify 404 error when term does not exist."""
        res = self.client.get("/api/v1/terms/non-existent-random-term-12345")
        self.assertEqual(res.status_code, 404)
        data = res.get_json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["error"]["code"], 404)

    def test_random_term(self):
        """Verify random term retrieval."""
        res = self.client.get("/api/v1/terms/random")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("term_en", data["data"])

    def test_random_terms_count(self):
        """Verify random multiple terms retrieval."""
        res = self.client.get("/api/v1/terms/random?count=3")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 3)

    def test_suggest_autocomplete(self):
        """Verify autocomplete prefix search."""
        res = self.client.get("/api/v1/suggest?q=bit&limit=5")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(len(data["data"]), 0)
        item = data["data"][0]
        self.assertIn("id", item)
        self.assertIn("slug", item)
        self.assertIn("term_en", item)

    def test_categories_endpoints(self):
        """Verify categories list, detail, and category terms."""
        res = self.client.get("/api/v1/categories")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 28)

        # Test single category
        res2 = self.client.get("/api/v1/categories/crypto")
        self.assertEqual(res2.status_code, 200)
        cat_data = res2.get_json()
        self.assertEqual(cat_data["data"]["id"], "crypto")

    def test_letters_endpoints(self):
        """Verify letters list and letter terms."""
        res = self.client.get("/api/v1/letters")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 27)

    def test_formulas_endpoint(self):
        """Verify financial formulas endpoint."""
        res = self.client.get("/api/v1/formulas")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["data"]), 44)
        first_f = data["data"][0]
        self.assertIn("formula_en", first_f)
        self.assertIn("formula_fa", first_f)

    def test_batch_terms_post(self):
        """Verify batch retrieval with POST body."""
        payload = {"identifiers": ["sharperatio", "461", "non-existent-xyz"]}
        res = self.client.post("/api/v1/terms/batch", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["meta"]["requested"], 3)
        self.assertEqual(data["meta"]["found"], 2)
        self.assertIn("non-existent-xyz", data["meta"]["missing"])

    def test_backward_compatibility_existing_routes(self):
        """Verify existing web frontend API endpoints are 100% functional."""
        res = self.client.get("/api/stats")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["total_terms"], 6108)

        res2 = self.client.get("/api/terms?q=stock")
        self.assertEqual(res2.status_code, 200)
        self.assertIn("terms", res2.get_json())

    def test_reverse_proxy_trusted_headers(self):
        """Verify reverse proxy headers (X-Forwarded-For, X-Forwarded-Proto) when client IP is trusted."""
        from app import app, apply_reverse_proxy
        apply_reverse_proxy(app, allowed_ips="127.0.0.1,10.0.0.1")

        # Directly invoke the WSGI app with WSGI environ to test header rewriting
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/api/v1/health",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "5000",
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_X_FORWARDED_FOR": "203.0.113.195",
            "HTTP_X_FORWARDED_PROTO": "https",
            "wsgi.url_scheme": "http",
            "wsgi.input": None
        }
        captured_environ = {}
        def dummy_start_response(status, headers):
            pass

        def inspect_app(env, sr):
            captured_environ.update(env)
            return [b"ok"]

        # Test through reverse_proxy logic
        from werkzeug.middleware.proxy_fix import ProxyFix
        proxy_fix = ProxyFix(inspect_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

        allowed = {"127.0.0.1", "10.0.0.1"}
        def test_wsgi(env, sr):
            if env.get("REMOTE_ADDR", "") in allowed:
                return proxy_fix(env, sr)
            return inspect_app(env, sr)

        test_wsgi(environ, dummy_start_response)
        self.assertEqual(captured_environ.get("REMOTE_ADDR"), "203.0.113.195")
        self.assertEqual(captured_environ.get("wsgi.url_scheme"), "https")

    def test_reverse_proxy_untrusted_headers(self):
        """Verify reverse proxy headers are ignored when connecting client IP is NOT in allowed list."""
        from app import app, apply_reverse_proxy
        apply_reverse_proxy(app, allowed_ips="10.0.0.1")

        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/api/v1/health",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "5000",
            "REMOTE_ADDR": "192.168.1.50",
            "HTTP_X_FORWARDED_FOR": "203.0.113.195",
            "HTTP_X_FORWARDED_PROTO": "https",
            "wsgi.url_scheme": "http",
            "wsgi.input": None
        }
        captured_environ = {}
        def dummy_start_response(status, headers):
            pass

        def inspect_app(env, sr):
            captured_environ.update(env)
            return [b"ok"]

        from werkzeug.middleware.proxy_fix import ProxyFix
        proxy_fix = ProxyFix(inspect_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

        allowed = {"10.0.0.1"}
        def test_wsgi(env, sr):
            if env.get("REMOTE_ADDR", "") in allowed:
                return proxy_fix(env, sr)
            return inspect_app(env, sr)

        test_wsgi(environ, dummy_start_response)
        # Remote addr should remain untrusted direct IP, not the spoofed X-Forwarded-For
        self.assertEqual(captured_environ.get("REMOTE_ADDR"), "192.168.1.50")
        self.assertEqual(captured_environ.get("wsgi.url_scheme"), "http")

    def test_reverse_proxy_wildcard_allow(self):
        """Verify reverse proxy headers work from any IP when allowed_ips='*'."""
        from app import app, apply_reverse_proxy
        apply_reverse_proxy(app, allowed_ips="*")

        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/api/v1/health",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "5000",
            "REMOTE_ADDR": "172.16.0.5",
            "HTTP_X_FORWARDED_FOR": "198.51.100.22",
            "HTTP_X_FORWARDED_PROTO": "https",
            "wsgi.url_scheme": "http",
            "wsgi.input": None
        }
        captured_environ = {}
        def dummy_start_response(status, headers):
            pass

        def inspect_app(env, sr):
            captured_environ.update(env)
            return [b"ok"]

        from werkzeug.middleware.proxy_fix import ProxyFix
        proxy_fix = ProxyFix(inspect_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

        # Wildcard means allowed is None
        allowed = None
        def test_wsgi(env, sr):
            if allowed is None or env.get("REMOTE_ADDR", "") in allowed:
                return proxy_fix(env, sr)
            return inspect_app(env, sr)

        test_wsgi(environ, dummy_start_response)
        self.assertEqual(captured_environ.get("REMOTE_ADDR"), "198.51.100.22")
        self.assertEqual(captured_environ.get("wsgi.url_scheme"), "https")

    def test_tts_missing_text(self):
        """Verify TTS endpoint returns 400 when text parameter is omitted."""
        res = self.client.get("/api/tts")
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("error", data)

    def test_tts_generate_audio_and_cache(self):
        """Verify TTS endpoint generates and caches audio/mpeg stream."""
        from unittest.mock import patch

        dummy_audio = b"\xff\xfb\x90\x00dummy_audio_bytes"

        def mock_run(coro):
            coro.close()
            return dummy_audio

        with patch("asyncio.run", side_effect=mock_run):
            res = self.client.get("/api/tts?text=تست&lang=fa")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.mimetype, "audio/mpeg")
            self.assertEqual(res.data, dummy_audio)

        # Test caching directly from memory cache
        res_cached = self.client.get("/api/tts?text=تست&lang=fa")
        self.assertEqual(res_cached.status_code, 200)
        self.assertEqual(res_cached.data, dummy_audio)

    def test_tts_english_generation(self):
        """Verify TTS endpoint generates English audio."""
        from unittest.mock import patch

        dummy_audio = b"\xff\xfb\x90\x00english_audio_bytes"

        def mock_run(coro):
            coro.close()
            return dummy_audio

        with patch("asyncio.run", side_effect=mock_run):
            res = self.client.get("/api/tts?text=Hello&lang=en")
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.mimetype, "audio/mpeg")
            self.assertEqual(res.data, dummy_audio)

    def test_tts_cache_eviction(self):
        """Verify cache eviction when exceeding 1000 entries."""
        from unittest.mock import patch

        from app import _TTS_CACHE, _TTS_LOCK

        with _TTS_LOCK:
            _TTS_CACHE.clear()
            for i in range(1001):
                _TTS_CACHE[f"dummy:{i}"] = b"dummy"

        dummy_audio = b"\xff\xfb\x90\x00eviction_audio"

        def mock_run(coro):
            coro.close()
            return dummy_audio

        with patch("asyncio.run", side_effect=mock_run):
            res = self.client.get("/api/tts?text=eviction_test&lang=en")
            self.assertEqual(res.status_code, 200)

    def test_tts_empty_audio_failure(self):
        """Verify 500 when audio generation yields empty bytes."""
        from unittest.mock import patch

        def mock_run(coro):
            coro.close()
            return b""

        with patch("asyncio.run", side_effect=mock_run):
            res = self.client.get("/api/tts?text=empty_fail_123&lang=fa")
            self.assertEqual(res.status_code, 500)
            data = res.get_json()
            self.assertEqual(data.get("error"), "Failed to synthesize speech")

    def test_tts_exception_handling(self):
        """Verify 500 and error message when TTS raises an unexpected exception."""
        from unittest.mock import patch

        def mock_run(coro):
            coro.close()
            raise RuntimeError("EdgeTTS network timeout")

        with patch("asyncio.run", side_effect=mock_run):
            res = self.client.get("/api/tts?text=error_test_456&lang=fa")
            self.assertEqual(res.status_code, 500)
            data = res.get_json()
            self.assertIn("EdgeTTS network timeout", data.get("error", ""))

    def test_normalize_application_root(self):
        """Verify normalization of various root path string formats."""
        from app import normalize_application_root

        self.assertEqual(normalize_application_root(""), "")
        self.assertEqual(normalize_application_root(None), "")
        self.assertEqual(normalize_application_root("/"), "")
        self.assertEqual(normalize_application_root("   /   "), "")
        self.assertEqual(normalize_application_root("myapp"), "/myapp")
        self.assertEqual(normalize_application_root("/myapp"), "/myapp")
        self.assertEqual(normalize_application_root("/myapp/"), "/myapp")
        self.assertEqual(normalize_application_root("  /dict/v1/  "), "/dict/v1")
        self.assertEqual(normalize_application_root("dict/v1"), "/dict/v1")

    def test_apply_application_root_subpath_routing(self):
        """Verify mounting application under a custom subpath (e.g. /myapp)."""
        from app import apply_application_root

        try:
            apply_application_root(app, "/myapp")
            self.assertEqual(app.config["APPLICATION_ROOT_PREFIX"], "/myapp")

            # 1. Index page under subpath
            res = self.client.get("/myapp/")
            self.assertEqual(res.status_code, 200)

            # 2. REST API v1 health under subpath
            res_health = self.client.get("/myapp/api/v1/health")
            self.assertEqual(res_health.status_code, 200)
            self.assertEqual(res_health.get_json()["status"], "success")

            # 3. Web frontend stats API under subpath
            res_stats = self.client.get("/myapp/api/stats")
            self.assertEqual(res_stats.status_code, 200)
            self.assertEqual(res_stats.get_json()["total_terms"], 6108)

            # 4. OpenAPI JSON specification under subpath
            res_spec = self.client.get("/myapp/api/v1/openapi.json")
            self.assertEqual(res_spec.status_code, 200)
            spec_data = res_spec.get_json()
            server_urls = [s["url"] for s in spec_data.get("servers", [])]
            self.assertTrue(any("/myapp/api/v1" in u for u in server_urls))

            # 5. Swagger UI docs under subpath
            res_swagger = self.client.get("/myapp/api/v1/docs")
            self.assertEqual(res_swagger.status_code, 200)
            self.assertIn(b"/myapp/api/v1/openapi.json", res_swagger.data)

            # 6. /docs redirect under subpath
            res_docs = self.client.get("/myapp/docs")
            self.assertEqual(res_docs.status_code, 302)
            self.assertIn("/myapp/api/v1/docs", res_docs.headers.get("Location", ""))

            # 7. Categories terms_url contains subpath
            res_cats = self.client.get("/myapp/api/v1/categories")
            self.assertEqual(res_cats.status_code, 200)
            cat_list = res_cats.get_json()["data"]
            self.assertTrue(cat_list[0]["terms_url"].startswith("/myapp/api/v1/categories/"))

            # 8. Letters terms_url contains subpath
            res_ltrs = self.client.get("/myapp/api/v1/letters")
            self.assertEqual(res_ltrs.status_code, 200)
            ltr_list = res_ltrs.get_json()["data"]
            self.assertTrue(ltr_list[0]["terms_url"].startswith("/myapp/api/v1/letters/"))

        finally:
            # Reset application root back to default
            apply_application_root(app, "")

    def test_application_root_redirects_and_fallbacks(self):
        """Verify redirect from /myapp -> /myapp/, / -> /myapp/, and 404 for unmapped paths."""
        from app import apply_application_root

        try:
            apply_application_root(app, "myapp")

            # 1. Exact mount point without trailing slash -> 308 redirect to /myapp/
            res_prefix = self.client.get("/myapp")
            self.assertEqual(res_prefix.status_code, 308)
            self.assertTrue(res_prefix.headers.get("Location", "").endswith("/myapp/"))

            # 2. Exact mount point with query string -> 308 redirect preserving query
            res_prefix_query = self.client.get("/myapp?q=inflation")
            self.assertEqual(res_prefix_query.status_code, 308)
            self.assertTrue(res_prefix_query.headers.get("Location", "").endswith("/myapp/?q=inflation"))

            # 3. Domain root / -> 302 redirect to /myapp/
            res_root = self.client.get("/")
            self.assertEqual(res_root.status_code, 302)
            self.assertEqual(res_root.headers.get("Location"), "/myapp/")

            # 4. Domain root with query -> 302 redirect preserving query
            res_root_query = self.client.get("/?ref=portal")
            self.assertEqual(res_root_query.status_code, 302)
            self.assertEqual(res_root_query.headers.get("Location"), "/myapp/?ref=portal")

            # 5. Unmapped path -> 404
            res_unmapped = self.client.get("/unmapped_page")
            self.assertEqual(res_unmapped.status_code, 404)

        finally:
            apply_application_root(app, "")

    def test_application_root_with_reverse_proxy(self):
        """Verify combined usage of application root and reverse proxy header handling."""
        from app import apply_application_root, apply_reverse_proxy

        try:
            apply_application_root(app, "/myapp")
            apply_reverse_proxy(app, allowed_ips="*")

            res = self.client.get(
                "/myapp/api/v1/health",
                headers={
                    "X-Forwarded-For": "198.51.100.77",
                    "X-Forwarded-Proto": "https"
                }
            )
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json()["status"], "success")

            # Test passing IP list and untrusted client fallback
            apply_reverse_proxy(app, allowed_ips=["10.0.0.1"])
            res_untrusted = self.client.get(
                "/myapp/api/v1/health",
                headers={"X-Forwarded-For": "203.0.113.1"}
            )
            self.assertEqual(res_untrusted.status_code, 200)

            # Test disabling reverse proxy
            apply_reverse_proxy(app, False)
            self.assertFalse(app.config.get("REVERSE_PROXY_ENABLED"))

        finally:
            apply_application_root(app, "")
            apply_reverse_proxy(app, "*")

    def test_rebuild_pipeline_fresh_app_and_openapi_server_url(self):
        """Verify pipeline rebuild on fresh Flask instance and OpenAPI server_url branch."""
        from flask import Flask

        from app import apply_application_root
        from openapi_spec import get_openapi_spec

        fresh_app = Flask("fresh_test_app")
        apply_application_root(fresh_app, "/test_fresh")
        self.assertTrue(hasattr(fresh_app, "_original_wsgi_app"))

        spec = get_openapi_spec(server_url="https://api.test.com/api/v1")
        server_urls = [s["url"] for s in spec["servers"]]
        self.assertIn("https://api.test.com/api/v1", server_urls)

if __name__ == "__main__":
    unittest.main()
