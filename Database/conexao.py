import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os



load_dotenv()

def conectar():
    try:
        conexao =  mysql.connector.connect(
            host     = os.getenv('DB_HOST'),
            database = os.getenv('DB_NAME'),
            user     = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        return conexao
    
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def desconectar(conexao, cursor):
    if cursor:
        cursor.close()

    if conexao and conexao.is_connected():
        conexao.close()

        