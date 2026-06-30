from pydantic import BaseModel, Field


class Pos(BaseModel):
    x: float = Field(..., description="X坐标")
    y: float = Field(..., description="Y坐标")

class PosList(BaseModel):
    pos: list[Pos] = Field(..., description="坐标列表")