# 💰 Controle Financeiro Pessoal

Aplicação web de controle financeiro pessoal desenvolvida com **Python e Flask**.

O projeto permite que usuários criem uma conta e gerenciem suas próprias receitas e despesas através de um dashboard.

Este projeto foi desenvolvido com o objetivo de praticar desenvolvimento web com Flask, banco de dados, autenticação de usuários e operações CRUD.

## 🚀 Funcionalidades

- Cadastro de usuários
- Login e logout
- Senhas armazenadas utilizando hash
- Sessão de usuário
- Cadastro de transações
- Edição de transações
- Exclusão de transações
- Separação entre entradas e saídas
- Categorias de transações
- Cálculo do saldo
- Total de receitas
- Total de despesas
- Histórico de transações
- Cada usuário possui suas próprias transações

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Werkzeug
- HTML
- CSS
- Jinja2

## 📁 Estrutura do projeto

```text
controle-financeiro-flask/
│
├── app.py
├── models.py
├── README.md
│
├── templates/
│   ├── login.html
│   ├── cadastro.html
│   ├── dashboard.html
│   ├── nova_transacao.html
│   └── editar_transacao.html
│
│
└── instance/
    └── database.db
```

## 🗃️ Banco de dados

A aplicação utiliza **SQLite** juntamente com **Flask-SQLAlchemy**.

O banco possui dois modelos principais:

### Usuário

```text
Usuario
├── id
├── nome
├── email
└── senha
```

### Transação

```text
Transacao
├── id
├── descricao
├── valor
├── data
├── categoria
├── tipo
└── usuario_id
```

Cada transação pertence a um usuário através do campo `usuario_id`.

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/allangdev/controle-financeiro-flask.git
```

Entre na pasta:

```bash
cd controle-financeiro-flask
```

### 2. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
```

Ative:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install flask flask-sqlalchemy
```

### 4. Execute a aplicação

```bash
python app.py
```

A aplicação estará disponível em:

```text
http://127.0.0.1:5001
```

## 🔐 Segurança

As senhas dos usuários não devem ser armazenadas diretamente no banco de dados.

A aplicação utiliza funções de hash de senha do Werkzeug:

```python
generate_password_hash()
check_password_hash()
```

As transações também são associadas ao usuário autenticado, evitando que um usuário acesse ou modifique transações pertencentes a outro usuário.

## 📚 Conceitos praticados

Durante o desenvolvimento deste projeto foram utilizados conceitos como:

- Rotas HTTP com Flask
- Métodos GET e POST
- Templates com Jinja2
- Formulários HTML
- Banco de dados relacional
- ORM com SQLAlchemy
- Operações CRUD
- Relacionamento entre tabelas
- Autenticação
- Sessões
- Hash de senhas
- Validação de dados
- Flash messages

## 🔮 Melhorias futuras

Algumas funcionalidades que podem ser adicionadas futuramente:

- [ ] Filtro de transações por período
- [ ] Gráficos de receitas e despesas
- [ ] Categorias personalizadas
- [ ] Dashboard mensal
- [ ] Metas financeiras
- [ ] Exportação de transações para CSV
- [ ] Migração de SQLite para PostgreSQL
- [ ] Deploy da aplicação

## 👨‍💻 Autor

**Allan Gabriel**

Estudante de Ciência da Computação.

GitHub: `@allangdev`
