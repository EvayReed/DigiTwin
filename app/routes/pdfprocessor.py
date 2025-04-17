from PyPDF2 import PdfReader
import os
from typing import List, Tuple
import logging
import pdfplumber

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_path: str):
        # 转换为绝对路径
        self.pdf_path = os.path.abspath(pdf_path)
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"找不到PDF文件: {self.pdf_path}")
        logger.info(f"正在处理PDF文件: {self.pdf_path}")
        self.reader = PdfReader(self.pdf_path)
        self.pdf_plumber = pdfplumber.open(self.pdf_path)
        
    def extract_text(self) -> str:
        """提取 PDF 中的文本内容"""
        text = ""
        try:
            # 使用 pdfplumber 提取文本
            for page in self.pdf_plumber.pages:
                # 提取文本，包括表格
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                
                # 提取表格
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            text += " | ".join(str(cell) for cell in row if cell) + "\n"
                        text += "\n"
            
            # 如果 pdfplumber 提取的文本为空，尝试使用 PyPDF2
            if not text.strip():
                logger.warning("pdfplumber 未能提取文本，尝试使用 PyPDF2...")
                for page in self.reader.pages:
                    text += page.extract_text() + "\n"
            
            return text
            
        except Exception as e:
            logger.error(f"提取文本时发生错误: {str(e)}")
            # 如果发生错误，回退到 PyPDF2
            logger.warning("使用 PyPDF2 作为备选方案...")
            text = ""
            for page in self.reader.pages:
                text += page.extract_text() + "\n"
            return text
    
    def extract_text_with_layout(self) -> str:
        """提取 PDF 中的文本，保持布局"""
        text = ""
        try:
            for page in self.pdf_plumber.pages:
                # 提取文本，保持布局
                words = page.extract_words()
                if words:
                    # 按 y 坐标排序，保持垂直布局
                    words.sort(key=lambda x: (x['top'], x['x0']))
                    current_y = None
                    for word in words:
                        if current_y is None or abs(word['top'] - current_y) > 5:
                            text += "\n"
                            current_y = word['top']
                        text += word['text'] + " "
                text += "\n\n"
            return text
        except Exception as e:
            logger.error(f"提取布局文本时发生错误: {str(e)}")
            return self.extract_text()
    
    def extract_tables(self) -> List[List[List[str]]]:
        """提取 PDF 中的表格，并进行优化处理
        
        Returns:
            处理后的表格列表，每个表格是一个二维列表
        """
        tables = []
        try:
            for page in self.pdf_plumber.pages:
                # 使用更精确的表格检测设置
                page_tables = page.extract_tables({
                    'vertical_strategy': 'text',  # 使用文本边界作为垂直分隔线
                    'horizontal_strategy': 'text',  # 使用文本边界作为水平分隔线
                    'intersection_y_tolerance': 10,  # 允许的垂直误差
                    'intersection_x_tolerance': 10,  # 允许的水平误差
                    'snap_y_tolerance': 3,  # 垂直对齐容差
                    'snap_x_tolerance': 3,  # 水平对齐容差
                })
                
                if page_tables:
                    for table in page_tables:
                        # 清理和格式化表格数据
                        processed_table = []
                        for row in table:
                            # 清理空单元格和多余空格
                            processed_row = [
                                str(cell).strip() if cell is not None else ""
                                for cell in row
                            ]
                            # 移除完全空的行
                            if any(cell for cell in processed_row):
                                processed_table.append(processed_row)
                        
                        # 处理可能的合并单元格
                        if processed_table:
                            # 检测可能的表头
                            header_row = processed_table[0]
                            # 如果第一行有重复的列标题，可能是合并单元格
                            if len(set(header_row)) < len(header_row):
                                # 合并重复的列标题
                                merged_header = []
                                current = ""
                                for cell in header_row:
                                    if cell and cell != current:
                                        merged_header.append(cell)
                                        current = cell
                                    else:
                                        merged_header.append("")
                                processed_table[0] = merged_header
                            
                            tables.append(processed_table)
            
            return tables
            
        except Exception as e:
            logger.error(f"提取表格时发生错误: {str(e)}")
            return []
    
    def extract_tables_with_metadata(self) -> List[dict]:
        """提取表格及其元数据（位置、标题等）
        
        Returns:
            包含表格及其元数据的列表
        """
        tables_with_metadata = []
        try:
            for page_num, page in enumerate(self.pdf_plumber.pages):
                # 获取页面上的所有文本块
                words = page.extract_words()
                # 使用与 extract_tables 相同的设置
                settings = {
                    'vertical_strategy': 'text',
                    'horizontal_strategy': 'text',
                    'intersection_y_tolerance': 10,
                    'intersection_x_tolerance': 10,
                    'snap_y_tolerance': 3,
                    'snap_x_tolerance': 3,
                }
                
                # 提取表格
                tables = page.extract_tables(settings)
                
                if tables:
                    for table_idx, table in enumerate(tables):
                        table_data = {
                            'page': page_num + 1,
                            'table_index': table_idx,
                            'data': [],
                            'title': None,
                            'position': None
                        }
                        
                        # 处理表格数据
                        processed_table = []
                        for row in table:
                            processed_row = [
                                str(cell).strip() if cell is not None else ""
                                for cell in row
                            ]
                            if any(cell for cell in processed_row):
                                processed_table.append(processed_row)
                        
                        table_data['data'] = processed_table
                        
                        # 尝试识别表格标题
                        if words and processed_table:
                            # 获取表格的大致位置（使用第一行作为参考）
                            first_row_words = [word for word in words if any(cell in word['text'] for cell in processed_table[0])]
                            if first_row_words:
                                min_y = min(word['top'] for word in first_row_words)
                                # 查找表格上方的文本作为可能的标题
                                title_words = []
                                for word in words:
                                    if word['bottom'] < min_y and abs(word['bottom'] - min_y) < 20:
                                        title_words.append(word)
                                
                                # 按位置排序并组合标题
                                if title_words:
                                    title_words.sort(key=lambda x: (x['top'], x['x0']))
                                    table_data['title'] = " ".join(word['text'] for word in title_words)
                        
                                # 记录表格位置
                                table_data['position'] = {
                                    'x0': min(word['x0'] for word in first_row_words),
                                    'y0': min_y,
                                    'x1': max(word['x1'] for word in first_row_words),
                                    'y1': max(word['bottom'] for word in first_row_words)
                                }
                        
                        tables_with_metadata.append(table_data)
            
            return tables_with_metadata
            
        except Exception as e:
            logger.error(f"提取表格元数据时发生错误: {str(e)}")
            return []
    
    def process_pdf(self) -> str:
        """处理 PDF 文件，提取文本
        
        Returns:
            提取的文本内容
        """
        try:
            logger.info("开始提取文本...")
            text = self.extract_text()
            logger.info("文本提取完成")
            return text
        except Exception as e:
            logger.error(f"处理PDF时发生错误: {str(e)}")
            raise

