from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    available: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "price": 10.99,
                "available": True,
            }
        }
    )
