from langchain.document_loaders import TextLoader, UnstructuredExcelLoader, CSVLoader
from langchain_community.document_loaders import PyPDFLoader, JSONLoader
import os


class MultiFileLoader:
    LOADER_CONFIG = {
        '.txt': (TextLoader, {}),
        '.md': (TextLoader, {}),
        '.csv': (CSVLoader, {}),
        '.xlsx': (UnstructuredExcelLoader, {'mode': "elements"}),
        '.pdf': (PyPDFLoader, {}),
        '.json': (JSONLoader, {'jq_schema': '.'})
    }

    def __init__(self, file_path: str, loader_params: dict = None):
        self.file_path = file_path
        self.loader_params = loader_params or {}

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file path does not exist: {file_path}")

        self.file_ext = os.path.splitext(file_path)[1].lower()
        if self.file_ext not in self.LOADER_CONFIG:
            supported = ', '.join(self.LOADER_CONFIG.keys())
            raise ValueError(f"Unsupported file types {self.file_ext}，support type：{supported}")

    def _get_loader_config(self):
        loader_class, default_params = self.LOADER_CONFIG[self.file_ext]
        merged_params = {**default_params, **self.loader_params.get(self.file_ext, {})}
        return loader_class, merged_params

    def load(self):
        loader_class, params = self._get_loader_config()
        try:
            loader = loader_class(self.file_path, **params)
            return loader.load()
        except Exception as e:
            error_msg = f"Failed to load {self.file_ext} file: {str(e)}"
            raise RuntimeError(error_msg) from e
