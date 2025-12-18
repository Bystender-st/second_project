from pydantic import BaseModel, Field, ConfigDict


class PackageTypeResponse(BaseModel):
    id: int = Field(..., description="ID типа посылки")
    name: str = Field(..., description="Название типа посылки")

    model_config = ConfigDict(from_attributes=True)
