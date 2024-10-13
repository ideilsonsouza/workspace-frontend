import requests
import json
from database.connect import DatabaseManager  # Supondo que você salvou a classe DatabaseManager em um arquivo chamado database.py

class AuthManager:
    def __init__(self, api_url):
        """
        Inicializa a classe com a URL da API e o nome do banco de dados.
        """
        self.api_url = api_url
        self.db = DatabaseManager()

    def authenticate(self, username, password):
        """
        Faz a autenticação do usuário e armazena o token no banco de dados.
        """
        try:
            response = requests.post(f"{self.api_url}/auth/login", json={"username": username, "password": password})
            response.raise_for_status()  # Lança um erro se a resposta não for 2xx

            token_data = response.json()
            # Armazenar o token no banco de dados
            self.db.insert_or_update('token', token_data, where="id = 1")

            return token_data  # Retorna os dados do token recebido

        except requests.RequestException as e:
            print(f"Erro na autenticação: {str(e)}")
            return None

    def make_request(self, method, endpoint, **kwargs):
        """
        Faz uma requisição HTTP para a API usando o método especificado.
        """
        token = self.db.get_single_record('token', where="id = 1")

        if isinstance(token, str) and "error" not in token:
            token = json.loads(token)  # Converter a string JSON de volta para dicionário

        if isinstance(token, dict) and 'access_token' in token:
            headers = {'Authorization': f"Bearer {token['access_token']}"}
            url = f"{self.api_url}{endpoint}"

            try:
                response = requests.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()  # Retorna a resposta como JSON

            except requests.RequestException as e:
                print(f"Erro na requisição: {str(e)}")
                return None
        else:
            print("Token não disponível ou inválido.")
            return None

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.db.close()

# Exemplo de uso
# if __name__ == "__main__":
#     api_url = "http://localhost:8000/api"  # Substitua pela URL da sua API
#     auth_manager = AuthManager(api_url)

#     # Autenticar usuário
#     token_data = auth_manager.authenticate("username", "password")
#     print("Token armazenado:", token_data)

#     # Fazer uma requisição GET para um endpoint
#     result = auth_manager.make_request("GET", "/data")
#     print("Resultado da requisição:", result)

#     # Fechar a conexão com o banco de dados
#     auth_manager.close()
