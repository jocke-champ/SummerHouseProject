from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import todos, images, shopping

app = FastAPI(title="Summer House Manager")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(todos.router)
app.include_router(images.router)
app.include_router(shopping.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)