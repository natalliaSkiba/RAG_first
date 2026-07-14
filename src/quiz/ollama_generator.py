import json
from urllib.error import URLError
from urllib.request import Request, urlopen


class OllamaQuizGenerator:
    """Generates quiz JSON using a local Ollama model."""

    def __init__(
        self,
        model: str = "qwen2.5:3b",
        url: str = "http://localhost:11434/api/generate",
        timeout: int = 300,
    ) -> None:
        self.model = model
        self.url = url
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        """Send a prompt to Ollama and return the generated JSON text."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
            },
        }

        request = Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_data = json.loads(
                    response.read().decode("utf-8")
                )
        except URLError as error:
            raise RuntimeError(
                "Cannot connect to Ollama. Check that Ollama is running."
            ) from error

        generated_text = str(
            response_data.get("response", "")
        ).strip()

        if not generated_text:
            raise RuntimeError("Ollama returned an empty response")

        return generated_text