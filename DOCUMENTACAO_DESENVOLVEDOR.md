# Documentação do Desenvolvedor - Autônomo Pro

Este documento descreve a arquitetura técnica e os padrões utilizados no projeto Django `autonomo`.

## Arquitetura do Sistema
O sistema foi desenvolvido utilizando o framework **Django (v5.1+)**, focado em simplicidade, rápida manutenabilidade e entrega dinâmica de páginas.

### Módulos (Apps)
- `nucleo`: Gerencia o modelo de `UsuarioCustomizado`. Este herda do `AbstractUser` padrão do Django e adiciona o campo de "Perfil/Cargo" (`cargo`) para que no futuro seja possível estipular controles mais finos de permissões (ex: `@login_required` e `@user_passes_test` customizados).
- `clientes`: Gerencia a base de clientes do prestador de serviço.
- `servicos`: Mantém o catálogo de categorias e os serviços prestados baseados em orçamento/preço.
- `contratos`: O core do negócio. Faz o relacionamento *Many-to-Many* com `servicos` e *Foreign-Key* com `clientes`. Adiciona controles de data e hora do evento e status financeiro.
- `dashboard`: App front-end responsável por ler as métricas e compor as telas limpas para o usuário final que não necessite das ferramentas arcaicas do Django Admin.

## Decisões de Frontend
O projeto não utiliza uma API REST robusta (como Django REST Framework) de propósito. A decisão foi manter o MVP extremamente ágil utilizando:
- **Tailwind CSS (via CDN):** Para um estilo minimalista, veloz e componentizado direto nos templates HTML (`dashboard/base.html` e `dashboard/index.html`).
- **HTMX (via CDN):** Incluído por padrão para futuros desenvolvimentos de requisições assíncronas simples (ex: exclusões inline, filtros dinâmicos de tabelas sem recarregar a página).

## Segurança (Credenciais Padrões de Desenvolvimento)
- Superusuário padrão: `admin` / senha: `admin` (Utilizado apenas local via SQLite3).
- O controle de acesso atual da rota raiz (`/dashboard`) está isolado com `@login_required`.
- Para ambiente de produção (Deploy), garanta a substituição do `SECRET_KEY`, de `DEBUG=True` para `False`, e configure variáveis de ambiente (sugere-se utilizar `django-environ`).
