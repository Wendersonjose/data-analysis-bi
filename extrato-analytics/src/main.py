"""
Módulo principal para executar toda a análise de extratos bancários.
"""

import logging
import sys
from pathlib import Path

# Importar módulos do projeto
from src.config import PDFS_DIR, OUTPUT_DIR, GRAFICOS_DIR, LOG_FORMAT, LOG_LEVEL
from src.pdf_reader import PDFReader
from src.parser_summary import SummaryParser
from src.parser_transactions import TransactionParser
from src.categorizer import TransactionCategorizer
from src.analytics import DataAnalyzer
from src.export import DataExporter
from src.plots import ChartGenerator


def configurar_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Função principal que executa todo o pipeline de análise."""
    
    configurar_logging()
    logger = logging.getLogger(__name__)
    
    print("\n" + "="*60)
    print("  ANALISE DE EXTRATOS BANCARIOS - ITAU PJ")
    print("="*60 + "\n")
    
    try:
        # 1. LEITURA DOS PDFs
        logger.info("ETAPA 1: Leitura dos arquivos PDF")
        print("-> Lendo arquivos PDF...\n")
        
        reader = PDFReader(PDFS_DIR)
        dados_pdfs = reader.extract_all_pdfs()
        
        if not dados_pdfs:
            logger.error("Nenhum PDF foi processado. Verifique a pasta 'pdfs'.")
            print("\nAVISO: Nenhum PDF encontrado ou processado!")
            print("  Coloque os extratos bancarios em PDF na pasta 'pdfs' e tente novamente.\n")
            return 1
        
        print()
        
        # 2. EXTRACAO DO RESUMO MENSAL
        logger.info("ETAPA 2: Extracao dos resumos mensais")
        print("-> Extraindo resumos mensais...\n")
        
        summary_parser = SummaryParser()
        resumos = summary_parser.extrair_resumos_multiplos(dados_pdfs)
        
        print()
        
        # 3. EXTRACAO DAS TRANSACOES
        logger.info("ETAPA 3: Extracao das transacoes")
        print("-> Extraindo transacoes individuais...\n")
        
        transaction_parser = TransactionParser()
        transacoes = transaction_parser.extrair_transacoes_multiplas(dados_pdfs, resumos)
        
        print()
        
        # 4. CATEGORIZACAO
        logger.info("ETAPA 4: Categorizacao das transacoes")
        print("-> Categorizando transacoes...\n")
        
        categorizer = TransactionCategorizer()
        transacoes = categorizer.categorizar_transacoes(transacoes)
        
        print()
        
        # 5. ANALISES
        logger.info("ETAPA 5: Gerando analises")
        print("-> Realizando analises...\n")
        
        analyzer = DataAnalyzer(resumos, transacoes)
        
        df_fluxo = analyzer.gerar_fluxo_mensal()
        df_indicadores = analyzer.gerar_totais_periodo()
        df_saidas_cat = analyzer.gerar_ranking_categorias("saida")
        df_entradas_cat = analyzer.gerar_ranking_categorias("entrada")
        df_top_saidas = analyzer.gerar_top_descricoes("saida", 50)
        df_top_entradas = analyzer.gerar_top_descricoes("entrada", 50)
        df_pareto = analyzer.gerar_pareto_categorias("saida")
        
        print()
        
        # 6. EXPORTACAO
        logger.info("ETAPA 6: Exportando resultados")
        print("-> Exportando dados...\n")
        
        exporter = DataExporter(OUTPUT_DIR)
        exporter.exportar_analise_completa(
            df_resumos=analyzer.df_resumos,
            df_transacoes=analyzer.df_transacoes,
            df_fluxo=df_fluxo,
            df_saidas_cat=df_saidas_cat,
            df_entradas_cat=df_entradas_cat,
            df_top_saidas=df_top_saidas,
            df_top_entradas=df_top_entradas,
            df_indicadores=df_indicadores
        )
        
        print()
        
        # 7. GERACAO DE GRAFICOS
        logger.info("ETAPA 7: Gerando graficos")
        print("-> Gerando graficos...\n")
        
        chart_gen = ChartGenerator(GRAFICOS_DIR)
        chart_gen.gerar_todos_graficos(
            df_fluxo=df_fluxo,
            df_ranking_saidas=df_saidas_cat,
            df_ranking_entradas=df_entradas_cat,
            df_pareto_saidas=df_pareto
        )
        
        print()
        print("="*60)
        print("  ✓ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print(f"\nResultados salvos em:")
        print(f"   - CSVs e Excel: {OUTPUT_DIR}")
        print(f"   - Graficos PNG: {GRAFICOS_DIR}")
        print()
        
        # Resumo dos resultados
        print("Resumo da analise:")
        print(f"   - PDFs processados: {len(dados_pdfs)}")
        print(f"   - Meses analisados: {len(resumos)}")
        print(f"   - Transacoes extraidas: {len(transacoes)}")
        print(f"   - Categorias identificadas: {len(df_saidas_cat) if not df_saidas_cat.empty else 0}")
        print()
        
        return 0
        
    except Exception as e:
        logger.error(f"Erro durante a execucao: {e}", exc_info=True)
        print(f"\nERRO: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
