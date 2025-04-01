from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True