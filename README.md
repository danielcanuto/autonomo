# Autônomo Pro - ERP para Profissionais Autônomos e MEI

O **Autônomo Pro** é uma plataforma de gestão inteligente desenvolvida em Django, projetada para simplificar a vida do profissional autônomo. O sistema centraliza desde o primeiro contato com o cliente até a entrega do contrato e a declaração de rendimentos para o MEI.

## 🚀 Funcionalidades Principais

### 💰 Ciclo de Vendas (Vendas)
- **Gestão de Clientes**: Cadastro completo com histórico de interações e documentos vinculados.
- **Catálogo de Serviços**: Defina seus serviços com preços base e templates de orçamento.
- **Orçamentos & Propostas**: Gere orçamentos dinâmicos com substituição automática de variáveis.
- **Controle de Contratos**: Transforme orçamentos em contratos ativos com gestão de status e datas.

### ⚙️ Gestão Administrativa (Gerencial)
- **Gestão de Equipe**: Controle de colaboradores com diferentes níveis de acesso (Admin, Gestor, Vendedor, Operador).
- **Parceiros e Fornecedores**: Cadastro de fornecedores para vinculação de custos e insumos.
- **Identidade Visual**: Personalização completa com logo da empresa e dados da Razão Social ou perfil autônomo (CPF).

### 📊 Financeiro e Relatórios
- **Fluxo de Caixa**: Registro automático de entradas (pagamentos) e saídas (custos).
- **Relatório de Rendimentos MEI**: Relatório mensal automatizado que separa receitas de Serviços e Produtos, facilitando a declaração anual (DASN-SIMEI).

## 🛠️ Tecnologias Utilizadas
- **Backend**: Python 3 / Django 5
- **Frontend**: HTML5 / Tailwind CSS (v3) / FontAwesome 6
- **Interatividade**: HTMX
- **Banco de Dados**: SQLite (Desenvolvimento) / PostgreSQL (Recomendado para Produção)

## 📁 Estrutura do Projeto
- `autonomo`: Pasta de configurações globais do projeto Django.
- `nucleo`: Gestão de usuários customizados, permissões e configurações de identidade da empresa.
- `clientes`: Módulo de CRM para gestão de clientes.
- `servicos`: Catálogo de serviços e categorias.
- `orcamentos`: Geração de propostas e fluxos de aprovação.
- `contratos`: Gestão de acordos e vigências.
- `financeiro`: Fluxo de caixa, gestão de fornecedores e relatórios MEI.
- `dashboard`: Painel principal e landing page do sistema.

## ⚙️ Instalação Local

1.  **Clone o repositório**
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # (Windows: venv\Scripts\activate)
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute as migrações:**
    ```bash
    python manage.py migrate
    ```
5.  **Crie seu acesso administrativo:**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

---
*Desenvolvido em conformidade com as necessidades de fotógrafos, pintores, consultores e diversos profissionais prestadores de serviço.*
