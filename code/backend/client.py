import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import yandex_neurosupport as nrsprt

load_dotenv()

class NeuroSupportClient:
    def __init__(self):
        self.auth_token = os.getenv("IAM_TOKEN") 
        self.folder_id = os.getenv("FOLDER_ID")
        self.service = os.getenv("SERVICE")
        self.product = os.getenv("PRODUCT")
        self.client = nrsprt.YandexCloudNeuroSupportClient(
            auth_token=self.auth_token,
            folder_id=self.folder_id,
            service=self.service,
            product=self.product
        )


    def health(self) -> Dict[str, Any]:
        try:
            return self.client.get_indexes_full()
        except Exception as e:
            return {"error": str(e)}


    def generate_answer(self, dialog: List[Dict[str, str]], index_name: Optional[str] = None) -> Dict[str, Any]:
        return self.client.get_generative_answer(index_name=index_name, dialog=dialog)

    def list_indexes(self) -> Dict[str, Any]:
        return self.client.get_indexes_full()

    def get_index_info(self, index_name: str, index_version: Optional[int] = None) -> Dict[str, Any]:
        return self.client.get_index_info(index_name=index_name, index_version=index_version)

    def upload_documents(self, index_name: str, documents: List[Dict[str, Any]], meta: Optional[Dict[str, Any]] = None,
                         auto_switch: bool = True, diff: bool = False) -> Dict[str, Any]:
        return self.client.create_or_update_index(index_name=index_name, documents=documents, meta=meta,
                                                  auto_switch=auto_switch, diff=diff)

    def get_documents(self, index_name: str, document_id: Optional[str] = None) -> Dict[str, Any]:
        return self.client.get_documents_from_index(index_name=index_name, document_id=document_id)

    def delete_documents(self, index_name: str, docs_ids: List[str]) -> Dict[str, Any]:
        return self.client.delete_documents_from_index(index_name=index_name, docs_ids=docs_ids)

    def switch_version(self, index_name: str, version: int) -> Dict[str, Any]:
        return self.client.switch_index_version(index_name=index_name, index_version=version)

    def rename_index(self, index_name: str, new_name: str) -> Dict[str, Any]:
        return self.client.rename_index(index_name=index_name, new_name=new_name)

    def delete_index(self, index_name: str) -> Dict[str, Any]:
        return self.client.delete_index(index_name=index_name)
