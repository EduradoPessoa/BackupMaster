#!/usr/bin/env python3
"""
Script de teste para debug do BackupMaster
"""

import sys
import traceback

try:
    from backupmaster_gui import main
    main()
except Exception as e:
    print("=" * 60)
    print("ERRO AO EXECUTAR BACKUPMASTER:")
    print("=" * 60)
    print(f"\nTipo: {type(e).__name__}")
    print(f"Mensagem: {str(e)}")
    print("\nTraceback completo:")
    print("-" * 60)
    traceback.print_exc()
    print("=" * 60)
    input("\nPressione ENTER para fechar...")
    sys.exit(1)
