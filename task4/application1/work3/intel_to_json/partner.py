from pydantic import BaseModel, Field

from intel_to_json.kibot_partner import KibotPartner


class Partner(BaseModel):
    name: str = Field(..., description="名字")
    element: str = Field(..., description="元素")
    hobbies: list[str] = Field(..., description="喜好")
    kibot_partner: list[KibotPartner] = Field(..., description="携带的奇波")
