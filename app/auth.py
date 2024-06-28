from flask import jsonify
import jwt
from datetime import datetime, timedelta
from app.config import Config


# # Chave secreta para assinatura do token (mantenha segura em produção)
SECRET_KEY = Config.SECRET_KEY

# Função para gerar um token JWT
def generate_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),  # Tempo de expiração do token
            'iat': datetime.utcnow(),  # Tempo de emissão do token
            'sub': user_id  # Identificador do usuário (pode ser o ID do usuário no banco de dados)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)

def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return data
    except jwt.ExpiredSignatureError:
        return None