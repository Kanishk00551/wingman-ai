from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

# Load environment variables from the .env file right away
load_dotenv()

# Now your other imports can safely run
from wingman_backend.app.routes import photo, profile, auth, user, history, usage

from wingman_backend.app.routes import photo, profile, auth, user, history, usage

app.include_router(conversation.router)

app = FastAPI(title="Wingman AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(photo.router)
app.include_router(profile.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(history.router)
app.include_router(usage.router)

@app.get("/")
def root():
    return {"status": "Wingman AI backend is running"}