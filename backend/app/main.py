from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import prediction  

app = FastAPI(
    title="P2P Energy Trading with XAI",
    description="An AI + Blockchain based energy trading platform with SHAP explanations",
    version="1.0.0"
)

# CORS configuration (for connecting frontend later)
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",
   # Add deployed frontend URL here in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes here
app.include_router(prediction.router, prefix="/api/predict")

# Health check route (optional)
@app.get("/")
def read_root():
    return {"message": "P2P Energy Trading Backend is running"}
