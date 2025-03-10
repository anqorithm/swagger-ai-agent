from pydantic import BaseModel, Field, field_validator

class OpenAPIPath(BaseModel):
    path: str
    methods: list[str]
    summary: str | None = None
    description: str | None = None

class APISpecification(BaseModel):
    title: str | None = None
    version: str | None = None
    paths: dict[str, dict[str, object]] = {}
    
    @field_validator('paths')
    @classmethod
    def validate_paths(cls, v):
        if not v:
            raise ValueError("API specification must contain at least one path")
        return v

class MessageResponse(BaseModel):
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful"
            }
        }

class EndpointResponse(BaseModel):
    endpoint_info: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "endpoint_info": "{'get': {'summary': 'Get user', 'parameters': [...]}}"
            }
        }

class AssistantRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, 
                         description="Question about the API")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What endpoints are available for user management?"
            }
        }

class AssistantResponse(BaseModel):
    ai_response: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "ai_response": "The API has GET /users and POST /users endpoints for user management."
            }
        }

class AppState:
    def __init__(self):
        self.api_spec: APISpecification | None = None
