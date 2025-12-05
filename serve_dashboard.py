#!/usr/bin/env python3
"""
Servidor HTTP simples para o Dashboard de Telemetria
"""

import http.server
import socketserver
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Muda para o diretório web
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    os.chdir(web_dir)
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("="*60)
        print("🌐 BackupMaster - Dashboard de Telemetria")
        print("="*60)
        print(f"\n✅ Servidor rodando em: http://localhost:{PORT}")
        print(f"📊 Acesse o dashboard no navegador")
        print(f"\n🔐 Senha Admin: backupmaster2025")
        print(f"\nPressione Ctrl+C para parar o servidor\n")
        print("="*60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor encerrado")

if __name__ == "__main__":
    main()
