# tables.py

# Definição das tabelas no banco de dados
tables_array = [
    '''
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_url TEXT NOT NULL,           -- URL do backend (ex.: URL da API)
        api_port INTEGER NOT NULL,
        refresh_interval INTEGER NOT NULL, -- Intervalo de tempo para renovação de token (em segundos)
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        access_token TEXT NOT NULL,      -- Token de autenticação
        token_type TEXT NOT NULL,        -- Tipo do token, geralmente 'Bearer'
        expires_in INTEGER NOT NULL,     -- Tempo de expiração do token em segundos
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
]