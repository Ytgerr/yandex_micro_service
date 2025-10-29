from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from client import NeuroSupportClient

app = FastAPI(title="NeuroSupport API Gateway", version="1.0.0")
client = NeuroSupportClient()

class DialogMessage(BaseModel):
    role: str
    text: str

class AnswerRequest(BaseModel):
    dialog: List[DialogMessage]
    index_name: Optional[str] = None

class DocumentsRequest(BaseModel):
    documents: List[Dict[str, Any]]
    meta: Optional[Dict[str, Any]] = None
    auto_switch: bool = True
    diff: bool = False

class DeleteDocsRequest(BaseModel):
    docs_ids: List[str]

@app.get("/")
def root():
    return {"status": "API Gateway is running"}

@app.get("/health")
def health():
    try:
        return client.health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer")
def answer(req: AnswerRequest):
    try:
        dialog_formatted = [{"role": msg.role, "text": msg.text} for msg in req.dialog]
        return client.generate_answer(dialog=dialog_formatted, index_name=req.index_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indexes")
def list_indexes():
    try:
        return client.list_indexes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indexes/{index_name}")
def get_index(index_name: str, version: Optional[int] = None):
    try:
        return client.get_index_info(index_name=index_name, index_version=version)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/indexes/{index_name}/documents")
def upload_documents(index_name: str, req: DocumentsRequest):
    try:
        return client.upload_documents(index_name=index_name, documents=req.documents,
                                       meta=req.meta, auto_switch=req.auto_switch, diff=req.diff)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indexes/{index_name}/documents")
def get_documents(index_name: str, document_id: Optional[str] = None):
    try:
        return client.get_documents(index_name=index_name, document_id=document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/indexes/{index_name}/documents")
def delete_documents(index_name: str, req: DeleteDocsRequest):
    try:
        return client.delete_documents(index_name=index_name, docs_ids=req.docs_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/indexes/{index_name}/switch_version")
def switch_version(index_name: str, version: int):
    try:
        return client.switch_version(index_name=index_name, version=version)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/indexes/{index_name}/rename")
def rename_index(index_name: str, new_name: str):
    try:
        return client.rename_index(index_name=index_name, new_name=new_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/indexes/{index_name}/delete")
def delete_index(index_name: str):
    try:
        return client.delete_index(index_name=index_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
