from langchain.document_loaders import TextLoader, UnstructuredExcelLoader, CSVLoader
from langchain_community.document_loaders import PyPDFLoader, JSONLoader
import os
from pydantic import BaseModel, Field, FilePath
from typing import Dict, Any, Tuple, Type


class LoaderConfig(BaseModel):
    loader_class: Type
    default_params: Dict[str, Any] = Field(default_factory=dict)


class MultiFileLoader:
    LOADER_CONFIG = {
        '.txt': LoaderConfig(loader_class=TextLoader),
        '.md': LoaderConfig(loader_class=TextLoader),
        '.csv': LoaderConfig(loader_class=CSVLoader),
        '.xlsx': LoaderConfig(loader_class=UnstructuredExcelLoader, default_params={'mode': "elements"}),
        '.pdf': LoaderConfig(loader_class=PyPDFLoader),
        '.json': LoaderConfig(loader_class=JSONLoader, default_params={'jq_schema': '.'})
    }

    def __init__(self, file_path: FilePath, loader_params: Dict[str, Any] = None):
        self.file_path = file_path
        self.loader_params = loader_params or {}

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file path does not exist: {file_path}")

        self.file_ext = os.path.splitext(file_path)[1].lower()
        if self.file_ext not in self.LOADER_CONFIG:
            supported = ', '.join(self.LOADER_CONFIG.keys())
            raise ValueError(f"Unsupported file types {self.file_ext}，support type：{supported}")

    def _get_loader_config(self) -> Tuple[Type, Dict[str, Any]]:
        config = self.LOADER_CONFIG[self.file_ext]
        merged_params = {**config.default_params, **self.loader_params}
        return config.loader_class, merged_params

    def load(self):
        loader_class, params = self._get_loader_config()
        try:
            loader = loader_class(self.file_path, **params)
            return loader.load()
        except Exception as e:
            error_msg = f"Failed to load {self.file_ext} file: {str(e)}"
            raise RuntimeError(error_msg) from e
