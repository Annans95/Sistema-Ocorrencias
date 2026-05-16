# 🏢 Sistema de Registro de Ocorrências Internas

![CI](https://github.com/Annans95/Sistema-Ocorrencias/actions/workflows/ci.yml/badge.svg)

**Deploy:** [https://sistema-ocorrencias-web.onrender.com](https://sistema-ocorrencias-web.onrender.com)

**Versão atual:** 1.1.0

## 📌 Descrição do Problema

Em ambientes corporativos, é comum que problemas internos, como falhas de TI, manutenção e demandas operacionais, sejam registrados de forma desorganizada. Muitas vezes essas ocorrências ficam espalhadas em mensagens informais, sem acompanhamento adequado, o que pode gerar perda de informações, falta de priorização e dificuldade no controle das demandas.

## 💡 Proposta da Solução

Este projeto propõe um sistema simples de registro de ocorrências internas, permitindo cadastrar, visualizar e acompanhar o status de problemas dentro de uma organização. A aplicação simula um sistema de help desk utilizado em empresas, organizando as demandas de forma estruturada.

O sistema possui três formas de uso:

- **CLI:** versão local em linha de comando, voltada para uso simples e offline.
- **GUI:** versão local com interface gráfica em CustomTkinter.
- **Web:** versão publicada online, com gerenciamento de equipamentos, histórico de ocorrências por patrimônio e QR Code integrado a uma API pública.

## 🎯 Público-Alvo

- Pequenas empresas
- Equipes internas de TI, manutenção, RH e operações
- Pessoas que desejam organizar demandas internas de forma simples

## ⚙️ Funcionalidades Principais

### CLI

- Criar ocorrências
- Listar ocorrências cadastradas
- Atualizar status das ocorrências: aberta, em andamento ou resolvida
- Ver detalhes completos de uma ocorrência
- Excluir ocorrências
- Cadastrar e gerenciar equipamentos
- Vincular ocorrências a equipamentos
- Visualizar histórico de ocorrências por equipamento

### GUI Local

- Criar ocorrências por interface gráfica
- Visualizar ocorrências em cards organizados por status
- Ver detalhes de uma ocorrência
- Atualizar status
- Excluir ocorrências
- Cadastrar e gerenciar equipamentos
- Vincular ocorrências a equipamentos
- Visualizar histórico de ocorrências por equipamento

### Web

- Criar, listar, editar e excluir ocorrências
- Cadastrar e gerenciar equipamentos
- Vincular ocorrências a equipamentos
- Visualizar histórico de ocorrências por equipamento
- Gerar QR Codes para acesso rápido ao histórico dos equipamentos
- Consome API pública externa para gerar QR Codes
- Acessar a aplicação por link público via deploy no Render


## 🤝 Integração com API Pública

A versão web utiliza a API pública **QR Server API** para gerar QR Codes dos equipamentos:

[https://api.qrserver.com/v1/create-qr-code/](https://api.qrserver.com/v1/create-qr-code/)

Cada QR Code aponta para uma rota pública da aplicação web. Ao acessar o link, o sistema abre o histórico do equipamento correspondente, facilitando a consulta de ocorrências por patrimônio e a criação de uma nova ocorrência.


## 🛠️ Tecnologias Utilizadas

- Python 3
- Flask
- CustomTkinter
- Pytest
- Ruff
- Gunicorn
- Render
- Git e GitHub
- GitHub Actions

## 🖼️ Interface Web do Sistema

### Tela principal

![Tela principal](<docs/tela principal web - sistema de ocorrencias.png>)

### Tela de Equipamentos

![Tela de Equipamentos](<docs/Tela de equipamentos 2- sistema de ocorrencia.png>)

### Modal do equipamento

![Modal do equipamento](<docs/Modal do equipamento - sistema de ocorrencias.png>)


## 📦 Instalação

Antes de começar, você precisa ter:

- Python 3 instalado (recomendado: 3.10 ou superior)
- Uma IDE ou editor de código (VS Code, PyCharm ou similar)

### 1. Clone o repositório

```bash
git clone https://github.com/Annans95/Sistema-Ocorrencias.git
cd Sistema-Ocorrencias
```
Ou baixe o ZIP diretamente pelo GitHub e extraia os arquivos.

### 2. Instale as dependências
Abra o terminal na pasta do projeto e execute:
```bash
pip install -r requirements.txt
```
💡 Dica: Você pode criar um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv

#Windows
venv\Scripts\activate 
#Linux/Mac
source venv/bin/activate
```


## ▶️ Execução

### Interface CLI

```bash
python src/main.py
```

### Interface Desktop (GUI Local)

```bash
python src/ui/app.py
```

### Interface Web Local

```bash
python src/web/app.py
```

Depois, acesse:

```text
http://127.0.0.1:5003
```
As interfaces CLI, GUI e Web compartilham o arquivo `ocorrencias.json` para persistência local dos dados.

## 🧪 Testes Automatizados

Para executar os testes:

```bash
pytest
```

Os testes cobrem:

- fluxo principal de ocorrências;
- criação, atualização, remoção e persistência de equipamentos;
- integração web com a API pública de QR Code, validando a URL gerada para o serviço externo.

## 🧹 Lint

Para verificar a qualidade do código:

```bash
ruff check .
```

## 🚀 Deploy

A aplicação web está publicada no Render:

[https://sistema-ocorrencias-web.onrender.com](https://sistema-ocorrencias-web.onrender.com)

Configuração usada no Render:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn src.web.app:app
```

## 🔢 Versionamento

- **1.0.0:** primeira entrega estável, com estrutura inicial, CLI, GUI local, testes e CI.
- **1.1.0:** entrega intermediária, com interface web, equipamentos, QR Code, integração com API pública, testes de integração e deploy.

## 👩‍💻 Autora

Anna Nicolly da Silva

## 🔗 Repositório

[Sistema de Ocorrências](https://github.com/Annans95/Sistema-Ocorrencias)
