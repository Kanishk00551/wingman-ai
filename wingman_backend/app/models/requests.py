from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class OnboardingRequest(BaseModel):
    user_id: str
    city: str = "Mumbai"
    style: str = "witty"
    personality: str = "balanced"
    dating_goal: str = "serious"
    target_app: str = "Hinge"

class ConversationRequest(BaseModel):
    user_id: str = ""
    conversation: str
    match_name: str = ""
    user_city: str = "Mumbai"
    user_style: str = "witty"