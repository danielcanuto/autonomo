import os
import django
import csv
from datetime import datetime

# Configuração do Ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autonomo.settings')
django.setup()

from clientes.models import Cliente
from servicos.models import Servico

def export_clientes():
    # Garantir que o diretório export existe
    os.makedirs('export', exist_ok=True)
    filename = os.path.join('export', f"clientes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Nome', 'Tipo', 'Email', 'Telefone', 'Documento', 'Endereço', 'Criado Em']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for root in Cliente.objects.all():
            writer.writerow({
                'ID': root.id,
                'Nome': root.nome,
                'Tipo': root.get_tipo_pessoa_display(),
                'Email': root.email,
                'Telefone': root.telefone,
                'Documento': root.documento,
                'Endereço': root.endereco,
                'Criado Em': root.criado_em.strftime('%d/%m/%Y %H:%M')
            })
    print(f"✅ Clientes exportados para: {filename}")

def export_servicos():
    # Garantir que o diretório export existe
    os.makedirs('export', exist_ok=True)
    filename = os.path.join('export', f"servicos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Categoria', 'Nome', 'Preço Base (R$)', 'Ativo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for s in Servico.objects.all().select_related('categoria'):
            writer.writerow({
                'ID': s.id,
                'Categoria': s.categoria.nome if s.categoria else "Sem Categoria",
                'Nome': s.nome,
                'Preço Base (R$)': str(s.preco_base),
                'Ativo': "Sim" if s.ativo else "Não"
            })
    print(f"✅ Serviços exportados para: {filename}")

if __name__ == "__main__":
    print("📦 Iniciando exportação de dados...")
    export_clientes()
    export_servicos()
    print("\nConcluído!")
