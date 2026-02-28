# Autônomo - Sistema de Controle de Clientes e Contratos

Um sistema web em Django desenvolvido para gerenciar clientes e contratos, criado inicialmente para fotógrafos, mas estruturado de forma flexível para atender qualquer trabalhador autônomo.

## Funcionalidades Planejadas

- **Gestão de Clientes:** Cadastro completo com nome, e-mail, telefone, CPF/CNPJ e endereço.
- **Catálogo de Serviços:** Criação de categorias e listagem de serviços oferecidos pelo profissional, com valores base.
- **Gestão de Contratos:** Vinculação de um cliente a um serviço, com definição de valor final, datas de vigência e status do contrato (Rascunho, Ativo, Concluído, Cancelado).

## Como executar o projeto localmente

1. Crie e ative um ambiente virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3. Execute as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```
4. Crie um superusuário para acessar o painel administrativo:
    ```bash
    python manage.py createsuperuser
    ```
5. Inicie o servidor:
    ```bash
    python manage.py runserver
    ```

## Estrutura do Projeto

- `nucleo`: App central responsável pelo modelo base de usuário e configurações gerais.
- `clientes`: Módulo dedicado à gestão das informações dos clientes.
- `servicos`: Módulo para gerenciar o catálogo de categorias e serviços.
- `contratos`: Módulo para gerir os acordos de prestação de serviços entre o autônomo e o cliente.
