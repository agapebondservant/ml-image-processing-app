from fastapi import FastAPI, UploadFile, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from app.analytics import cifar_cnn, mri_cnn, config
import logging
from PIL import Image
import io
import json

api_app = FastAPI()

# Enable CORS
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_app.post('/inference')
async def predict(file: UploadFile) -> str:
    logging.info("In inference...")
    model_name, model_stage = config.model_name, config.model_stage
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    return cifar_cnn.predict(img, model_name, model_stage)


@api_app.post('/inference-mri')
async def predict(file: UploadFile) -> str:
    logging.info("In inference...")
    model_name, model_stage = config.model_name, config.model_stage
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    return mri_cnn.predict(img, model_name, model_stage)


def generate_schema():
    """
    Used to render OpenAPI schema as a static page in Streamlit apps
    """
    with open('app/analytics/static/openapi.json', 'w') as f:
        json.dump(get_openapi(
            title=api_app.title,
            version=api_app.version,
            openapi_version="3.0.2",
            description=api_app.description,
            routes=api_app.routes,
        ), f, indent=4)


def custom_openapi():
    openapi_schema = get_openapi(
        title=api_app.title,
        version=api_app.version,
        openapi_version="3.0.2",
        description=api_app.description,
        routes=api_app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://blogs.vmware.com/cloudprovider/files/2021/11/tanzu-logo.png"
    }
    api_app.openapi_schema = openapi_schema
    return api_app.openapi_schema


api_app.openapi = custom_openapi
