from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class SchemaModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


class ApiModel(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True
        populate_by_name = True


class RequestModel(ApiModel):
    pass


class ResponseModel(ApiModel):
    pass
