"""
Módulo para leitura de arquivos PDF usando pdfplumber.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
import pdfplumber

logger = logging.getLogger(__name__)


class PDFReader:
    """Classe para leitura de extratos bancários em PDF."""
    
    def __init__(self, pdf_dir: Path):
        """
        Inicializa o leitor de PDFs.
        
        Args:
            pdf_dir: Diretório contendo os arquivos PDF.
        """
        self.pdf_dir = pdf_dir
        
    def list_pdfs(self) -> List[Path]:
        """
        Lista todos os arquivos PDF no diretório.
        
        Returns:
            Lista de caminhos para arquivos PDF.
        """
        pdf_files = sorted(self.pdf_dir.glob("*.pdf"))
        logger.info(f"Encontrados {len(pdf_files)} arquivos PDF em {self.pdf_dir}")
        return pdf_files
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extrai texto de um arquivo PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF.
            
        Returns:
            Dicionário contendo o texto extraído e metadados.
        """
        logger.info(f"Extraindo texto de: {pdf_path.name}")
        
        result = {
            "arquivo": pdf_path.name,
            "caminho": str(pdf_path),
            "texto_completo": "",
            "paginas": [],
            "sucesso": False,
            "erro": None
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                result["num_paginas"] = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages, 1):
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        result["paginas"].append({
                            "numero": i,
                            "texto": texto_pagina
                        })
                        result["texto_completo"] += texto_pagina + "\n"
                
                result["sucesso"] = True
                logger.info(f"✓ {pdf_path.name}: {len(pdf.pages)} página(s) extraída(s)")
                
        except Exception as e:
            result["erro"] = str(e)
            logger.error(f"✗ Erro ao extrair {pdf_path.name}: {e}")
        
        return result
    
    def extract_all_pdfs(self) -> List[Dict[str, Any]]:
        """
        Extrai texto de todos os PDFs no diretório.
        
        Returns:
            Lista de dicionários com dados extraídos.
        """
        pdf_files = self.list_pdfs()
        
        if not pdf_files:
            logger.warning("Nenhum arquivo PDF encontrado!")
            return []
        
        resultados = []
        for pdf_path in pdf_files:
            resultado = self.extract_text_from_pdf(pdf_path)
            resultados.append(resultado)
        
        sucessos = sum(1 for r in resultados if r["sucesso"])
        logger.info(f"Extração concluída: {sucessos}/{len(resultados)} PDFs processados com sucesso")
        
        return resultados
