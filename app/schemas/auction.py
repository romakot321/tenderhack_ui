from pydantic import BaseModel


class AuctionSchema(BaseModel):
    url: str
    status: bool | None = None
    warning: bool | None = None
    reason: str | None = None
