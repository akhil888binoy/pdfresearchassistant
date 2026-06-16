import os
from fastapi import FastAPI
from src.routers.pdf_router import pdf_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")
app.include_router(pdf_router)
