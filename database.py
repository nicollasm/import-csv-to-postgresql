import configparser
import psycopg2
import pandas as pd


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


def connect_to_db(host, dbname, user, password):
    global failed_attempts, lock_start_time

    try:
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(str(e))


def get_tables(conn):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    df = pd.read_sql_query(query, conn)
    return df['table_name'].tolist()


def get_columns(conn, table_name):
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    df = pd.read_sql_query(query, conn)
    return df['column_name'].tolist()


selected_columns = []


def confirm_selection(selection_indices, fields):
    global selected_columns
    selected_columns = [fields[i] for i in selection_indices]


def export_data_to_csv(conn, table_name):
    global selected_columns
    try:
        if not selected_columns:
            # Se nenhuma coluna foi selecionada, selecione todas
            query = f"SELECT * FROM {table_name}"
        else:
            # Selecione apenas as colunas escolhidas
            query = f"SELECT {', '.join(selected_columns)} FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        df.to_csv(f"{table_name}.csv", index=False)
        print(f"Dados exportados com sucesso para {table_name}.csv")
    except Exception as e:
        print("Não foi possível exportar os dados.")
        print(e)
