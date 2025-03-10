from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Depends, status
import json

from config import get_settings
from models import (
    MessageResponse, EndpointResponse, 
    AssistantRequest, AssistantResponse, AppState
)
from services import AIService, APISpecService

app_state = AppState()

def get_app_state():
    return app_state

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

ai_service = AIService(settings)

@app.post(
    "/v1/specifications", 
    response_model=MessageResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Upload API specification",
    description="Upload OpenAPI/Swagger JSON file for AI-based processing"
)
async def upload_specification(
    file: UploadFile = File(...),
    state: AppState = Depends(get_app_state)
):
    try:
        content_bytes = await file.read()
        try:
            content = json.loads(content_bytes)
            state.api_spec = APISpecService.load_spec(content)
            return {"message": "API specification loaded successfully."}
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON file format"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

@app.get(
    "/v1/endpoints/{endpoint_path}", 
    response_model=EndpointResponse,
    summary="Get endpoint details",
    description="Retrieve information about a specific API endpoint"
)
def get_endpoint_details(
    endpoint_path: str,
    state: AppState = Depends(get_app_state)
):
    try:
        endpoint_info = APISpecService.query_endpoint(endpoint_path, state)
        return {"endpoint_info": endpoint_info}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving endpoint details: {str(e)}"
        )

@app.post(
    "/v1/assistant/query", 
    response_model=AssistantResponse,
    summary="Query the AI assistant",
    description="AI-powered Q&A for API documentation"
)
async def query_assistant(
    request: AssistantRequest,
    state: AppState = Depends(get_app_state)
):
    if not state.api_spec:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API specification is not loaded yet. Please upload a Swagger JSON file."
        )
    
    try:
        api_spec_str = json.dumps(state.api_spec.dict(), indent=2)
        
        ai_response = AIService.generate_response(
            request.question, 
            api_spec_str, 
            settings.openai_api_key
        )
        
        return {"ai_response": ai_response}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@app.get(
    "/v1/health", 
    response_model=MessageResponse,
    summary="Health check",
    description="Health check endpoint"
)
def health_check():
    return {"message": "ok!"}
