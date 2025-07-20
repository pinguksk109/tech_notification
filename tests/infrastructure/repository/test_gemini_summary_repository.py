import os
import pytest
from infrastructure.repository.gemini_summary_repository import (
    GeminiSummaryRepository,
)
from pydantic import BaseModel


class DummyResponse(BaseModel):
    summary: str


@pytest.mark.skip
@pytest.mark.asyncio
async def test_return_response():
    # 1. setup
    os.environ.setdefault("GEMINI_API_KEY", "hoge")
    repo = GeminiSummaryRepository()

    # 2. execute
    response = await repo.request("晴れ 時々 くもり", DummyResponse)

    # 3. verify
    print(response)
