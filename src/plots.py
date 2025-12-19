"""
Módulo para geração de gráficos usando matplotlib.
"""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Classe para geração de gráficos."""
    
    def __init__(self, output_dir: Path):
        """
        Inicializa o gerador de gráficos.
        
        Args:
            output_dir: Diretório para salvar os gráficos.
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar estilo matplotlib
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
        
        logger.info(f"Gerador de gráficos inicializado: {output_dir}")
    
    def salvar_grafico(self, nome_arquivo: str):
        """
        Salva o gráfico atual.
        
        Args:
            nome_arquivo: Nome do arquivo (sem extensão).
        """
        caminho = self.output_dir / f"{nome_arquivo}.png"
        plt.tight_layout()
        plt.savefig(caminho, dpi=150, bbox_inches='tight')
        plt.close()
        logger.info(f"✓ Gráfico salvo: {nome_arquivo}.png")
    
    def grafico_entradas_por_mes(self, df_fluxo: pd.DataFrame):
        """
        Gera gráfico de linha com entradas por mês.
        
        Args:
            df_fluxo: DataFrame com fluxo mensal.
        """
        if df_fluxo.empty or "total_entradas" not in df_fluxo.columns:
            logger.warning("Dados insuficientes para gráfico de entradas")
            return
        
        logger.info("Gerando gráfico: entradas por mês")
        
        plt.figure()
        plt.plot(df_fluxo["mes_label"], df_fluxo["total_entradas"], marker='o', linewidth=2)
        plt.title("Entradas por Mês", fontsize=14, fontweight='bold')
        plt.xlabel("Mês")
        plt.ylabel("Valor (R$)")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        self.salvar_grafico("entradas_por_mes")
    
    def grafico_saidas_por_mes(self, df_fluxo: pd.DataFrame):
        """
        Gera gráfico de linha com saídas por mês.
        
        Args:
            df_fluxo: DataFrame com fluxo mensal.
        """
        if df_fluxo.empty or "total_saidas" not in df_fluxo.columns:
            logger.warning("Dados insuficientes para gráfico de saídas")
            return
        
        logger.info("Gerando gráfico: saídas por mês")
        
        plt.figure()
        plt.plot(df_fluxo["mes_label"], df_fluxo["total_saidas"], marker='o', linewidth=2)
        plt.title("Saídas por Mês", fontsize=14, fontweight='bold')
        plt.xlabel("Mês")
        plt.ylabel("Valor (R$)")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        self.salvar_grafico("saidas_por_mes")
    
    def grafico_resultado_por_mes(self, df_fluxo: pd.DataFrame):
        """
        Gera gráfico de barras com resultado por mês.
        
        Args:
            df_fluxo: DataFrame com fluxo mensal.
        """
        if df_fluxo.empty or "resultado_liquido" not in df_fluxo.columns:
            logger.warning("Dados insuficientes para gráfico de resultado")
            return
        
        logger.info("Gerando gráfico: resultado por mês")
        
        plt.figure()
        cores = ['green' if x >= 0 else 'red' for x in df_fluxo["resultado_liquido"]]
        plt.bar(df_fluxo["mes_label"], df_fluxo["resultado_liquido"], color=cores, alpha=0.7)
        plt.title("Resultado Líquido por Mês", fontsize=14, fontweight='bold')
        plt.xlabel("Mês")
        plt.ylabel("Valor (R$)")
        plt.xticks(rotation=45, ha='right')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.grid(True, alpha=0.3, axis='y')
        
        self.salvar_grafico("resultado_por_mes")
    
    def grafico_top_categorias(self, df_ranking: pd.DataFrame, tipo: str = "saida", top_n: int = 10):
        """
        Gera gráfico de barras com top categorias.
        
        Args:
            df_ranking: DataFrame com ranking de categorias.
            tipo: "entrada" ou "saida"
            top_n: Número de categorias a exibir.
        """
        if df_ranking.empty:
            logger.warning(f"Dados insuficientes para gráfico de top {tipo}s")
            return
        
        logger.info(f"Gerando gráfico: top {top_n} categorias de {tipo}")
        
        df_top = df_ranking.head(top_n)
        coluna_valor = f"total_{tipo}"
        
        plt.figure()
        plt.barh(df_top["categoria"], df_top[coluna_valor], alpha=0.7)
        plt.title(f"Top {top_n} Categorias - {tipo.capitalize()}s", fontsize=14, fontweight='bold')
        plt.xlabel("Valor (R$)")
        plt.ylabel("Categoria")
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
        
        self.salvar_grafico(f"top10_categorias_{tipo}")
    
    def grafico_pareto(self, df_pareto: pd.DataFrame, tipo: str = "saida"):
        """
        Gera gráfico de Pareto (barras + linha acumulada).
        
        Args:
            df_pareto: DataFrame com análise de Pareto.
            tipo: "entrada" ou "saida"
        """
        if df_pareto.empty or "percentual_acumulado" not in df_pareto.columns:
            logger.warning(f"Dados insuficientes para Pareto de {tipo}s")
            return
        
        logger.info(f"Gerando gráfico: Pareto de {tipo}s")
        
        coluna_valor = f"total_{tipo}"
        
        fig, ax1 = plt.subplots()
        
        # Barras
        ax1.bar(df_pareto["categoria"], df_pareto[coluna_valor], alpha=0.7)
        ax1.set_xlabel("Categoria")
        ax1.set_ylabel("Valor (R$)")
        ax1.tick_params(axis='x', rotation=45)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Linha acumulada
        ax2 = ax1.twinx()
        ax2.plot(df_pareto["categoria"], df_pareto["percentual_acumulado"], 
                 color='red', marker='o', linewidth=2, label='% Acumulado')
        ax2.set_ylabel("Percentual Acumulado (%)")
        ax2.set_ylim(0, 110)
        ax2.axhline(y=80, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        
        plt.title(f"Análise de Pareto - {tipo.capitalize()}s por Categoria", 
                  fontsize=14, fontweight='bold')
        
        self.salvar_grafico(f"pareto_{tipo}s_categoria")
    
    def gerar_todos_graficos(self, df_fluxo: pd.DataFrame, 
                            df_ranking_saidas: pd.DataFrame,
                            df_ranking_entradas: pd.DataFrame,
                            df_pareto_saidas: pd.DataFrame):
        """
        Gera todos os gráficos do projeto.
        
        Args:
            df_fluxo: DataFrame com fluxo mensal.
            df_ranking_saidas: Ranking de saídas.
            df_ranking_entradas: Ranking de entradas.
            df_pareto_saidas: Análise de Pareto de saídas.
        """
        logger.info("Iniciando geração de todos os gráficos...")
        
        self.grafico_entradas_por_mes(df_fluxo)
        self.grafico_saidas_por_mes(df_fluxo)
        self.grafico_resultado_por_mes(df_fluxo)
        self.grafico_top_categorias(df_ranking_saidas, "saida")
        self.grafico_top_categorias(df_ranking_entradas, "entrada")
        self.grafico_pareto(df_pareto_saidas, "saida")
        
        logger.info("✓ Todos os gráficos foram gerados")
