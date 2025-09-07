from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
import os
from textsummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()

# Redirect root to Swagger UI
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")



# Train endpoint (not recommended for production, but okay for demo)
@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return JSONResponse(content={"message": "Training has been started"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Predict endpoint
@app.get("/predict")
async def predict_route(text: str):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
