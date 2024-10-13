import sqlite3
import json
from database.tables import tables_array  # Supondo que as tabelas estão no arquivo tables.py

class DatabaseManager:
    def __init__(self, db_name='data.db'):
        """
        Inicializa a classe com o nome do banco de dados e cria as tabelas.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """
        Conecta ao banco de dados e cria um cursor.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """
        Cria as tabelas necessárias no banco de dados, se elas não existirem.
        """
        try:
            for table in tables_array:
                self.cursor.execute(table)
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {str(e)}")

    def execute_query(self, query, params=()):
        """
        Executa uma consulta SELECT e retorna os resultados como uma lista de dicionários.
        """
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]

            results = [dict(zip(columns, row)) for row in rows]
            return results

        except sqlite3.Error as e:
            return {"error": str(e)}

    def execute_non_query(self, query, params=()):
        """
        Executa uma consulta de inserção, atualização ou exclusão.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return {"status": "success"}

        except sqlite3.Error as e:
            self.conn.rollback()
            return {"error": str(e)}

    def get_single_record(self, table, where=None, params=()):
        """
        Retorna um registro como um objeto, se houver apenas um,
        ou como uma lista de objetos se houver mais de um registro.
        """
        query = f"SELECT * FROM {table}"

        if where:
            query += f" WHERE {where}"

        records = self.execute_query(query, params)

        if isinstance(records, dict) and "error" in records:
            return json.dumps(records, indent=4)

        if len(records) == 1:
            return json.dumps(records[0], indent=4)

        elif len(records) == 0:
            return json.dumps([])

        else:
            return json.dumps(records, indent=4)

    def insert_or_update(self, table, data, where=None):
        """
        Insere ou atualiza um registro em uma tabela.
        Se o registro já existir (com base no 'where'), ele será atualizado.
        """

        query_check = f"SELECT COUNT(*) FROM {table} WHERE {where}"
        self.cursor.execute(query_check)
        count = self.cursor.fetchone()[0]

        if count > 0:
            set_clause = ', '.join([f"{key} = ?" for key in data])
            query = f"UPDATE {table} SET {set_clause} WHERE {where}"
            values = list(data.values())
            return self.execute_non_query(query, values)
        else:
            keys = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = list(data.values())
            query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
            return self.execute_non_query(query, values)


# if __name__ == "__main__":
#     # Inicializar a classe de gerenciamento do banco de dados
#     db = DatabaseManager('auth.db')

#     # Inserir um novo token ou atualizar o existente
#     token_data = {
#         'id': 1,  # ID fixo para o token
#         'access_token': 'novo_token',
#         'token_type': 'bearer',
#         'expires_in': 3600
#     }
#     result = db.insert_or_update('token', token_data, where="id = 1")
#     print(result)

#     # Consultar um registro da tabela token
#     result = db.get_single_record('token', where="id = 1")
#     print(result)

#     # Fechar a conexão com o banco de dados
#     db.close()
