from fastapi import FastAPI

app = FastAPI(title="Test App")

@app.get("/")
async def root():
    return {"message": "Hello from Vercel!", "status": "working"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Export for Vercel
handler = app 