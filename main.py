import tkinter as tk
import psycopg2
import pandas as pd
import configparser

failed_attempts = 0
lock_start_time = 0


def connect_to_db(host, dbname, user, password, failed_attempts, lock_start_time):
    LOCK_DURATION = 300  # Duração do bloqueio em segundos (5 minutos)

    if failed_attempts >= 5:
        remaining_lock_time = LOCK_DURATION - (time.monotonic() - lock_start_time)

        if remaining_lock_time > 0:
            print(f"Aguarde {int(remaining_lock_time)} segundos antes de tentar novamente.")
            return None

    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        failed_attempts = 0  # Resetar o contador de tentativas falhas
        return conn
    except Exception as e:
        print("Não foi possível conectar ao banco de dados.")
        print(e)
        failed_attempts += 1

        if failed_attempts >= 5:
            lock_start_time = time.monotonic()

        return None


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


def create_app():
    root = tk.Tk()
    root.title("Interface de Banco de Dados")
    root.geometry("800x600")

    # Campos de entrada para os detalhes da conexão ao banco de dados
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

    # Botão para salvar as configurações
    save_button = tk.Button(root, text="Salvar Configurações", command=lambda: save_config(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get(), failed_attempts, lock_start_time))

    save_button.pack()
    exit_button = tk.Button(root, text="Sair", command=root.quit)
    exit_button.pack()

    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
