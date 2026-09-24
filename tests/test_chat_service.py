import sys
import unittest
import json
from types import SimpleNamespace
from pathlib import Path
from openai import BadRequestError
from openai._base_client import make_request_options

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services import chatService


class FakeCompletions:
    def __init__(self, responses):
        self._responses = responses
        self.calls = 0

    def create(self, **kwargs):
        response = self._responses[self.calls]
        self.calls += 1
        if kwargs.get("stream"):
            return iter([response])
        return response


class FakeChat:
    def __init__(self, responses):
        self.completions = FakeCompletions(responses)


class FakeClient:
    def __init__(self, responses):
        self.chat = FakeChat(responses)


class TestChatService(unittest.TestCase):
    def test_chat_falls_back_when_provider_rejects_tool_calls(self):
        def create(**kwargs):
            if kwargs.get("tools"):
                request = SimpleNamespace(method="POST", url="https://example.test/v1/chat/completions")
                response = SimpleNamespace(request=request, status_code=400, headers={}, text="tool use failed")
                raise BadRequestError("tool use failed", response=response, body={"error": {"message": "tool use failed"}})
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content="I can answer directly without tools.",
                            tool_calls=[],
                        )
                    )
                ]
            )

        fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))

        original_client = chatService.client
        chatService.client = fake_client
        try:
            result = "".join(chatService.chat("What is 2+2?", "fallback-session"))
        finally:
            chatService.client = original_client

        events = [json.loads(line) for line in result.splitlines()]
        self.assertEqual(events[-1]["content"], "I can answer directly without tools.")

    def test_chat_handles_unknown_tool_name(self):
        response_with_unknown_tool = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=None,
                        tool_calls=[
                            SimpleNamespace(
                                id="call_1",
                                function=SimpleNamespace(
                                    name="add",
                                    arguments="{}",
                                ),
                            )
                        ],
                    )
                )
            ]
        )
        follow_up_response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    delta=SimpleNamespace(content="I can help with that without using a tool."),
                )
            ]
        )

        fake_client = FakeClient([response_with_unknown_tool, follow_up_response])

        original_client = chatService.client
        chatService.client = fake_client
        try:
            result = "".join(chatService.chat("What is 2+2?", "unknown-tool-session"))
        finally:
            chatService.client = original_client

        events = [json.loads(line) for line in result.splitlines()]
        self.assertEqual(events[-1]["content"], "I can help with that without using a tool.")


if __name__ == "__main__":
    unittest.main()
