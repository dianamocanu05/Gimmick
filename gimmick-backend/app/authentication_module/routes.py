from flask import request, jsonify

from app.authentication_module.models import User, session

def init_routes(app):
    @app.route('/auth/signup',methods=['POST'])
    def signup():
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate user data (you should add your validation logic here)

        # Create a new user
        new_user = User(username=username, email=email, password_hash=password)
        session.add(new_user)
        session.commit()

        return jsonify({"message": f"User {username} signed up successfully"}), 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Validate login data (you should add your validation logic here)

        # Check if the user exists
        user = session.query(User).filter_by(username=username).first()

        if user:
            if user.password_hash == password:
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404