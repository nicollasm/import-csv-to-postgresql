import tkinter as tk
from tkinter import messagebox
from database import connect_to_db, save_config, read_config, get_tables


def create_login_window():
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

    save_button = tk.Button(root, text="Salvar Configurações", command=lambda: save_config(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get()))
    save_button.pack()

    connect_button = tk.Button(root, text="Conectar", command=lambda: connect_to_db(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get()))
    connect_button.pack()

    test_button = tk.Button(root, text="Testar Conexão", command=lambda: test_connection(
        host_entry.get(), dbname_entry.get(), user_entry.get(), password_entry.get()))
    test_button.pack()

    exit_button = tk.Button(root, text="Sair", command=root.quit)
    exit_button.pack()

    return root


def create_data_window(conn):
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
    select_fields_button = tk.Button(data_window, text="Selecionar campos",
                                     command=lambda: select_fields(conn, table_var.get()))
    select_fields_button.pack()

    # Botão para exportar dados em CSV
    export_button = tk.Button(data_window, text="Exportar CSV",
                              command=lambda: export_data_to_csv(conn, table_var.get()))
    export_button.pack()

    # Botão para fechar a janela de dados
    exit_button = tk.Button(data_window, text="Sair", command=data_window.quit)
    exit_button.pack()


def select_fields(conn, table_name):
    fields_window = tk.Toplevel()
    fields_window.title(f"Selecionar campos da tabela {table_name}")
    fields_window.geometry("400x300")

    # Listbox para selecionar múltiplos campos
    fields_label = tk.Label(fields_window, text="Selecione os campos:")
    fields_label.pack()
    fields = get_columns(conn, table_name)
    fields_var = [tk.StringVar(value=field) for field in fields]
    fields_listbox = tk.Listbox(fields_window, selectmode=tk.MULTIPLE)
    fields_listbox.pack()
    for field in fields:
        fields_listbox.insert(tk.END, field)

    # Botão para confirmar a seleção
    confirm_button = tk.Button(fields_window, text="Confirmar seleção",
                               command=lambda: confirm_selection(fields_listbox.curselection(), fields))
    confirm_button.pack()


def test_connection(host, dbname, user, password):
    conn = connect_to_db(host, dbname, user, password)
    if conn:
        messagebox.showinfo("Testar Conexão", "Conexão bem-sucedida!")
        conn.close()
    else:
        messagebox.showerror("Testar Conexão", "Não foi possível se conectar ao banco de dados.")
