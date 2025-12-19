"""
Parser para extrair o resumo mensal dos extratos bancários.
"""

import re
import logging
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class SummaryParser:
    """Parser para o resumo mensal do extrato."""
    
    # Mapeamento de meses
    MESES_PT = {
        "jan": "01", "fev": "02", "mar": "03", "abr": "04",
        "mai": "05", "jun": "06", "jul": "07", "ago": "08",
        "set": "09", "out": "10", "nov": "11", "dez": "12"
    }
    
    def __init__(self):
        """Inicializa o parser de resumo."""
        self.valor_pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2})-?')
        self.data_pattern = re.compile(r'(\d{2}/\d{2}/\d{4})')
        self.mes_ano_pattern = re.compile(r'(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s*[/\-]?\s*(\d{4})', re.IGNORECASE)
    
    def parse_valor(self, texto: str) -> float:
        """
        Converte valor no formato brasileiro para float.
        
        Args:
            texto: String com o valor (ex: "1.234,56" ou "1.234,56-")
            
        Returns:
            Valor como float (saídas são negativas).
        """
        if not texto:
            return 0.0
        
        # Remover espaços
        texto = texto.strip()
        
        # Verificar se é negativo (termina com -)
        is_negative = texto.endswith("-")
        
        # Remover pontos de milhar e substituir vírgula por ponto
        valor_limpo = texto.replace(".", "").replace(",", ".").replace("-", "")
        
        try:
            valor = float(valor_limpo)
            return -valor if is_negative else valor
        except ValueError:
            return 0.0
    
    def extrair_mes_ano(self, texto: str) -> Optional[Dict[str, str]]:
        """
        Extrai mês e ano do extrato.
        
        Args:
            texto: Texto do extrato.
            
        Returns:
            Dicionário com mes_key (YYYY-MM) e mes_label (mes/ano).
        """
        match = self.mes_ano_pattern.search(texto)
        if match:
            mes_nome = match.group(1).lower()
            ano = match.group(2)
            mes_num = self.MESES_PT.get(mes_nome)
            
            if mes_num:
                return {
                    "mes_key": f"{ano}-{mes_num}",
                    "mes_label": f"{mes_nome}/{ano}"
                }
        
        # Fallback: tentar encontrar data e extrair mês/ano
        datas = self.data_pattern.findall(texto)
        if datas:
            try:
                data_obj = datetime.strptime(datas[0], "%d/%m/%Y")
                mes_nome = list(self.MESES_PT.keys())[data_obj.month - 1]
                return {
                    "mes_key": data_obj.strftime("%Y-%m"),
                    "mes_label": f"{mes_nome}/{data_obj.year}"
                }
            except:
                pass
        
        return None
    
    def extrair_resumo(self, texto: str, arquivo: str) -> Dict[str, any]:
        """
        Extrai o resumo mensal do texto do extrato.
        
        Args:
            texto: Texto completo do extrato.
            arquivo: Nome do arquivo PDF.
            
        Returns:
            Dicionário com os valores do resumo.
        """
        logger.info(f"Extraindo resumo de: {arquivo}")
        
        resumo = {
            "arquivo": arquivo,
            "mes_key": None,
            "mes_label": None,
            "depositos_recebimentos": 0.0,
            "transferencias_doc_ted": 0.0,
            "outras_entradas": 0.0,
            "saques_efetuados": 0.0,
            "debitos_automaticos": 0.0,
            "outras_saidas": 0.0,
            "total_entradas": 0.0,
            "total_saidas": 0.0,
            "saldo_inicial": 0.0,
            "saldo_final": 0.0
        }
        
        # Extrair mês e ano
        mes_info = self.extrair_mes_ano(texto)
        if mes_info:
            resumo.update(mes_info)
        
        # Extrair valores do resumo
        linhas = texto.split("\n")
        
        # Flags para controlar qual seção estamos lendo
        lendo_entradas = False
        lendo_saidas = False
        
        for i, linha in enumerate(linhas):
            linha_lower = linha.lower().strip()
            
            # Detectar início da seção de entradas
            if "entradas" in linha_lower and "(" in linha_lower and "crédito" in linha_lower:
                lendo_entradas = True
                lendo_saidas = False
                continue
            
            # Detectar início da seção de saídas
            if "saídas" in linha_lower or "saidas" in linha_lower:
                if "(" in linha_lower and "débito" in linha_lower:
                    lendo_entradas = False
                    lendo_saidas = True
                    continue
            
            # Depósitos e recebimentos
            if "depositos" in linha_lower or "recebimentos" in linha_lower:
                if "depositos" in linha_lower and "recebimentos" in linha_lower:
                    valores = self.valor_pattern.findall(linha)
                    if valores:
                        resumo["depositos_recebimentos"] = abs(self.parse_valor(valores[-1]))
            
            # Transferências DOC/TED
            if "transferencias" in linha_lower or ("doc" in linha_lower and "ted" in linha_lower):
                valores = self.valor_pattern.findall(linha)
                if valores and "depositos" not in linha_lower:
                    resumo["transferencias_doc_ted"] = abs(self.parse_valor(valores[-1]))
            
            # Outras entradas
            if "outras entradas" in linha_lower:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["outras_entradas"] = self.parse_valor(valores[-1])
            
            # Saques
            if "saques" in linha_lower or "saque efetuado" in linha_lower:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["saques_efetuados"] = abs(self.parse_valor(valores[-1]))
            
            # Débitos automáticos
            if "debitos automaticos" in linha_lower or "débitos automáticos" in linha_lower:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["debitos_automaticos"] = abs(self.parse_valor(valores[-1]))
            
            # Outras saídas
            if "outras saidas" in linha_lower or "outras saídas" in linha_lower:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["outras_saidas"] = abs(self.parse_valor(valores[-1]))
            
            # Total de entradas - procurar "total" na seção de entradas
            if linha_lower.startswith("total") and lendo_entradas:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["total_entradas"] = abs(self.parse_valor(valores[-1]))
                    lendo_entradas = False
            
            # Total de saídas - procurar "total" na seção de saídas
            if linha_lower.startswith("total") and lendo_saidas:
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["total_saidas"] = abs(self.parse_valor(valores[-1]))
                    lendo_saidas = False
            
            # Saldo inicial
            if "saldo em" in linha_lower and i < len(linhas) / 2:  # Provavelmente saldo inicial
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["saldo_inicial"] = self.parse_valor(valores[-1])
            
            # Saldo final
            if "saldo em" in linha_lower and i > len(linhas) / 2:  # Provavelmente saldo final
                valores = self.valor_pattern.findall(linha)
                if valores:
                    resumo["saldo_final"] = self.parse_valor(valores[-1])
        
        logger.info(f"✓ Resumo extraído: {resumo['mes_label'] or 'mês não identificado'}")
        return resumo
    
    def extrair_resumos_multiplos(self, dados_pdfs: List[Dict]) -> List[Dict]:
        """
        Extrai resumos de múltiplos PDFs.
        
        Args:
            dados_pdfs: Lista de dicionários com dados dos PDFs.
            
        Returns:
            Lista de resumos extraídos.
        """
        resumos = []
        
        for dados in dados_pdfs:
            if dados.get("sucesso") and dados.get("texto_completo"):
                resumo = self.extrair_resumo(
                    dados["texto_completo"],
                    dados["arquivo"]
                )
                resumos.append(resumo)
        
        logger.info(f"Total de resumos extraídos: {len(resumos)}")
        return resumos
