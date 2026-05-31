from __future__ import annotations

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import ROOT_DIR
from app.model_registry import ModelRegistryError, model_status
from app.services.inference import predict_image


app = FastAPI(title="KGO Fill Detection API", version="1.0.0")
app.mount("/static", StaticFiles(directory=ROOT_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=str(ROOT_DIR / "app" / "templates"))


@app.get("/health")
async def health():
    return {"status": "ok", "models": model_status()}


@app.get("/api/models")
async def models():
    return {"models": model_status()}


@app.post("/api/predict")
async def predict_api(image: UploadFile = File(...)):
    try:
        return predict_image(await image.read())
    except (ModelRegistryError, FileNotFoundError, ValueError, RuntimeError, ImportError) as exc:
        return JSONResponse(status_code=400, content={"error": str(exc), "models": model_status()})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"result": None, "error": None, "models": model_status()})


@app.post("/", response_class=HTMLResponse)
async def run_ui(request: Request, image: UploadFile = File(...)):
    try:
        result = predict_image(await image.read())
        return templates.TemplateResponse(
            request,
            "index.html",
            {"result": result, "error": None, "models": model_status()},
        )
    except (ModelRegistryError, FileNotFoundError, ValueError, RuntimeError, ImportError) as exc:
        return templates.TemplateResponse(
            request,
            "index.html",
            {"result": None, "error": str(exc), "models": model_status()},
            status_code=400,
        )
