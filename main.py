# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from routers.workflow import router as workflow_router

# load_dotenv()

# app = FastAPI(title="Crew Workflow API", version="1.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(workflow_router)

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}


import sys
if sys.platform == "linux":
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

from routers.workflow import router as workflow_router

def load_keyvault_secrets():
    try:
        vault_url = "https://hassaan-keyvault.vault.azure.net/"
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        os.environ["AZURE_OPENAI_ENDPOINT"] = client.get_secret("AZURE-OPENAI-ENDPOINT").value
        os.environ["AZURE_OPENAI_API_KEY"] = client.get_secret("AZURE-OPENAI-API-KEY").value
        os.environ["AZURE_OPENAI_API_VERSION"] = client.get_secret("AZURE-OPENAI-API-VERSION").value
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()

load_keyvault_secrets()

app = FastAPI(title="Crew Workflow API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
