from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import json
from services.llm_service import ai_engine

def export_rag_contents(index_path: str, embeddings) -> List[Dict]:
    """
    从FAISS索引中提取所有文档内容并结构化输出
    
    Args:
        index_path: 索引文件路径(.faiss)
        embeddings: 与索引匹配的嵌入模型
        
    Returns:
        List[Dict]: 结构化文档列表，包含元数据和内容
    """
    # 加载索引
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # 获取所有文档ID
    doc_ids = db.index_to_docstore_id.values()

    # 提取文档内容
    documents = []
    for doc_id in doc_ids:
        doc = db.docstore.search(doc_id)
        if isinstance(doc, Document):
            documents.append({
                "id": doc_id,
                "content": doc.page_content,
                "metadata": doc.metadata
            })
    print(documents)
    return documents

export_rag_contents("./store/user_2354365767", ai_engine.get_embedding_model())