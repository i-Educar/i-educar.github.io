# Documentação Técnica dos Pacotes i-Educar – Guia de Implantação

**Versão:** 2.10.0  
**Última atualização:** Fevereiro/2025

---

## Sumário

1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Catálogo de Pacotes](#2-catálogo-de-pacotes)
3. [Pré-requisitos Gerais](#3-pré-requisitos-gerais)
4. [Etapas de Implantação por Pacote](#4-etapas-de-implantação-por-pacote)
5. [Integração com Login Único gov.br](#5-integração-com-login-único-govbr)
6. [Comandos Úteis](#6-comandos-úteis)
7. [Solução de Problemas](#7-solução-de-problemas)

---

## 1. Visão Geral da Arquitetura

### 1.1 Composer Plug and Play

O i-Educar usa o plugin **[dex/composer-plug-and-play](https://github.com/edersoares/composer-plug-and-play)** para gerenciar pacotes locais sem alterar o `composer.json` principal.

**Fluxo:**

| Etapa | Descrição |
|-------|-----------|
| 1 | Pacotes ficam em `packages/portabilis/` ou `packages/serventec/` |
| 2 | O plugin gera `packages/plug-and-play.json` e `packages/plug-and-play.lock` |
| 3 | Esses arquivos não são commitados (`.gitignore`) |
| 4 | O `composer.json` raiz permanece limpo |

### 1.2 Estrutura de Diretórios

```
i-educar/
├── packages/
│   ├── DOCUMENTACAO_TECNICA_IMPLANTACAO.md   # Este documento
│   ├── portabilis/           # Pacotes Portábilis
│   │   ├── i-educar-educacenso-package/
│   │   ├── i-educar-reports-package/
│   │   └── i-educar-transport-package/
│   └── serventec/            # Pacotes Serventec
│       ├── i-educar-bis-package/
│       └── i-educar-govbr-login-package/
├── packages/plug-and-play.json   # Configuração (gerado)
└── packages/plug-and-play.lock   # Lock (gerado)
```

---

## 2. Catálogo de Pacotes

| Pacote | Organização | Descrição | Obrigatório |
|--------|-------------|-----------|-------------|
| **i-educar-educacenso-package** | Portabilis | Censo Escolar INEP (exportação/importação) | Recomendado |
| **i-educar-reports-package** | Portabilis | Relatórios em Jasper | Recomendado |
| **i-educar-transport-package** | Portabilis | Transporte Escolar | Opcional |
| **i-educar-bis-package** | Serventec | BI, dashboards, gráficos, Excel | Opcional |
| **i-educar-govbr-login-package** | Serventec | Login via Login Único gov.br (CPF) | Opcional |

---

## 3. Pré-requisitos Gerais

### 3.1 Ambiente

- **PHP:** >= 8.3
- **Laravel:** 12.x
- **PostgreSQL:** 12+
- **Redis:** (para cache/sessions)
- **Composer:** 2.x

### 3.2 Dependências do Sistema

- Extensões PHP: `gd`, `json`, `pdo`, `pgsql`, `zip`
- **Reports:** Java JDK 8+ (para Jasper)
- **Transport:** conforme módulo legado

### 3.3 Permissões

- `storage/` e `bootstrap/cache/` com permissão de escrita
- Usuário do servidor com acesso ao banco de dados

---

## 4. Etapas de Implantação por Pacote

### 4.1 i-educar-educacenso-package

**Objetivo:** Módulo de Censo Escolar INEP – exportação e importação de dados.

#### Etapas resumidas

| # | Etapa | Comando/Ação |
|---|-------|--------------|
| 1 | Clone | `git clone git@github.com:portabilis/i-educar-educacenso-package.git packages/portabilis/i-educar-educacenso-package` |
| 2 | Adicionar | `composer plug-and-play:add portabilis/i-educar-educacenso-package @dev` |
| 3 | Resolver | `composer plug-and-play` |
| 4 | Migrations | `php artisan migrate` |
| 5 | Validar | Acessar menu Educacenso |

---

### 4.2 i-educar-reports-package

**Objetivo:** Geração de relatórios em Jasper (.jrxml).

#### Etapas resumidas

| # | Etapa | Comando/Ação |
|---|-------|--------------|
| 1 | Clone | `git clone git@github.com:portabilis/i-educar-reports-package.git packages/portabilis/i-educar-reports-package` |
| 2 | Adicionar | `composer plug-and-play:add portabilis/i-educar-reports-package @dev` |
| 3 | Resolver | `composer plug-and-play` |
| 4 | Migrations | `php artisan migrate` |
| 5 | Publicar assets | `php artisan vendor:publish --tag=reports-assets` |
| 6 | Validar | Gerar relatório de teste |

---

### 4.3 i-educar-transport-package

**Objetivo:** Módulo de Transporte Escolar.

#### Etapas resumidas

| # | Etapa | Comando/Ação |
|---|-------|--------------|
| 1 | Clone | `git clone git@github.com:portabilis/i-educar-transport-package.git packages/portabilis/i-educar-transport-package` |
| 2 | Adicionar | `composer plug-and-play:add portabilis/i-educar-transport-package @dev` |
| 3 | Resolver | `composer plug-and-play` |
| 4 | Migrations | `php artisan migrate` |
| 5 | Permissões | Atribuir permissões de transporte aos tipos de usuário |
| 6 | Validar | Acessar menus de transporte |

---

### 4.4 i-educar-bis-package (BI / Power BI)

**Objetivo:** Dashboards, gráficos e relatórios analíticos (Chart.js, Excel).

#### Etapas resumidas

| # | Etapa | Comando/Ação |
|---|-------|--------------|
| 1 | Clone | `git clone git@github.com:serventecieducar/i-educar-powerbi-package.git packages/serventec/i-educar-bis-package` |
| 2 | Adicionar | `composer plug-and-play:add serventec/i-educar-bis-package @dev` |
| 3 | Resolver | `composer plug-and-play` |
| 4 | Migrations | `php artisan migrate` |
| 5 | Publicar assets | `php artisan vendor:publish --tag=bis-assets` |
| 6 | Cache | `php artisan cache:clear` |
| 7 | Permissões | Configurações > Permissões > Tipos de usuário (menus BI) |
| 8 | Validar | Acessar Escola > BI |

---

### 4.5 i-educar-govbr-login-package

**Objetivo:** Login via Login Único gov.br, com vinculação de usuários por CPF.

**Etapas detalhadas:** Ver [seção 5 – Integração com Login Único gov.br](#5-integração-com-login-único-govbr).

---

## 5. Integração com Login Único gov.br

Esta seção detalha as etapas para implantar o pacote **i-educar-govbr-login-package** e integrar o i-Educar ao [Login Único gov.br](https://acesso.gov.br).

### 5.1 Visão Geral

O pacote permite que funcionários autentiquem no i-Educar usando suas credenciais gov.br. A vinculação é feita pelo **CPF**: o gov.br retorna o CPF do cidadão e o sistema localiza o usuário correspondente em `cadastro.fisica` → `portal.funcionario` → `pmieducar.usuario`.

### 5.2 Pré-requisitos

| Item | Descrição |
|------|-----------|
| Credenciais gov.br | `client_id` e `client_secret` fornecidos após solicitação |
| HTTPS | Obrigatório em produção (exigência do gov.br) |
| Cadastro | Funcionários com CPF em `cadastro.fisica` e usuário ativo |

### 5.3 Etapas de Integração

#### Etapa 1: Solicitar integração no gov.br

1. Acesse [acesso.gov.br/roteiro-tecnico](https://acesso.gov.br/roteiro-tecnico/)
2. Siga o [passo a passo de integração](https://acesso.gov.br/roteiro-tecnico/iniciarintegracao.html)
3. Solicite as credenciais (client_id, client_secret)
4. Informe a **URL de callback** que será configurada: `https://seu-dominio.gov.br/auth/govbr/callback` (ou equivalente conforme seu domínio)

> **Nota:** O gov.br exige que o domínio da aplicação esteja cadastrado. Para desenvolvimento local, use `GOVBR_ENVIRONMENT=staging` e domínios de homologação (ex.: `local.minha_aplicacao.gov.br`).

#### Etapa 2: Instalar o pacote

Na raiz do i-Educar:

```bash
# Clone
git clone git@github.com:serventecieducar/i-educar-govbr-login-package.git packages/serventec/i-educar-govbr-login-package

# Adicionar e resolver dependências
composer plug-and-play:add serventec/i-educar-govbr-login-package @dev
composer plug-and-play
```

**Com Docker:**

```bash
docker compose exec php composer plug-and-play:add serventec/i-educar-govbr-login-package @dev
docker compose exec php composer plug-and-play
```

#### Etapa 3: Configurar variáveis de ambiente

Adicione ao `.env`:

```env
# Gov.br – Login Único
GOVBR_LOGIN_ENABLED=true
GOVBR_CLIENT_ID=seu_client_id_recebido_do_govbr
GOVBR_CLIENT_SECRET=seu_client_secret_recebido_do_govbr
GOVBR_REDIRECT_URI="${APP_URL}/auth/govbr/callback"
GOVBR_ENVIRONMENT=production
GOVBR_LOGIN_LABEL="Entrar com GOV.BR"
```

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `GOVBR_CLIENT_ID` | Sim | Chave fornecida pelo gov.br |
| `GOVBR_CLIENT_SECRET` | Sim | Segredo fornecido pelo gov.br |
| `GOVBR_REDIRECT_URI` | Sim | URL de retorno após autenticação (deve ser HTTPS em produção) |
| `GOVBR_ENVIRONMENT` | Sim | `production` ou `staging` |
| `GOVBR_LOGIN_ENABLED` | Não | `true` para exibir botão (padrão: `true`) |
| `GOVBR_LOGIN_LABEL` | Não | Texto do botão (padrão: "Entrar com GOV.BR") |

#### Etapa 4: Registrar URL no painel gov.br

1. Acesse o painel de configuração da sua aplicação no gov.br
2. Cadastre a **URL de redirecionamento (callback)** exatamente como definida em `GOVBR_REDIRECT_URI`
3. Exemplo: `https://ieducar.seudominio.gov.br/auth/govbr/callback`
4. Em ambiente de homologação, cadastre a URL correspondente ao `staging`

#### Etapa 5: Preparar cadastro de usuários

Para que um funcionário use o Login Único:

1. **Pessoa física** cadastrada em `cadastro.pessoa` e `cadastro.fisica` com **CPF** válido
2. **Funcionário** em `portal.funcionario` com `ref_cod_pessoa_fj` = idpes da pessoa
3. **Usuário** em `pmieducar.usuario` com `cod_usuario` = idpes (ativo)

O fluxo interno: gov.br retorna CPF → busca em `cadastro.fisica` → obtém `idpes` → localiza usuário em `pmieducar.usuario`.

#### Etapa 6: Validar integração

1. Acesse a tela de login do i-Educar
2. Verifique se o botão **"Entrar com GOV.BR"** aparece (abaixo do formulário ou ao lado do SSO existente)
3. Clique no botão → deve redirecionar para gov.br
4. Faça login no gov.br com um CPF cadastrado como funcionário
5. Após autorização, deve retornar ao i-Educar já autenticado

### 5.4 Ambiente de Homologação (staging)

Para testes antes da produção:

```env
GOVBR_ENVIRONMENT=staging
```

O pacote usará `https://sso.staging.acesso.gov.br` em vez do ambiente de produção.

### 5.5 Rotas Expostas

| Rota | Método | Descrição |
|------|--------|-----------|
| `/auth/govbr/redirect` | GET | Redireciona o usuário para o gov.br |
| `/auth/govbr/callback` | GET | Recebe o retorno do gov.br e efetua o login |

### 5.6 Fluxo Técnico (OAuth2 + PKCE)

1. Usuário clica em "Entrar com GOV.BR"
2. Aplicação redireciona para `https://sso.acesso.gov.br/authorize` com `client_id`, `scope`, `redirect_uri`, `state`, `code_challenge` (PKCE)
3. Usuário autentica no gov.br
4. gov.br redireciona para `GOVBR_REDIRECT_URI` com `code` e `state`
5. Aplicação troca `code` por token e obtém dados do usuário (userinfo)
6. Pacote extrai CPF do userinfo, busca em `cadastro.fisica`, localiza usuário e executa `Auth::login($user)`

### 5.7 Troubleshooting Login Único

| Problema | Solução |
|----------|---------|
| Botão não aparece | Verificar `GOVBR_LOGIN_ENABLED=true` e `GOVBR_CLIENT_ID` definido |
| "CPF não encontrado" | Confirmar CPF em `cadastro.fisica` e vínculo com `portal.funcionario` e `pmieducar.usuario` |
| Erro de redirect_uri | A URL em `GOVBR_REDIRECT_URI` deve ser idêntica à cadastrada no gov.br |
| Erro em staging | Usar `GOVBR_ENVIRONMENT=staging` e domínio de homologação cadastrado |

---

## 6. Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `composer plug-and-play` | Resolve e instala pacotes plug-and-play |
| `composer plug-and-play:add vendor/package @dev` | Adiciona pacote à configuração |
| `composer plug-and-play:update` | Atualiza pacotes plug-and-play |
| `composer plug-and-play:init` | Inicializa estrutura |
| `composer plug-and-play:reset` | Remove arquivos gerados |
| `php artisan migrate` | Executa migrations de todos os pacotes |
| `php artisan cache:clear` | Limpa cache (recomendado após alterar menus) |
| `php artisan vendor:publish --tag=<tag>` | Publica assets de pacotes |

---

## 7. Solução de Problemas

### 7.1 Pacote não carrega após instalação

- Verificar se `packages/<org>/<pacote>/` existe e contém `composer.json`
- Executar `composer plug-and-play` novamente
- Executar `composer dump-autoload`

### 7.2 Migrations não encontradas

- Confirmar que o pacote possui `database/migrations/`
- O ServiceProvider deve chamar `loadMigrationsFrom()` no `boot()`
- Executar `php artisan migrate` na raiz do i-Educar

### 7.3 Menu não aparece

- Executar `php artisan cache:clear`
- Verificar permissões em Configurações > Permissões > Tipos de usuário
- Confirmar que o pacote registra itens de menu na migration ou no Provider

### 7.4 Erro "Class not found" em pacote

- Verificar namespace e PSR-4 no `composer.json` do pacote
- Executar `composer dump-autoload` na raiz
- Reiniciar servidor PHP (php-fpm, artisan serve)

### 7.5 Gov.br: "CPF não encontrado"

- Garantir que o funcionário tenha CPF em `cadastro.fisica`
- CPF deve estar normalizado (apenas dígitos, sem pontos/traços)
- Usuário deve estar ativo em `pmieducar.usuario`

### 7.6 BI: Gráficos não carregam

- Verificar se Chart.js está carregado (CDN ou bundle)
- Conferir permissões do usuário para os menus BI
- Limpar cache do navegador

---

## Referências

- [PACOTES_E_FLUXO_CRIACAO.md](../docs/PACOTES_E_FLUXO_CRIACAO.md) – Criar novo pacote
- [INSTALL.md](../INSTALL.md) – Instalação do i-Educar
- [UPGRADE.md](../UPGRADE.md) – Atualização
- [Composer Plug and Play](https://github.com/edersoares/composer-plug-and-play)
- [Login Único gov.br – Roteiro de Integração](https://acesso.gov.br/roteiro-tecnico/)
- [Login Único gov.br – Passo a passo](https://acesso.gov.br/roteiro-tecnico/iniciarintegracao.html)
- [BI – Guia de instalação](../docs/BI_PACOTE_INSTALACAO.md)
