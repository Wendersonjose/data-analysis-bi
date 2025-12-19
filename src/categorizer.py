"""
Categorizador automático de transações bancárias.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class TransactionCategorizer:
    """Classe para categorizar transações automaticamente."""
    
    def __init__(self):
        """Inicializa o categorizador com as regras."""
        self.categorias = {
            "Fornecedores": [
                "sispag fornecedor", "fornecedor", "sispag",
            ],
            "Tributos/Boletos": [
                "trib", "cod barras", "codigo de barras", "trib municipal",
                "tributo", "boleto", "das", "darf", "gps", "inss"
            ],
            "PIX": [
                "pix qrs", "pix transf", "pix", "qr code"
            ],
            "Cartões": [
                "rede visa", "rede mast", "rede elo", "amex",
                "visa", "master", "mastercard", "american express",
                "cartao", "cartão", "adquirencia"
            ],
            "Tarifas Bancárias": [
                "tar pix", "tar ", "tarifa", "plano adapt",
                "pacote servicos", "pacote serviços", "manutencao",
                "manutenção", "anuidade"
            ],
            "Débito Automático": [
                "business", "debito automatico", "débito automático",
                "deb autom", "deb aut"
            ],
            "Saques": [
                "saque", "banco24h", "banco 24h", "saq"
            ],
            "Depósitos": [
                "dep din", "dep disp", "c dep cheque", "deposito",
                "depósito", "cheque depositado"
            ],
            "Aplicações/Resgates": [
                "aplic aut mais", "apl", "res", "rend pago",
                "aplicacao", "aplicação", "resgate", "rendimento",
                "investimento", "cdb", "lci", "lca"
            ],
            "Transferências": [
                "transf", "ted", "doc", "transferencia", "transferência"
            ],
            "Recebimentos": [
                "recebimento", "credito", "crédito", "receb"
            ],
        }
    
    def categorizar(self, descricao: str) -> str:
        """
        Categoriza uma transação baseada na descrição.
        
        Args:
            descricao: Descrição da transação.
            
        Returns:
            Nome da categoria.
        """
        if not descricao:
            return "Outros"
        
        descricao_lower = descricao.lower().strip()
        
        # Verificar cada categoria
        for categoria, palavras_chave in self.categorias.items():
            for palavra in palavras_chave:
                if palavra in descricao_lower:
                    return categoria
        
        return "Outros"
    
    def categorizar_transacoes(self, transacoes: List[Dict]) -> List[Dict]:
        """
        Adiciona categoria a cada transação.
        
        Args:
            transacoes: Lista de transações.
            
        Returns:
            Lista de transações com categoria adicionada.
        """
        logger.info(f"Categorizando {len(transacoes)} transações...")
        
        for transacao in transacoes:
            descricao = transacao.get("descricao", "")
            transacao["categoria"] = self.categorizar(descricao)
        
        # Estatísticas de categorização
        categorias_unicas = set(t["categoria"] for t in transacoes)
        logger.info(f"✓ Transações categorizadas em {len(categorias_unicas)} categorias")
        
        return transacoes
    
    def obter_estatisticas_categorias(self, transacoes: List[Dict]) -> Dict[str, int]:
        """
        Retorna estatísticas de distribuição por categoria.
        
        Args:
            transacoes: Lista de transações categorizadas.
            
        Returns:
            Dicionário com contagem por categoria.
        """
        stats = {}
        for transacao in transacoes:
            categoria = transacao.get("categoria", "Outros")
            stats[categoria] = stats.get(categoria, 0) + 1
        
        return stats
