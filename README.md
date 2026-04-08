# 🏢 Sistema de Registro de Ocorrências Internas

![CI](https://github.com/Annans95/Sistema-Ocorrencias/actions/workflows/ci.yml/badge.svg)

## 📌 Descrição do Problema
Em ambientes corporativos, é comum que problemas internos (como falhas de TI, manutenção, demandas operacionais) sejam registrados de forma desorganizada, muitas vezes em mensagens informais ou sem acompanhamento adequado. Isso pode gerar perda de informações, falta de priorização e dificuldade no controle das demandas.

---

## 💡 Proposta da Solução
Este projeto propõe um sistema simples de registro de ocorrências internas, permitindo cadastrar, visualizar e acompanhar o status de problemas dentro de uma organização. A aplicação simula um sistema de help desk utilizado em empresas, organizando as demandas de forma estruturada.

O projeto pode ser usado de duas formas:
- **CLI**: interface em linha de comando para operações rápidas
- **GUI**: interface gráfica com CustomTkinter para uma experiência visual mais amigável

---

## 🎯 Público-Alvo
- Pequenas empresas
- Equipes internas (TI, manutenção, RH)
- Pessoas que desejam organizar demandas internas de forma simples

---

## ⚙️ Funcionalidades Principais
- **CLI**
	- Criar ocorrências
	- Listar ocorrências cadastradas de forma resumida
	- Atualizar status das ocorrências (aberta, em andamento, resolvida)
	- Ver detalhes completos de uma ocorrência
	- Excluir ocorrências

- **GUI**
	- Criar ocorrências pelo formulário lateral
	- Visualizar ocorrências em cards organizados por status
	- Ver detalhes de uma ocorrência em uma janela dedicada
	- Atualizar o status para frente ou para trás
	- Excluir ocorrências
	- Persistir os dados automaticamente em arquivo JSON

---

## 🛠️ Tecnologias Utilizadas
- Python 3
- CustomTkinter
- Pytest (testes automatizados)
- Ruff (linting/análise estática)
- Git e GitHub

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/Annans95/Sistema-Ocorrencias.git
cd Sistema-Ocorrencias
```
Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
Instale as dependências:
```bash
pip install -r requirements.txt
```
---

## ▶️ Execução
Com o ambiente virtual ativado, você pode usar qualquer uma das interfaces abaixo:

### CLI (linha de comando)
```bash
python src/main.py
```

### GUI (interface gráfica)
```bash
python src/ui/app.py
```

As duas interfaces usam o mesmo arquivo de persistência: `ocorrencias.json` na raiz do projeto.
Ou seja, uma ocorrência criada pela CLI aparece na GUI (e vice-versa).

---

## 🧪 Testes Automatizados
Para executar os testes:
```bash
pytest
```
---

## 🧹 Lint (Análise Estática)
Para verificar a qualidade do código:
```bash
ruff check .
```
Lint executado utilizando Ruff.
Resultado: nenhum problema encontrado (all checks passed).

---

## 🔢 Versionamento
Versão atual: 1.0.0

---

## 👩‍💻 Autora
Anna Nicolly da Silva

---

🔗 Repositório: https://github.com/Annans95/Sistema-Ocorrencias
