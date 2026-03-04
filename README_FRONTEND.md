# Configuração do Frontend (Tailwind v4)

Como estamos elevando o projeto para o **Padrão 2025**, agora temos uma camada de build para o CSS. Isso nos permite usar Design Tokens reais e OKLCH para cores.

## Primeiros Passos

⚠️ **Nota:** Como não consegui rodar o `npm install` diretamente no seu ambiente (limitação técnica temporária), por favor execute os comandos abaixo no seu terminal WSL dentro da pasta `autonomo`:

1. **Instalar dependências:**
   ```bash
   npm install
   ```

2. **Iniciar o modo Watch (Desenvolvimento):**
   ```bash
   npm run dev
   ```
   *Isso vai gerar o arquivo `static/css/output.css` e monitorar mudanças no seu HTML.*

3. **Gerar Versão de Produção:**
   ```bash
   npm run build
   ```

## O que mudou?

- **Cores Semânticas:** Agora usamos `text-primary` em vez de `text-indigo-600`. Se você quiser mudar a cor da marca, basta alterar no arquivo `static/css/input.css` dentro do bloco `@theme`.
- **Acessibilidade Nativa:** O novo sistema já configura o foco (`focus-visible`) de forma profissional e acessível por padrão.
- **Formatação Automática:** O Prettier agora organiza suas classes do Tailwind automaticamente ao salvar (se você tiver a extensão instalada no VS Code).
