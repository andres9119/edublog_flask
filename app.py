from flask import Flask, jsonify, request
from flask_cors import CORS
from db import create_connection

app = Flask(__name__)
CORS(app)  

# Ruta para obtener todas las noticias
@app.route('/api/news', methods=['GET'])
def get_news():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM News")
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(results)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    password = data['password']  # Contraseña en texto plano
    email = data['email']
    
    # Conexión a la base de datos
    connection = create_connection()
    cursor = connection.cursor()
    
    # Inserción de nuevo usuario
    cursor.execute(
        "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)",
        (username, password, email)  # Almacena la contraseña en texto plano
    )
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({'message': 'User created', 'user': {'id': user_id, 'username': username}}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    # Conexión a la base de datos
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)  # Devuelve los resultados como diccionarios
    
    # Obtener todos los usuarios
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(users)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    # Conexión a la base de datos
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Obtener un usuario por ID
    cursor.execute("SELECT * FROM Users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # Actualiza la contraseña si se proporciona
    is_authenticated = data.get('is_authenticated')  # Actualiza el estado de autenticación si se proporciona

    # Conexión a la base de datos
    connection = create_connection()
    cursor = connection.cursor()
    
    # Construir la consulta de actualización
    update_fields = []
    values = []
    
    if username:
        update_fields.append("username = %s")
        values.append(username)
    
    if email:
        update_fields.append("email = %s")
        values.append(email)
    
    if password:  # La contraseña se actualiza como texto plano
        update_fields.append("password = %s")
        values.append(password)
    
    if is_authenticated is not None:  
        update_fields.append("is_authenticated = %s")
        values.append(is_authenticated)

    values.append(id)
    update_query = f"UPDATE Users SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(update_query, values)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User updated'})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Conexión a la base de datos
    connection = create_connection()
    cursor = connection.cursor()
    
    # Eliminar un usuario por ID
    cursor.execute("DELETE FROM Users WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        return jsonify({'message': 'User deleted'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    connection = create_connection()
    cursor = connection.cursor()

    # Consulta para verificar el usuario
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()

    # Compara la contraseña ingresada con la almacenada en texto plano
    if user and password == user[2]:  # Asumiendo que la contraseña está en la columna 2
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, message="Email o contraseña incorrectos."), 401

@app.route('/api/events', methods=['GET'])
def get_events():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    title = data['title']
    description = data['description']
    date = data['date']
    location = data.get('location', 'Unknown')
    image = data.get('image', None)  # Capturar el valor de la imagen

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO Events (title, description, date, location, image) VALUES (%s, %s, %s, %s, %s)",
        (title, description, date, location, image)
    )
    connection.commit()
    event_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({'message': 'Event created', 'event': {'id': event_id, 'title': title}}), 201

# Ruta para obtener un evento por ID
@app.route('/api/events/<int:id>', methods=['GET'])
def get_event(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Events WHERE id = %s", (id,))
    event = cursor.fetchone()
    cursor.close()
    connection.close()

    if event:
        return jsonify(event)
    return jsonify({'message': 'Event not found'}), 404

# Ruta para actualizar un evento
@app.route('/api/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    location = data.get('location')
    image = data.get('image')  # Asegúrate de capturar la imagen también

    connection = create_connection()
    cursor = connection.cursor()

    update_fields = []
    values = []

    if title:
        update_fields.append("title = %s")
        values.append(title)

    if description:
        update_fields.append("description = %s")
        values.append(description)

    if date:
        update_fields.append("date = %s")
        values.append(date)

    if location:
        update_fields.append("location = %s")
        values.append(location)

    if image:
        update_fields.append("image = %s")
        values.append(image)

    # Asegúrate de añadir el ID al final de los valores
    values.append(id)
    update_query = f"UPDATE Events SET {', '.join(update_fields)} WHERE id = %s"
    
    try:
        cursor.execute(update_query, values)
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Event not found'}), 404
            
    except connection.errors.DatabaseError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Event updated', 'event': {'id': id, 'title': title, 'description': description, 'date': date, 'location': location, 'image': image}}), 200

# Ruta para eliminar un evento
@app.route('/api/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM Events WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount > 0:
        return jsonify({'message': 'Event deleted'})
    return jsonify({'message': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
