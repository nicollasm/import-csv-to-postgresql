# Importar CSV para PostgreSQL

Este projeto é um script Python que permite ao usuário interagir com um banco de dados PostgreSQL e exportar os dados de uma tabela selecionada para um arquivo CSV.

## Pré-requisitos

- Python 3.7 ou superior
- PostgreSQL 10 ou superior
- Bibliotecas Python: tkinter, psycopg2, pandas e configparser

## Instalação

1. Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/nicollasm/import-csv-to-postgresql.git
```

2. Navegue até o diretório do projeto:

```bash
cd import-csv-to-postgresql
```

3. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Configuração

1. Copie o arquivo `config.ini.default` para `config.ini`:

```bash
cp config.ini.default config.ini
```

2. Preencha o arquivo `config.ini` com as informações do seu banco de dados PostgreSQL:

```ini
[DATABASE]
host = seu_host
dbname = seu_nome_do_banco_de_dados
user = seu_usuário
password = sua_senha
```

## Execução

Execute o script `main.py`:

```bash
python main.py
```

Isso abrirá uma interface gráfica onde você pode inserir as informações do seu banco de dados e interagir com ele.

## Funcionalidades

- Salvar Configurações: Salva as informações do banco de dados inseridas nos campos de entrada para o arquivo `config.ini`.
- Conectar: Tenta conectar ao banco de dados PostgreSQL com as informações inseridas.
- Testar Conexão: Verifica se a conexão com o banco de dados PostgreSQL é bem-sucedida.
- Selecione a tabela: Depois de conectado, você pode selecionar uma tabela do banco de dados a partir de um menu suspenso.
- Selecionar campos: Abre uma nova janela onde você pode selecionar quais campos da tabela deseja exportar para o CSV.
- Exportar CSV: Exporta os dados da tabela selecionada (e campos selecionados, se aplicável) para um arquivo CSV.
