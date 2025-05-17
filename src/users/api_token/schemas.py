from pydantic import UUID4

from src.core_.schemas import ResponseModel, SchemaModel


class ApiTokenSchema(SchemaModel):
    api_token_id: UUID4
    user_id: UUID4
    token: str
    
    
class ApiTokenResponse(ApiTokenSchema, ResponseModel):
    pass


class ApiTokenCreateResponse(ResponseModel):
    token: str