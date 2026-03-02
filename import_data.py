import os
import django
import csv
import glob
from decimal import Decimal

# Configuração do Ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autonomo.settings')
django.setup()

from clientes.models import Cliente
from servicos.models import Servico, Categoria

def find_latest_file(pattern):
    files = glob.glob(os.path.join('export', pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def import_servicos():
    filename = find_latest_file('servicos_export_*.csv')
    if not filename:
        print("⚠️ Nenhum arquivo de exportação de serviços encontrado em 'export/'.")
        return

    print(f"📥 Importando serviços de: {filename}")
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            # 1. Garantir categoria
            nome_cat = row['Categoria']
            categoria = None
            if nome_cat != "Sem Categoria":
                categoria, _ = Categoria.objects.get_or_create(nome=nome_cat)
            
            # 2. Criar ou Atualizar serviço
            servico, created = Servico.objects.update_or_create(
                nome=row['Nome'],
                defaults={
                    'categoria': categoria,
                    'preco_base': Decimal(row['Preço Base (R$)']),
                    'ativo': row['Ativo'] == 'Sim'
                }
            )
            count += 1
            status = "Criado" if created else "Atualizado"
            print(f"  - [{status}] {servico.nome}")
    
    print(f"✅ total de {count} serviços processados.")

def import_clientes():
    filename = find_latest_file('clientes_export_*.csv')
    if not filename:
        print("⚠️ Nenhum arquivo de exportação de clientes encontrado em 'export/'.")
        return

    print(f"📥 Importando clientes de: {filename}")
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            # Tenta mapear o tipo de volta para a sigla
            tipo_display = row['Tipo']
            tipo_sigla = 'PF' if 'Física' in tipo_display else 'PJ'
            
            cliente, created = Cliente.objects.update_or_create(
                documento=row['Documento'],
                defaults={
                    'nome': row['Nome'],
                    'tipo_pessoa': tipo_sigla,
                    'email': row['Email'],
                    'telefone': row['Telefone'],
                    'endereco': row['Endereço']
                }
            )
            count += 1
            status = "Criado" if created else "Atualizado"
            print(f"  - [{status}] {cliente.nome}")
    
    print(f"✅ Total de {count} clientes processados.")

if __name__ == "__main__":
    print("🔄 Iniciando alimentação do banco de dados...")
    import_servicos()
    import_clientes()
    print("\nAlimentação concluída!")
