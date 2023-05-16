import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from sqlalchemy import create_engine
import pandas as pd

root = tk.Tk()


# Função para conectar ao banco de dados
def connect_db():
    try:
        conn = psycopg2.connect(
            host=host_entry.get(),
            database=database_entry.get(),
            user=user_entry.get(),
            password=password_entry.get()
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível conectar ao banco de dados: {e}")


# Função para testar a conexão com o banco de dados
def test_connection():
    conn = connect_db()
    if conn is not None:
        conn.close()
        messagebox.showinfo("Sucesso", "Conexão bem-sucedida com o banco de dados!")


# Função para salvar as configurações de conexão
def save_config():
    config = {
        "host": host_entry.get(),
        "database": database_entry.get(),
        "user": user_entry.get(),
        "password": password_entry.get(),
        "backup_dir": backup_dir_entry.get()
    }
    with open('db_config.json', 'w') as f:
        json.dump(config, f)
    messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")


# Função para selecionar o diretório de backup
def select_backup_dir():
    backup_dir = filedialog.askdirectory()
    backup_dir_entry.delete(0, tk.END)
    backup_dir_entry.insert(0, backup_dir)


# Função para fazer o backup do banco de dados
def backup_database():
    try:
        backup_subdir = os.path.join(backup_dir_entry.get(), datetime.now().strftime('%Y-%m-%d'))
        os.makedirs(backup_subdir, exist_ok=True)

        dump_command = f"pg_dump -U {user_entry.get()} -W {password_entry.get()} -F t {database_entry.get()} > {os.path.join(backup_subdir, 'backup.tar')}"
        os.system(dump_command)

        messagebox.showinfo("Sucesso", "Backup realizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível realizar o backup: {e}")


# GUI
host_label = tk.Label(root, text="Host:")
host_label.pack()
host_entry = tk.Entry(root)
host_entry.insert(0, "localhost")
host_entry.pack()

database_label = tk.Label(root, text="Database:")
database_label.pack()
database_entry = tk.Entry(root)
database_entry.pack()

user_label = tk.Label(root, text="User:")
user_label.pack()
user_entry = tk.Entry(root)
user_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

backup_dir_label = tk.Label(root, text="Backup Directory:")
backup_dir_label.pack()
backup_dir_entry = tk.Entry(root)
backup_dir_entry.pack()

select_backup_dir_button = tk.Button(root, text="Select Backup Directory", command=select_backup_dir)
select_backup_dir_button.pack()

test_button = tk.Button(root, text="Test Connection", command=test_connection)
test_button.pack()

save_button = tk.Button(root, text="Save Config", command=save_config)
save_button.pack()

backup_button = tk.Button(root, text="Backup Database", command=backup_database)
backup_button.pack()


def validate_data():
    try:
        engine = create_engine(
            f"postgresql://{user_entry.get()}:{password_entry.get()}@{host_entry.get()}/{database_entry.get()}")

        # Obtém a lista de todas as tabelas no banco de dados
        table_names = engine.table_names()

        for table_name in table_names:
            # Obtém um dataframe pandas com os dados da tabela
            df = pd.read_sql_table(table_name, engine)

            # Resto do código...

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível validar os dados: {e}")


validate_button = tk.Button(root, text="Validar Dados", command=validate_data)
validate_button.pack()

root.mainloop()
