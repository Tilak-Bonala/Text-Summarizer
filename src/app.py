from fastapi import FastAPI
import uvicorn 
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.responses import Response
from textsummarizer.pipeline.prediction_pipeline import PredictionPipeline

text:str ="What is Text Summarization?"

app = FastAPI()
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training ():
    try:
        os.system("python main.py")
        return Responce(content="Training has been started")
    except Exception as e:
        return Responce(content=f"Error Occured! {e}")


@app.get("/predict")
async def predict_route(text:str=text):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return Response(content=summary)
    except Exception as e:
        raise Response(content=f"Error Occured! {e}")
    
if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)

