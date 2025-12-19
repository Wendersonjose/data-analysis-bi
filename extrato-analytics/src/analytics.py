"""
Módulo de análises e consolidações dos dados.
"""

import logging
import pandas as pd
from typing import List, Dict

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Classe para realizar análises nos dados extraídos."""
    
    def __init__(self, resumos: List[Dict], transacoes: List[Dict]):
        """
        Inicializa o analisador.
        
        Args:
            resumos: Lista de resumos mensais.
            transacoes: Lista de transações.
        """
        self.df_resumos = pd.DataFrame(resumos)
        self.df_transacoes = pd.DataFrame(transacoes)
        
        logger.info(f"Analisador inicializado: {len(resumos)} resumos, {len(transacoes)} transações")
    
    def gerar_fluxo_mensal(self) -> pd.DataFrame:
        """
        Gera tabela de fluxo de caixa mensal.
        
        Returns:
            DataFrame com fluxo mensal.
        """
        logger.info("Gerando fluxo mensal...")
        
        if self.df_resumos.empty:
            return pd.DataFrame()
        
        df = self.df_resumos.copy()
        
        # Calcular resultado líquido
        df["resultado_liquido"] = df["total_entradas"] - df["total_saidas"]
        
        # Selecionar colunas relevantes
        colunas = [
            "mes_key", "mes_label", "total_entradas", "total_saidas",
            "resultado_liquido", "saldo_inicial", "saldo_final"
        ]
        
        colunas_existentes = [c for c in colunas if c in df.columns]
        df_fluxo = df[colunas_existentes].copy()
        
        # Ordenar por mês
        if "mes_key" in df_fluxo.columns:
            df_fluxo = df_fluxo.sort_values("mes_key")
        
        logger.info(f"✓ Fluxo mensal gerado: {len(df_fluxo)} meses")
        return df_fluxo
    
    def gerar_totais_periodo(self) -> pd.DataFrame:
        """
        Gera tabela com totais do período.
        
        Returns:
            DataFrame com indicadores do período.
        """
        logger.info("Calculando totais do período...")
        
        if self.df_resumos.empty:
            return pd.DataFrame()
        
        indicadores = {
            "Indicador": [
                "Total de Entradas",
                "Total de Saídas",
                "Resultado Líquido",
                "Média Mensal de Entradas",
                "Média Mensal de Saídas",
                "Média Mensal de Resultado",
                "Número de Meses"
            ],
            "Valor": [
                self.df_resumos["total_entradas"].sum(),
                self.df_resumos["total_saidas"].sum(),
                self.df_resumos["total_entradas"].sum() - self.df_resumos["total_saidas"].sum(),
                self.df_resumos["total_entradas"].mean(),
                self.df_resumos["total_saidas"].mean(),
                (self.df_resumos["total_entradas"] - self.df_resumos["total_saidas"]).mean(),
                len(self.df_resumos)
            ]
        }
        
        df_indicadores = pd.DataFrame(indicadores)
        logger.info("✓ Totais do período calculados")
        return df_indicadores
    
    def gerar_ranking_categorias(self, tipo: str = "saida") -> pd.DataFrame:
        """
        Gera ranking de categorias por entradas ou saídas.
        
        Args:
            tipo: "entrada" ou "saida"
            
        Returns:
            DataFrame com ranking.
        """
        logger.info(f"Gerando ranking de {tipo}s por categoria...")
        
        if self.df_transacoes.empty:
            return pd.DataFrame()
        
        coluna_valor = f"valor_{tipo}"
        
        if coluna_valor not in self.df_transacoes.columns:
            return pd.DataFrame()
        
        # Filtrar apenas transações com valor > 0
        df = self.df_transacoes[self.df_transacoes[coluna_valor] > 0].copy()
        
        # Agrupar por categoria
        ranking = df.groupby("categoria").agg({
            coluna_valor: ["sum", "count", "mean"]
        }).reset_index()
        
        ranking.columns = ["categoria", f"total_{tipo}", "quantidade", f"media_{tipo}"]
        ranking = ranking.sort_values(f"total_{tipo}", ascending=False)
        
        logger.info(f"✓ Ranking de {tipo}s gerado: {len(ranking)} categorias")
        return ranking
    
    def gerar_ranking_categorias_mensal(self, tipo: str = "saida") -> pd.DataFrame:
        """
        Gera ranking de categorias por mês.
        
        Args:
            tipo: "entrada" ou "saida"
            
        Returns:
            DataFrame com ranking mensal.
        """
        logger.info(f"Gerando ranking mensal de {tipo}s...")
        
        if self.df_transacoes.empty:
            return pd.DataFrame()
        
        coluna_valor = f"valor_{tipo}"
        
        if coluna_valor not in self.df_transacoes.columns or "mes_key" not in self.df_transacoes.columns:
            return pd.DataFrame()
        
        # Filtrar e agrupar
        df = self.df_transacoes[self.df_transacoes[coluna_valor] > 0].copy()
        
        ranking_mensal = df.groupby(["mes_key", "categoria"]).agg({
            coluna_valor: "sum"
        }).reset_index()
        
        ranking_mensal.columns = ["mes_key", "categoria", f"total_{tipo}"]
        ranking_mensal = ranking_mensal.sort_values(["mes_key", f"total_{tipo}"], ascending=[True, False])
        
        logger.info(f"✓ Ranking mensal gerado")
        return ranking_mensal
    
    def gerar_top_descricoes(self, tipo: str = "saida", top_n: int = 50) -> pd.DataFrame:
        """
        Gera ranking das principais descrições.
        
        Args:
            tipo: "entrada" ou "saida"
            top_n: Número de itens no ranking
            
        Returns:
            DataFrame com top descrições.
        """
        logger.info(f"Gerando top {top_n} descrições de {tipo}s...")
        
        if self.df_transacoes.empty:
            return pd.DataFrame()
        
        coluna_valor = f"valor_{tipo}"
        
        if coluna_valor not in self.df_transacoes.columns:
            return pd.DataFrame()
        
        # Filtrar e agrupar por descrição
        df = self.df_transacoes[self.df_transacoes[coluna_valor] > 0].copy()
        
        top_desc = df.groupby("descricao").agg({
            coluna_valor: ["sum", "count"],
            "categoria": "first"
        }).reset_index()
        
        top_desc.columns = ["descricao", f"total_{tipo}", "quantidade", "categoria"]
        top_desc = top_desc.sort_values(f"total_{tipo}", ascending=False).head(top_n)
        
        logger.info(f"✓ Top {len(top_desc)} descrições gerado")
        return top_desc
    
    def gerar_serie_temporal(self) -> pd.DataFrame:
        """
        Gera série temporal de resultado líquido.
        
        Returns:
            DataFrame com série temporal.
        """
        logger.info("Gerando série temporal...")
        
        if self.df_resumos.empty:
            return pd.DataFrame()
        
        df = self.df_resumos.copy()
        df["resultado_liquido"] = df["total_entradas"] - df["total_saidas"]
        
        serie = df[["mes_key", "mes_label", "resultado_liquido"]].copy()
        
        if "mes_key" in serie.columns:
            serie = serie.sort_values("mes_key")
        
        logger.info(f"✓ Série temporal gerada: {len(serie)} períodos")
        return serie
    
    def gerar_pareto_categorias(self, tipo: str = "saida") -> pd.DataFrame:
        """
        Gera análise de Pareto por categoria.
        
        Args:
            tipo: "entrada" ou "saida"
            
        Returns:
            DataFrame com análise de Pareto.
        """
        logger.info(f"Gerando análise de Pareto para {tipo}s...")
        
        ranking = self.gerar_ranking_categorias(tipo)
        
        if ranking.empty:
            return pd.DataFrame()
        
        coluna_total = f"total_{tipo}"
        
        # Calcular percentuais
        total_geral = ranking[coluna_total].sum()
        ranking["percentual"] = (ranking[coluna_total] / total_geral * 100).round(2)
        ranking["percentual_acumulado"] = ranking["percentual"].cumsum().round(2)
        
        logger.info("✓ Análise de Pareto gerada")
        return ranking
