import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from src.quiz.gemini_generator import GeminiQuizGenerator


class FakeResponse:
    """Simulates a successful HTTP response."""

    def __init__(self, payload: dict) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: object | None,
    ) -> bool:
        return False

    def read(self) -> bytes:
        """Return the simulated response body.  """

        return self.body


class GeminiQuizGeneratorTest(unittest.TestCase):
    """EN: Tests Gemini generator. """

    def test_should_retry_after_503_and_return_response(self) -> None:
        """Retry after HTTP 503 and return the next valid response. """

        generated_json = (
            '{"topic": "Détresse", "questions": []}'
        )

        successful_response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": generated_json,
                            }
                        ]
                    }
                }
            ]
        }

        request_count = 0
        sleep_delays: list[int] = []

        def fake_urlopen(
            request: object,
            timeout: int,
        ) -> FakeResponse:
            """Fail once with 503, then succeed. """

            nonlocal request_count
            request_count += 1

            if request_count == 1:
                raise HTTPError(
                    url="https://example.test",
                    code=503,
                    msg="Service Unavailable",
                    hdrs=None,
                    fp=io.BytesIO(
                        b'{"error": {"code": 503}}'
                    ),
                )

            return FakeResponse(successful_response)

        def fake_sleep(seconds: int) -> None:
            """ Record the delay without waiting."""

            sleep_delays.append(seconds)

        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": "test-api-key"},
        ):
            with patch(
                "src.quiz.gemini_generator.urlopen",
                side_effect=fake_urlopen,
            ):
                with patch(
                    "src.quiz.gemini_generator.time.sleep",
                    side_effect=fake_sleep,
                ):
                    generator = GeminiQuizGenerator(
                        max_retries=3,
                    )

                    result = generator.generate(
                        "Generate one quiz question."
                    )

        self.assertEqual(generated_json, result)
        self.assertEqual(2, request_count)
        self.assertEqual([1], sleep_delays)
