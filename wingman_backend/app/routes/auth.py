from fastapi import APIRouter

from app.models.requests import SignupRequest, LoginRequest
from app.config import supabase_client

router = APIRouter()

@router.post("/auth/signup")
async def signup(req: SignupRequest):
    try:
        response = supabase_client.auth.sign_up({
            "email": req.email,
            "password": req.password
        })

        if response.user:
            supabase_client.table("users").insert({
                "id": response.user.id,
                "email": req.email,
                "name": req.name,
            }).execute()

            return {
                "user_id": response.user.id,
                "email": req.email,
                "status": "success",
                "message": "Account created. Check email to verify."
            }

        return {"status": "error", "message": "Signup failed"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/auth/login")
async def login(req: LoginRequest):
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if response.user:
            return {
                "user_id": response.user.id,
                "email": req.email,
                "access_token": response.session.access_token,
                "status": "success"
            }

        return {"status": "error", "message": "Invalid credentials"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/auth/logout")
async def logout():
    try:
        supabase_client.auth.sign_out()
        return {"status": "success", "message": "Logged out"}
    except Exception as e:
        return {"status": "error", "message": str(e)}