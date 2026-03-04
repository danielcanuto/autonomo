# Autônomo Pro - ERP para Profissionais Autônomos e MEI

O **Autônomo Pro** é uma plataforma de gestão inteligente desenvolvida em Django, projetada para profissionais que buscam excelência operacional e visual. O sistema centraliza o ciclo completo de serviços e produtos customizados, com foco em performance e UX "Premium".

## 🚀 Funcionalidades Principais (2025-READY)

### 💎 Design System & UX
- **Design Premium**: Interface baseada em **Tailwind CSS v4** e **OKLCH Design Tokens** para fidelidade cromática e harmonia visual.
- **Glassmorphism & Micro-interações**: Efeitos de transparência e transições suaves para uma experiência fluida.
- **Dashboard Unificado**: Visão 360º com agenda integrada de contratos e entregas, além de controle consolidado de recebíveis.

### 💰 Ciclo de Vendas e CRM
- **CRM Completo**: Histórico de clientes e documentos vinculados.
- **Vendas Dinâmicas**: Orçamentos que se transformam em contratos em um clique.
- **Controle de Recebíveis**: Gestão granular de pagamentos pendentes, parciais e finalizados.

### 🏄‍♂️ Módulo de Encomendas Customizadas (Ex: Surf)
- **Centro de Ação (Workflow)**: Gerenciamento rápido de produção (Fila -> Produção -> Entrega) diretamente na ficha.
- **Painel Financeiro Dinâmico**: Barra de progresso de pagamentos e cálculo automático de saldo devedor.
- **Ficha Técnica Avançada**: Especificações precisas, pintura artística e suporte a arquivos de Shape 3D.

### ⚙️ Gestão Administrativa e Fiscal
- **Controle de Equipe**: Níveis de acesso flexíveis (Admin, Gestor, Vendedor, Operador).
- **Relatório MEI Automatizado**: Separação de rendimentos para facilitar a declaração anual (DASN-SIMEI).

## 🛠️ Tecnologias Utilizadas
- **Backend**: Python 3 / Django 5
- **Frontend**: Tailwind CSS v4, FontAwesome 6, Google Fonts (Inter/Outfit)
- **Tooling**: Node.js, npm, @tailwindcss/cli
- **Banco de Dados**: SQLite (Desenvolvimento) / PostgreSQL (Produção)

## ⚙️ Instalação Local

1.  **Clone o repositório**
2.  **Ambiente Virtual:**
    ```bash
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Frontend (Tailwind v4):**
    ```bash
    npm install
    npm run build
    ```
4.  **Django:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

---
*Redefinindo os padrões de gestão para o profissional moderno.*
