from pydantic import BaseModel, Field

class SampleTab1Model(BaseModel):
    """Data model for Sample Tab 1."""
    username: str = Field(default="test_user", min_length=3, title="Username", description="Your username.")
    firstName: str = Field(default="", title="First Name")
    lastName: str = Field(default="", title="Last Name")
    rememberMe: bool = Field(default=False, title="Remember Me")
    enableNotifications: bool = Field(default=True, title="Enable Notifications")

class SampleTab2Model(BaseModel):
    """Data model for Sample Tab 2."""
    password: str = Field(default="password", min_length=8, title="Password", description="Your password (minimum 8 characters).")
    volume: int = Field(default=50, ge=0, le=100, title="Volume", description="Audio volume (0-100).")
    email: str = Field(default="test@example.com", pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", title="Email", description="Your email address.")
    phoneNumber: str = Field(default="", title="Phone Number", description="Your phone number.")
    address: str = Field(default="", title="Address", description="Your street address.")
    comments: str = Field(default="", title="Comments", description="Any comments you want to leave.")
    selectAnOption: str = Field(default="Option 1", title="Selection Option", description="The selected option.")