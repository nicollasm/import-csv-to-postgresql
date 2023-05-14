import tkinter as tk
from tkinter import messagebox
import psycopg2
import configparser
import time
from datetime import datetime, timedelta

# Contador de tentativas de login falhas
failed_attempts = 0
# Hora de início do bloqueio
lock_start_time = None


# Conexão ao banco de dados
def connect_to_db(host, dbname, user, password):
    global failed_attempts, lock_start_time
    if failed_attempts >= 5:
        # Se o usuário falhou na tentativa de login 5 vezes, verifique o tempo de bloqueio
        if time.time() - lock_start_time < 300:
            remaining_time = 300 - (time.time() - lock_start_time)
            print(f"Você deve aguardar {int(remaining_time // 60)} minutos e {int(remaining_time % 60)} segundos antes de tentar novamente.")
            return
        else:
            # Se o tempo de bloqueio expirou, redefina failed_attempts e permita que o usuário tente fazer login novamente
            failed_attempts = 0

    try:
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password
        )

        print("Conectado com sucesso ao banco de dados.")
        failed_attempts = 0
        open_data_window(conn)  # Abra a janela de dados após uma conexão bem-sucedida

    except Exception as e:
        print(e)
        failed_attempts += 1
        if failed_attempts >= 5:
            lock_start_time = time.time()



def open_data_window(conn):
    data_window = tk.Toplevel()
    data_window.title("Dados do Banco de Dados")
    data_window.geometry("800x600")

    # Dropdown para selecionar a tabela
    table_label = tk.Label(data_window, text="Selecione a tabela:")
    table_label.pack()
    tables = get_tables(conn)
    table_var = tk.StringVar(data_window)
    table_var.set(tables[0])  # Valor padrão
    table_dropdown = tk.OptionMenu(data_window, table_var, *tables)
    table_dropdown.pack()

    # Botão para selecionar os campos
    select_fields_button = tk.Button(data_window, text="Selecionar campos", command=lambda: select_fields(conn, table_var.get()))
    select_fields_button.pack()

    # Botão para exportar dados em CSV
    export_button = tk.Button(data_window, text="Exportar CSV", command=lambda: export_data_to_csv(conn, table_var.get()))
    export_button.pack()

    # Botão para fechar a janela de dados
    exit_button = tk.Button(data_window, text="Sair", command=data_window.quit)
    exit_button.pack()



def get_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables
    except psycopg2.Error as e:
        print("Erro ao obter tabelas:", e)


def save_config(host, dbname, user, password):
    config = configparser.ConfigParser()
    config['DATABASE'] = {
        'host': host,
        'dbname': dbname,
        'user': user,
        'password': password
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print("Configurações salvas com sucesso.")


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    host = config['DATABASE']['host']
    dbname = config['DATABASE']['dbname']
    user = config['DATABASE']['user']
    password = config['DATABASE']['password']

    return host, dbname, user, password


def get_tables(conn):
    try:
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        df = pd.read_sql_query(query, conn)
        return df['table_name'].tolist()
    except Exception as e:
        print("Não foi possível obter as tabelas.")
        print(e)
        return []


def get_columns(conn, table_name):
    try:
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        df = pd.read_sql_query(query, conn)
        return df['column_name'].tolist()
    except Exception as e:
        print("Não foi possível obter as colunas.")
        print(e)
        return []


def create_app():
    root = tk.Tk()
    root.title("Interface de Banco de Dados")
    root.geometry("800x600")

    host_label = tk.Label(root, text="Host:")
    host_label.pack()
    host_entry = tk.Entry(root)
    host_entry.pack()

    dbname_label = tk.Label(root, text="Nome do Banco de Dados:")
    dbname_label.pack()
    dbname_entry = tk.Entry(root)
    dbname_entry.pack()

    user_label = tk.Label(root, text="Usuário:")
    user_label.pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    password_label = tk.Label(root, text="Senha:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    save_button = tk.Button(root, text="Salvar Configurações", command=lambda: save_config(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get()))
    save_button.pack()

    login_button = tk.Button(root, text="Conectar", command=lambda: connect_to_db(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get()))
    login_button.pack()

    exit_button = tk.Button(root, text="Sair", command=root.quit)
    exit_button.pack()

    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
