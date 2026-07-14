import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GeminiQuizGenerator:
    """Generates quiz JSON using the Gemini API."""

    def __init__(
        self,
        model: str = "gemini-3.5-flash",
        base_url: str = (
            "https://generativelanguage.googleapis.com/v1beta"
        ),
        timeout: int = 300,
        max_retries: int = 3,
    ) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set"
            )

        if max_retries < 1:
            raise ValueError(
                "Max retries must be greater than zero"
            )

        self.model = model
        self.url = (
            f"{base_url}/models/{self.model}:generateContent"
        )
        self.timeout = timeout
        self.max_retries = max_retries

    def generate(self, prompt: str) -> str:
        """Send a prompt to Gemini and return generated JSON text. """

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
            },
        }

        request = Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )

        response_data: dict = {}
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                with urlopen(
                    request,
                    timeout=self.timeout,
                ) as response:
                    response_data = json.loads(
                        response.read().decode("utf-8")
                    )

                break

            except HTTPError as error:
                error_body = error.read().decode(
                    "utf-8",
                    errors="replace",
                )

                can_retry = error.code in {429, 503}
                is_last_attempt = attempt == self.max_retries

                if not can_retry or is_last_attempt:
                    raise RuntimeError(
                        f"Gemini API request failed with HTTP "
                        f"{error.code}: {error_body}"
                    ) from error

                last_error = error

            except URLError as error:
                if attempt == self.max_retries:
                    raise RuntimeError(
                        "Cannot connect to the Gemini API"
                    ) from error

                last_error = error

            time.sleep(2 ** (attempt - 1))

        else:
            raise RuntimeError(
                "Gemini API request failed after retries"
            ) from last_error

        candidates = response_data.get("candidates", [])

        if not candidates:
            raise RuntimeError(
                "Gemini returned no response candidates"
            )

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )

        generated_text = "".join(
            str(part.get("text", ""))
            for part in parts
            if isinstance(part, dict)
        ).strip()

        if not generated_text:
            raise RuntimeError(
                "Gemini returned an empty response"
            )

        return generated_text