from pydantic import BaseModel, Field

class SettingsModel(BaseModel):
    """Settings model."""

    port: int = Field(default=8080, gt=0, lt=65536, title="Port Number", description="The port to listen on.", examples=["12345"])
