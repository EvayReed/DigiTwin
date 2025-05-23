from fastapi import APIRouter, File, UploadFile, HTTPException,Header
from fastapi.responses import JSONResponse
import logging
from app.routes.pdfprocessor import PDFProcessor
from app.services.vector_database_server import vector_db_man
import os
from pathlib import Path
from app.core.utils.validate import get_token_from_header, handle_token_validation

router = APIRouter(tags=["pdf processing"])
logger = logging.getLogger(__name__)


# 创建上传目录
UPLOAD_DIR = Path("assets/pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...),
            authorization: str = Header(...),):
    """上传PDF文件并处理，返回所有提取的内容
    
    Args:
        file: 上传的PDF文件
        
    Returns:
        JSON响应，包含：
        - 文本内容
        - 表格数据
        - 带元数据的表格
        - 处理状态
        - 向量数据库存储结果
    """
    try:
        # 检查文件类型
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")
        
        # 保存文件
        file_location = UPLOAD_DIR / file.filename
        with file_location.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 处理PDF
        processor = PDFProcessor(str(file_location))
        
        # 提取文本
        text = processor.extract_text()
        text_with_layout = processor.extract_text_with_layout()
        
        # 提取表格
        tables = processor.extract_tables()
        tables_with_metadata = processor.extract_tables_with_metadata()
        
        # 将文本内容存储到向量数据库
        try:
            token = get_token_from_header(authorization)
            user_id = handle_token_validation(token)
            result = await vector_db_man.insert_into_vector_db_str(text, f'user_{user_id}')
            vector_db_state = {
                "message": "str uploaded successfully",
                "status": "success",
                "user_id": user_id
            }
        except ValueError as e:
            logger.error(f"ValueError in vector db storage: {str(e)}")
            vector_db_state = {
                "message": str(e),
                "status": "error",
                "error_type": "ValueError"
            }
        except Exception as e:
            logger.error(f"Unexpected error in vector db storage: {str(e)}")
            vector_db_state = {
                "message": "Internal server error",
                "status": "error",
                "error_type": "UnexpectedError"
            }
        
        return JSONResponse(content={
            "status": "success",
            "message": "PDF处理成功",
            "file_path": str(file_location),
            "text": {
                "plain_text": text,
                "text_with_layout": text_with_layout
            },
            "tables": {
                "simple_tables": tables,
                "tables_with_metadata": tables_with_metadata
            },
            "vector_db": vector_db_state
        })
        
    except Exception as e:
        logger.error(f"处理PDF时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """只提取PDF中的文本
    
    Args:
        file: 上传的PDF文件
        
    Returns:
        提取的文本内容
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")
        
        file_location = UPLOAD_DIR / file.filename
        with file_location.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        processor = PDFProcessor(str(file_location))
        text = processor.extract_text()
        
        return JSONResponse(content={
            "message": "文本提取成功",
            "text": text
        })
        
    except Exception as e:
        logger.error(f"提取文本时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-tables/")
async def extract_tables(file: UploadFile = File(...)):
    """提取PDF中的表格
    
    Args:
        file: 上传的PDF文件
        
    Returns:
        提取的表格数据
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")
        
        file_location = UPLOAD_DIR / file.filename
        with file_location.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        processor = PDFProcessor(str(file_location))
        tables = processor.extract_tables()
        tables_with_metadata = processor.extract_tables_with_metadata()
        
        return JSONResponse(content={
            "message": "表格提取成功",
            "tables": tables,
            "tables_with_metadata": tables_with_metadata
        })
        
    except Exception as e:
        logger.error(f"提取表格时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 