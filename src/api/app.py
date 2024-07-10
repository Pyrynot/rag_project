import os
import uvicorn
from fastapi import FastAPI
from llama_cpp.server.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000))
    )
