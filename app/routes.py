from flask import jsonify, Response, request
from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import user, vehicles
from app.database import db
from app.auth import generate_token, verify_token


approutes = Blueprint('users', __name__)
login_manager = LoginManager()

# Rotas do Flask
@approutes.route('/')
def index():
    return ({'message': 'Faça login'})

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@approutes.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        User = user.query.filter_by(username=data['username']).first()
        hashed_password = User.password_hash 
        if not User or not check_password_hash(hashed_password, data['password_hash']):
            return jsonify({'error': 'Invalid username or password'}), 401
        else:
            login_user(User)
            user_id = User.id
            token = generate_token(user_id)
            return jsonify({'token': token, 'message': 'Logado com sucesso!'})

@approutes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Deslogado com sucesso!'})

@approutes.route('/create_user', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password_hash')

        if password is None or len(password) == 0:
            return 'Senha inválida', 400
        
        passwordHash = generate_password_hash(password)
        
        # hashed_password = generate_password_hash(data[password], method='pbkdf2:sha256')
        new_user = user(name=name, email=email, username=username, password_hash=passwordHash)

        try:
        # Adicionar ao banco de dados
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@approutes.route('/profile/<int:user_id>', methods=['GET'])
def get_user(user_id):
    User = user.query.get(user_id)
    if User:
        return jsonify({
            'id': User.id,
            'name': User.name,
            'email': User.email,
            'username': User.username
        })
    else:
        return jsonify({'message': 'User not found'}), 404
    
@approutes.route('/protected')
def protected():
    token = request.headers.get('Authorization')
    if token:
        data = verify_token(token)
        if data:
            return jsonify({'message': 'Token is valid!'})
    return jsonify({'message': 'is not token valid'})

#vehicles
@approutes.route('/vehicles', methods=['GET'])
def get_vehicles():
    list_vehicles = vehicles.query.all()
    if list_vehicles:
        vehicles_list = []
        for vehicle in list_vehicles:
            vehicles_list.append({
                'id': vehicle.id,
                'model': vehicle.model,
                'mark': vehicle.mark,
                'color': vehicle.color,
                'type_vehicles': vehicle.type_vehicles,
                'exchange': vehicle.exchange,
                'vehicle_situation': vehicle.vehicle_situation,
                'uf': vehicle.uf,
                'country': vehicle.country,
                'plate': vehicle.plate
            })
        return jsonify(vehicles_list), 201
    else:
        return jsonify({'message': 'Lista de veiculos nao encontradas'}), 404

@approutes.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    Vehicle = vehicles.query.get(vehicle_id)
    if Vehicle:
        return jsonify({
            'id': Vehicle.id,
            'model': Vehicle.model,
            'mark': Vehicle.mark,
            'color': Vehicle.color,
            'type_vehicles': Vehicle.type_vehicles,
            'exchange': Vehicle.exchange,
            'vehicle_situation': Vehicle.vehicle_situation,
            'uf': Vehicle.uf,
            'country': Vehicle.country,
            'plate': Vehicle.plate
        })
    else:
        return jsonify({'message': 'Veículo não encontrado'}), 404
    
@approutes.route('/newVehicle', methods=['POST'])
def newVehicle():
    if request.method == 'POST':
        data = request.get_json()
        model = data.get('model')
        mark = data.get('mark')
        color = data.get('color')
        type_vehicles = data.get('type_vehicles')
        exchange = data.get('exchange')
        vehicle_situation = data.get('vehicle_situation')
        uf = data.get('uf')
        country = data.get('country')
        plate = data.get('plate')

        if not model or not mark or not color or not type_vehicles or not exchange or not vehicle_situation or not uf or not country or not plate:
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

        new_vehicle = vehicles(model=model, mark=mark, color=color, type_vehicles=type_vehicles, exchange=exchange, vehicle_situation=vehicle_situation, uf=uf, country=country, plate=plate)
        try:
        # Adicionar ao banco de dados
            db.session.add(new_vehicle)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        

#lists        
@approutes.route("/UF", methods=['GET'])
def get_ufs():
    states = [
        {"sigla": "AC", "nome": "Acre"},
        {"sigla": "AL", "nome": "Alagoas"},
        {"sigla": "AP", "nome": "Amapá"},
        {"sigla": "AM", "nome": "Amazonas"},
        {"sigla": "BA", "nome": "Bahia"},
        {"sigla": "CE", "nome": "Ceará"},
        {"sigla": "DF", "nome": "Distrito Federal"},
        {"sigla": "ES", "nome": "Espírito Santo"},
        {"sigla": "GO", "nome": "Goiás"},
        {"sigla": "MA", "nome": "Maranhão"},
        {"sigla": "MT", "nome": "Mato Grosso"},
        {"sigla": "MS", "nome": "Mato Grosso do Sul"},
        {"sigla": "MG", "nome": "Minas Gerais"},
        {"sigla": "PA", "nome": "Pará"},
        {"sigla": "PB", "nome": "Paraíba"},
        {"sigla": "PR", "nome": "Paraná"},
        {"sigla": "PE", "nome": "Pernambuco"},
        {"sigla": "PI", "nome": "Piauí"},
        {"sigla": "RJ", "nome": "Rio de Janeiro"},
        {"sigla": "RN", "nome": "Rio Grande do Norte"},
        {"sigla": "RS", "nome": "Rio Grande do Sul"},
        {"sigla": "RO", "nome": "Rondônia"},
        {"sigla": "RR", "nome": "Roraima"},
        {"sigla": "SC", "nome": "Santa Catarina"},
        {"sigla": "SP", "nome": "São Paulo"},
        {"sigla": "SE", "nome": "Sergipe"},
        {"sigla": "TO", "nome": "Tocantins"},
    ]
    return jsonify(states)

@approutes.route("/country", methods=['GET'])
def getCountry():
    states = [
        # {"nome": "Argentina"},
        {"nome": "Brasil"},
        # {"nome": "Uruguai"},
        # {"nome": "Paraguai"},
        # {"nome": "Venezuela"},
    ]
    return jsonify(states)