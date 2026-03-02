import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autonomo.settings')
django.setup()

def hard_reset():
    print("🚀 Iniciando HARD RESET de Orçamentos e Contratos...")
    
    with connection.cursor() as cursor:
        # 1. Limpar histórico de migrações para destravar o Django
        print("- Limpando histórico de migrações...")
        cursor.execute("DELETE FROM django_migrations WHERE app IN ('orcamentos', 'contratos')")
        
        # 2. Dropar tabelas (ordem inversa de dependência)
        print("- Removendo tabelas antigas...")
        tables_to_drop = [
            'contratos_pagamento',
            'orcamentos_orcamento_servicos', # Tabela ManyToMany do Django
            'orcamentos_orcamento',
            'contratos_contrato_servicos',
            'contratos_contrato'
        ]
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  [OK] Tabela {table} removida")
            except Exception as e:
                print(f"  [!] Erro ao remover {table}: {e}")

    # 3. Limpar movimentações financeiras relacionadas
    from financeiro.models import MovimentacaoCaixa
    print("- Limpando movimentações de caixa de clientes...")
    MovimentacaoCaixa.objects.filter(categoria='PAGAMENTO_CLIENTE').delete()

    print("\n✅ Estrutura limpa!")
    print("\nPRÓXIMOS PASSOS (Execute no terminal):")
    print("1. python3 manage.py makemigrations orcamentos contratos")
    print("2. python3 manage.py migrate")
    print("\nIsso recriará as tabelas corretamente e sem erros de histórico.")

if __name__ == "__main__":
    hard_reset()
