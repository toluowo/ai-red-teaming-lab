import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from ai_redteam.core.models import AssessmentRequest
from ai_redteam.targets import HTTPJSONTarget, OpenAICompatibleTarget


class _Handler(BaseHTTPRequestHandler):
    mode = "generic"

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8"))

        if self.mode == "openai":
            response = {
                "model": "integration-test-model",
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "I can't comply with that request."
                    }
                }],
                "usage": {"total_tokens": 7},
            }
        else:
            response = {"answer": f"received: {body.get('prompt', '')}"}

        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        pass


class TestTargetAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_http_json_adapter(self):
        target = HTTPJSONTarget(
            url=self.base,
            input_field="prompt",
            output_field="answer",
        )
        result = target.invoke(AssessmentRequest("IT-001", "hello"))
        self.assertIn("hello", result.output)
        self.assertEqual(result.metadata["adapter"], "http-json")

    def test_openai_compatible_adapter(self):
        _Handler.mode = "openai"
        target = OpenAICompatibleTarget(
            base_url=self.base,
            model="integration-test-model",
        )
        result = target.invoke(AssessmentRequest("IT-002", "test"))
        self.assertEqual(result.output, "I can't comply with that request.")
        self.assertEqual(result.metadata["adapter"], "openai-compatible")
        self.assertEqual(result.metadata["model"], "integration-test-model")
        _Handler.mode = "generic"

    def test_adapter_errors_are_structured(self):
        target = HTTPJSONTarget(url="http://127.0.0.1:1/unreachable", timeout=1)
        result = target.invoke(AssessmentRequest("IT-003", "hello"))
        self.assertEqual(result.output, "")
        self.assertIn("error", result.metadata)


if __name__ == "__main__":
    unittest.main()
