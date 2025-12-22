from fastapi import FastAPI

app = FastAPI(title="Aarogyadost API")

@app.get("/")
def read_root():
    return {"message": "Aarogyadost Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
