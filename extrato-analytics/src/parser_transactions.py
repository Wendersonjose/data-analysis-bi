"""
Parser para extrair transações individuais dos extratos bancários.
"""

import re
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TransactionParser:
    """Parser para transações individuais do extrato."""
    
    def __init__(self):
        """Inicializa o parser de transações."""
        self.data_pattern = re.compile(r'^(\d{2}/\d{2})')
        self.valor_pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2})-?')
        self.cabecalhos = [
            "data", "historico", "lancamento", "documento", "valor",
            "entrada", "saida", "saldo", "movimentacao"
        ]
    
    def parse_valor(self, texto: str) -> float:
        """
        Converte valor brasileiro para float.
        
        Args:
            texto: String com valor.
            
        Returns:
            Valor como float.
        """
        if not texto:
            return 0.0
        
        texto = texto.strip()
        is_negative = texto.endswith("-")
        
        valor_limpo = texto.replace(".", "").replace(",", ".").replace("-", "")
        
        try:
            valor = float(valor_limpo)
            return -valor if is_negative else valor
        except ValueError:
            return 0.0
    
    def eh_cabecalho(self, linha: str) -> bool:
        """
        Verifica se a linha é um cabeçalho de tabela.
        
        Args:
            linha: Linha de texto.
            
        Returns:
            True se for cabeçalho.
        """
        linha_lower = linha.lower().strip()
        return any(cab in linha_lower for cab in self.cabecalhos)
    
    def extrair_ano_extrato(self, texto: str) -> Optional[int]:
        """
        Tenta extrair o ano do extrato.
        
        Args:
            texto: Texto do extrato.
            
        Returns:
            Ano como inteiro ou None.
        """
        # Procurar por datas completas
        match = re.search(r'(\d{2}/\d{2}/(\d{4}))', texto)
        if match:
            return int(match.group(2))
        
        # Procurar por "mês/ano"
        match = re.search(r'(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s*[/\-]?\s*(\d{4})', texto, re.IGNORECASE)
        if match:
            return int(match.group(2))
        
        # Usar ano atual como fallback
        return datetime.now().year
    
    def recompor_transacao(self, linhas: List[str], index: int) -> tuple:
        """
        Recompõe uma transação que pode estar quebrada em múltiplas linhas.
        
        Args:
            linhas: Lista de todas as linhas.
            index: Índice da linha inicial.
            
        Returns:
            Tupla (linha_completa, linhas_consumidas).
        """
        linha_atual = linhas[index]
        linhas_consumidas = 1
        
        # Verificar se precisa juntar linhas seguintes
        next_index = index + 1
        while next_index < len(linhas):
            proxima_linha = linhas[next_index].strip()
            
            # Parar se encontrar nova data ou cabeçalho
            if self.data_pattern.match(proxima_linha) or self.eh_cabecalho(proxima_linha):
                break
            
            # Parar se linha vazia
            if not proxima_linha:
                break
            
            # Juntar linha
            linha_atual += " " + proxima_linha
            linhas_consumidas += 1
            next_index += 1
            
            # Limitar a 5 linhas para evitar loops infinitos
            if linhas_consumidas >= 5:
                break
        
        return linha_atual, linhas_consumidas
    
    def extrair_transacao_da_linha(self, linha: str, ano: int, arquivo: str, mes_key: Optional[str] = None) -> Optional[Dict]:
        """
        Extrai dados de uma transação de uma linha.
        
        Args:
            linha: Linha de texto.
            ano: Ano do extrato.
            arquivo: Nome do arquivo.
            mes_key: Chave do mês (YYYY-MM).
            
        Returns:
            Dicionário com dados da transação ou None.
        """
        # Extrair data (dd/mm)
        match_data = self.data_pattern.match(linha)
        if not match_data:
            return None
        
        data_str = match_data.group(1)
        
        # Extrair valores monetários
        valores = self.valor_pattern.findall(linha)
        
        if not valores:
            return None
        
        # Remover a data da linha para pegar descrição
        resto_linha = linha[len(data_str):].strip()
        
        # Tentar identificar entrada/saída/saldo
        valor_entrada = 0.0
        valor_saida = 0.0
        saldo = 0.0
        
        if len(valores) == 1:
            # Apenas um valor: pode ser entrada ou saída
            val = self.parse_valor(valores[0])
            if val < 0:
                valor_saida = abs(val)
            else:
                # Verificar se termina com - para identificar saída
                if valores[0].endswith("-"):
                    valor_saida = abs(val)
                else:
                    valor_entrada = abs(val)
        
        elif len(valores) == 2:
            # Dois valores: possivelmente entrada/saída + saldo
            val1 = self.parse_valor(valores[0])
            val2 = self.parse_valor(valores[1])
            
            # O último geralmente é o saldo
            saldo = val2
            
            # O primeiro é entrada ou saída
            if valores[0].endswith("-"):
                valor_saida = abs(val1)
            else:
                valor_entrada = abs(val1)
        
        elif len(valores) >= 3:
            # Três valores: entrada, saída, saldo
            valor_entrada = abs(self.parse_valor(valores[0]))
            valor_saida = abs(self.parse_valor(valores[1]))
            saldo = self.parse_valor(valores[2])
        
        # Extrair descrição (remover valores monetários)
        descricao = resto_linha
        for valor in valores:
            descricao = descricao.replace(valor, "")
        descricao = " ".join(descricao.split()).strip()
        
        # Completar data com ano
        data_completa = f"{data_str}/{ano}"
        
        return {
            "arquivo": arquivo,
            "mes_key": mes_key,
            "data": data_completa,
            "descricao": descricao,
            "valor_entrada": valor_entrada,
            "valor_saida": valor_saida,
            "saldo": saldo
        }
    
    def extrair_transacoes(self, texto: str, arquivo: str, mes_key: Optional[str] = None) -> List[Dict]:
        """
        Extrai todas as transações do texto do extrato.
        
        Args:
            texto: Texto completo do extrato.
            arquivo: Nome do arquivo PDF.
            mes_key: Chave do mês (YYYY-MM).
            
        Returns:
            Lista de transações.
        """
        logger.info(f"Extraindo transações de: {arquivo}")
        
        linhas = texto.split("\n")
        ano = self.extrair_ano_extrato(texto)
        
        transacoes = []
        i = 0
        
        while i < len(linhas):
            linha = linhas[i].strip()
            
            # Verificar se linha começa com data
            if self.data_pattern.match(linha):
                # Recompor transação se estiver quebrada
                linha_completa, consumidas = self.recompor_transacao(linhas, i)
                
                # Extrair transação
                transacao = self.extrair_transacao_da_linha(linha_completa, ano, arquivo, mes_key)
                
                if transacao:
                    transacoes.append(transacao)
                
                i += consumidas
            else:
                i += 1
        
        logger.info(f"✓ {len(transacoes)} transações extraídas de {arquivo}")
        return transacoes
    
    def extrair_transacoes_multiplas(self, dados_pdfs: List[Dict], resumos: List[Dict]) -> List[Dict]:
        """
        Extrai transações de múltiplos PDFs.
        
        Args:
            dados_pdfs: Lista de dados dos PDFs.
            resumos: Lista de resumos extraídos (para pegar mes_key).
            
        Returns:
            Lista de todas as transações.
        """
        todas_transacoes = []
        
        # Criar mapa de arquivo -> mes_key
        mes_map = {r["arquivo"]: r.get("mes_key") for r in resumos}
        
        for dados in dados_pdfs:
            if dados.get("sucesso") and dados.get("texto_completo"):
                arquivo = dados["arquivo"]
                mes_key = mes_map.get(arquivo)
                
                transacoes = self.extrair_transacoes(
                    dados["texto_completo"],
                    arquivo,
                    mes_key
                )
                todas_transacoes.extend(transacoes)
        
        logger.info(f"Total de transações extraídas: {len(todas_transacoes)}")
        return todas_transacoes
