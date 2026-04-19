import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

langchain_google_genai = types.ModuleType("langchain_google_genai")
langchain_google_genai.ChatGoogleGenerativeAI = MagicMock()
sys.modules["langchain_google_genai"] = langchain_google_genai

langchain_core = types.ModuleType("langchain_core")
langchain_core_prompts = types.ModuleType("langchain_core.prompts")
langchain_core_prompts.PromptTemplate = MagicMock()
sys.modules["langchain_core"] = langchain_core
sys.modules["langchain_core.prompts"] = langchain_core_prompts

from lambda_function import lambda_handler


@patch("lambda_function._build_daily_notification_orchestrator")
def test_should_return_200_when_daily_notification_orchestrator_succeeds(
    mock_build_daily_notification_orchestrator,
):
    # 1. setup
    daily_notification_orchestrator = MagicMock()
    daily_notification_orchestrator.handle = AsyncMock(return_value=None)
    mock_build_daily_notification_orchestrator.return_value = (
        daily_notification_orchestrator
    )

    # 2. execute
    actual = lambda_handler({}, {})

    # 3. verify
    assert actual == {"status_code": 200, "body": "Success"}
    mock_build_daily_notification_orchestrator.assert_called_once_with()
    daily_notification_orchestrator.handle.assert_awaited_once_with()


@patch("lambda_function._build_daily_notification_orchestrator")
def test_should_return_500_when_daily_notification_orchestrator_raises(
    mock_build_daily_notification_orchestrator,
):
    # 1. setup
    daily_notification_orchestrator = MagicMock()
    daily_notification_orchestrator.handle = AsyncMock(
        side_effect=Exception("Daily notification error")
    )
    mock_build_daily_notification_orchestrator.return_value = (
        daily_notification_orchestrator
    )

    # 2. execute
    result = lambda_handler({}, {})

    # 3. verify
    assert result["status_code"] == 500
