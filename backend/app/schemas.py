from pydantic import BaseModel
from pydantic import HttpUrl


class URLRequest(BaseModel):

    url: HttpUrl

    custom_alias: str | None = None

    expiry_days: int | None = None