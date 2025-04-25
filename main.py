from fastapi import FastAPI

from api import create_api_router

app = FastAPI(title="Student Engagement Chatbot API", 
              description="API for managing student engagement chatbot data",
              version="1.0.0")

# Register all API endpoints
create_api_router(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
