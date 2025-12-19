"""
Servidor HTTP simples para visualizar o dashboard de análise.
Uso: python servidor.py
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# Configurações
PORT = 8000
DIRECTORY = Path(__file__).parent / "saida_analise"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        # Adicionar headers para evitar problemas de CORS
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Verificar se a pasta existe
    if not DIRECTORY.exists():
        print(f"ERRO: Pasta '{DIRECTORY}' nao encontrada!")
        print("Execute a analise primeiro com: python -m src.main")
        return
    
    # Verificar se o dashboard existe
    dashboard_path = DIRECTORY / "dashboard.html"
    if not dashboard_path.exists():
        print(f"ERRO: Arquivo '{dashboard_path}' nao encontrado!")
        return
    
    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/dashboard.html"
        
        print("="*60)
        print("  SERVIDOR HTTP - DASHBOARD DE ANALISE")
        print("="*60)
        print(f"\nServidor rodando em: {url}")
        print(f"Pasta: {DIRECTORY}")
        print("\nPressione Ctrl+C para parar o servidor")
        print("="*60)
        print()
        
        # Abrir navegador automaticamente
        try:
            webbrowser.open(url)
            print("Abrindo navegador...")
        except:
            print(f"Abra seu navegador e acesse: {url}")
        
        # Manter servidor rodando
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServidor encerrado.")

if __name__ == "__main__":
    main()
