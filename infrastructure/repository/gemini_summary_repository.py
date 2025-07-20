from typing import Type
from application.port.llm_summary_port import LlmSummaryPort
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


class GeminiSummaryRepository(LlmSummaryPort):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY が .env から読み込めませんでした。"
            )

        self._model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", api_key=api_key
        )

    async def request(
        self, input: str, response_type: Type[BaseModel]
    ) -> Type[BaseModel]:
        llm_with_schema = self._model.with_structured_output(response_type)

        prompt = PromptTemplate.from_template(
            "以下の天気予報文を、一般の人が理解しやすい1文に要約してください：\n「{raw}」"
        )
        chain = prompt | llm_with_schema
        resp = await chain.ainvoke({"raw": input})
        return resp
