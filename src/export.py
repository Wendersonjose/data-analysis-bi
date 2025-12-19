"""
Módulo para exportação de dados em CSV e Excel.
"""

import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class DataExporter:
    """Classe para exportar dados em diferentes formatos."""
    
    def __init__(self, output_dir: Path):
        """
        Inicializa o exportador.
        
        Args:
            output_dir: Diretório para salvar os arquivos.
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Exportador inicializado: {output_dir}")
    
    def exportar_csv(self, df: pd.DataFrame, nome_arquivo: str):
        """
        Exporta DataFrame para CSV.
        
        Args:
            df: DataFrame a exportar.
            nome_arquivo: Nome do arquivo (sem extensão).
        """
        if df.empty:
            logger.warning(f"DataFrame vazio, pulando exportação: {nome_arquivo}")
            return
        
        caminho = self.output_dir / f"{nome_arquivo}.csv"
        df.to_csv(caminho, index=False, encoding="utf-8-sig", sep=";", decimal=",")
        logger.info(f"✓ CSV exportado: {nome_arquivo}.csv ({len(df)} linhas)")
    
    def exportar_excel(self, dados: dict, nome_arquivo: str = "analise_extratos.xlsx"):
        """
        Exporta múltiplos DataFrames para Excel com abas.
        
        Args:
            dados: Dicionário {nome_aba: DataFrame}.
            nome_arquivo: Nome do arquivo Excel.
        """
        caminho = self.output_dir / nome_arquivo
        
        logger.info(f"Exportando Excel: {nome_arquivo}")
        
        with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
            for nome_aba, df in dados.items():
                if df.empty:
                    logger.warning(f"Aba '{nome_aba}' vazia, pulando")
                    continue
                
                # Limitar nome da aba a 31 caracteres (limite do Excel)
                nome_aba_limpo = nome_aba[:31]
                
                df.to_excel(writer, sheet_name=nome_aba_limpo, index=False)
                logger.info(f"  ✓ Aba '{nome_aba_limpo}': {len(df)} linhas")
        
        logger.info(f"✓ Excel exportado: {nome_arquivo}")
    
    def exportar_todos_csv(self, dados: dict):
        """
        Exporta todos os DataFrames como CSVs individuais.
        
        Args:
            dados: Dicionário {nome_arquivo: DataFrame}.
        """
        logger.info("Exportando todos os CSVs...")
        
        for nome, df in dados.items():
            self.exportar_csv(df, nome)
        
        logger.info("✓ Todos os CSVs foram exportados")
    
    def exportar_analise_completa(self,
                                  df_resumos: pd.DataFrame,
                                  df_transacoes: pd.DataFrame,
                                  df_fluxo: pd.DataFrame,
                                  df_saidas_cat: pd.DataFrame,
                                  df_entradas_cat: pd.DataFrame,
                                  df_top_saidas: pd.DataFrame,
                                  df_top_entradas: pd.DataFrame,
                                  df_indicadores: pd.DataFrame):
        """
        Exporta análise completa em CSV e Excel.
        
        Args:
            df_resumos: Resumos mensais.
            df_transacoes: Todas as transações.
            df_fluxo: Fluxo de caixa mensal.
            df_saidas_cat: Saídas por categoria.
            df_entradas_cat: Entradas por categoria.
            df_top_saidas: Top descrições de saídas.
            df_top_entradas: Top descrições de entradas.
            df_indicadores: Indicadores do período.
        """
        logger.info("Iniciando exportação completa...")
        
        # Preparar dados para CSV
        dados_csv = {
            "01_resumo_mensal": df_resumos,
            "02_movimentacoes": df_transacoes,
            "03_fluxo_caixa_mensal": df_fluxo,
            "04_saidas_por_categoria": df_saidas_cat,
            "05_entradas_por_categoria": df_entradas_cat,
            "06_top_saidas_descricao": df_top_saidas,
            "07_top_entradas_descricao": df_top_entradas,
            "08_indicadores": df_indicadores
        }
        
        # Exportar CSVs
        self.exportar_todos_csv(dados_csv)
        
        # Preparar dados para Excel (nomes mais curtos)
        dados_excel = {
            "Resumo Mensal": df_resumos,
            "Movimentações": df_transacoes,
            "Fluxo de Caixa": df_fluxo,
            "Saídas por Categoria": df_saidas_cat,
            "Entradas por Categoria": df_entradas_cat,
            "Top 50 Saídas": df_top_saidas,
            "Top 50 Entradas": df_top_entradas,
            "Indicadores": df_indicadores
        }
        
        # Exportar Excel
        self.exportar_excel(dados_excel)
        
        logger.info("✓ Exportação completa finalizada")
