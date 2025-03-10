import json
from functools import lru_cache
from fastapi import HTTPException, status
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

from config import logger, Settings
from models import APISpecification, AppState

class AIService:
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = self.get_llm(settings.openai_api_key)
    
    @staticmethod
    @lru_cache(maxsize=1)
    def get_llm(api_key: str):
        return OpenAI(openai_api_key=api_key)
    
    @staticmethod
    @lru_cache(maxsize=100)
    def generate_response(query: str, api_spec_str: str, api_key: str) -> str:
        try:
            llm = AIService.get_llm(api_key)
            template = "Answer this question about the API: {query} using the following API spec: {api_spec}"
            prompt = PromptTemplate(
                input_variables=["query", "api_spec"],
                template=template
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            return chain.run(query=query, api_spec=api_spec_str)
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating AI response: {str(e)}"
            )


class APISpecService:
    
    @staticmethod
    def load_spec(content: dict[str, object]) -> APISpecification:
        try:
            return APISpecification(**content)
        except ValueError as e:
            logger.error(f"Invalid API specification: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid API specification format: {str(e)}"
            )
    
    @staticmethod
    def query_endpoint(endpoint: str, state: AppState) -> str:
        if not state.api_spec:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API specification is not loaded yet. Please upload a Swagger JSON file."
            )
        
        if endpoint in state.api_spec.paths:
            return json.dumps(state.api_spec.paths[endpoint], indent=2)
        
        for path, details in state.api_spec.paths.items():
            if endpoint in path:
                return json.dumps(details, indent=2)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found in API specification."
        )
