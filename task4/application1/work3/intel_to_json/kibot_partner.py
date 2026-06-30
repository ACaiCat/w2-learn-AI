from pydantic import BaseModel, Field


class KibotPartner(BaseModel):
    species: str = Field(..., description="种类")
    color: str = Field(..., description="颜色")
    bond_level: int = Field(..., description="羁绊等级")
    coordinates: list[float] = Field(..., description="坐标")
    is_friendly: bool = Field(..., description="是否友好")
