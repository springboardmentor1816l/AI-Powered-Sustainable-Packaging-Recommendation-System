from fastapi import FastAPI
from .routers import materials   # <--- IMPORTANT

app = FastAPI(title="EcoPack API")

@app.get("/")
def home():
    return {"message": "EcoPack API is running 🚀"}

# Register router
app.include_router(materials.router)
