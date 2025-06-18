import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Import routers with error handling
try:
    from app.routers import todos, images, shopping
    ROUTERS_AVAILABLE = True
except Exception as e:
    print(f"Error importing routers: {e}")
    ROUTERS_AVAILABLE = False

app = FastAPI(title="Summer House Manager")

# Only mount static files if not in serverless environment
if not os.environ.get("VERCEL"):
    try:
        from fastapi.staticfiles import StaticFiles
        # Ensure static directory exists
        os.makedirs("static", exist_ok=True)
        os.makedirs("static/uploads", exist_ok=True)
        # Static files
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")

# Include routers with error handling
if ROUTERS_AVAILABLE:
    try:
        app.include_router(todos.router)
        app.include_router(images.router)
        app.include_router(shopping.router)
    except Exception as e:
        print(f"Error including routers: {e}")

# Health check endpoint for Vercel
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "routers_available": ROUTERS_AVAILABLE,
        "environment": "vercel" if os.environ.get("VERCEL") else "local"
    }

@app.get("/")
async def root():
    return {
        "message": "Summer House Manager API",
        "status": "running",
        "health_endpoint": "/health"
    }

# Error handler
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)