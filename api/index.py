import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
    
    # For Vercel, we need to export the app directly
    def handler(request):
        return app
    
    # Also export as app for Vercel
    app = app
    
except Exception as e:
    print(f"Error importing app: {e}")
    # Create a minimal error app
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error_root():
        return {"error": f"Failed to import main app: {str(e)}"}
    
    @app.get("/health")
    async def health():
        return {"status": "error", "message": str(e)} 