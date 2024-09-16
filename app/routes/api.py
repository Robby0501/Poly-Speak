from flask import Blueprint, jsonify, request, g
from app.models.user import User
from app.services.lesson_generator import LessonGenerator
from flask_cors import cross_origin
import os
from sqlalchemy.orm import Session
import traceback

api_bp = Blueprint('api', __name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
lesson_generator = LessonGenerator(openai_api_key=openai_api_key)
LessonGenerator()

@api_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    print(f"Login attempt for email: {email}")

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        # Use email as string
        user = g.db.query(User).filter(User.email == email).first()
        print(f"User found: {user is not None}")

        if user:
            print(f"Stored password hash type: {type(user.password_hash)}")
            print(f"Stored password hash length: {len(user.password_hash)}")
            password_correct = user.check_password(password)
            print(f"Password correct: {password_correct}")

            if password_correct:
                response = jsonify({
                    'message': 'Login successful',
                    'user_id': user.id,
                    'language_to_learn': user.language_to_learn
                })
                return response, 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        print(f"Error during login: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An internal server error occurred'}), 500

@api_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        language_to_learn = data.get('language_to_learn')
        proficiency_level = data.get('proficiency_level')
        daily_goal = data.get('daily_goal')
        start_option = data.get('start_option')

        if not all([name, email, password, language_to_learn, proficiency_level, daily_goal, start_option]):
            print("Missing required fields")  # Debug print
            return jsonify({'error': 'Missing required fields'}), 400

        # Use email as string without encoding
        existing_user = g.db.query(User).filter(User.email == email).first()
        if existing_user:
            print("User with this email already exists")  # Debug print
            return jsonify({'error': 'User with this email already exists'}), 400

        hashed_password = User.hash_password(password)
        new_user = User(
            name=name,
            email=email,  # Store as string
            password_hash=hashed_password,
            language_to_learn=language_to_learn,
            proficiency_level=proficiency_level,
            daily_goal=int(daily_goal),
            start_option=start_option
        )
        g.db.add(new_user)
        g.db.commit()
        print("User created successfully:", new_user.id)  # Debug print
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        g.db.rollback()
        print("Error creating user:", str(e))  # Debug print
        traceback.print_exc()  # Print the full traceback
        return jsonify({'error': str(e)}), 500

@api_bp.route('/initial-lesson', methods=['GET'])
def get_initial_lesson():
    user_id = request.args.get('user_id')
    start_option = request.args.get('start_option')
    proficiency_level = request.args.get('proficiency_level')

    user = g.db.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if start_option == 'from scratch':
        lesson = lesson_generator.generate_lesson(user.language_to_learn, 'beginner', 'vocabulary')
    else:  # 'find my level'
        lesson = lesson_generator.generate_lesson(user.language_to_learn, proficiency_level, 'vocabulary')

    return jsonify({'lesson': lesson})

@api_bp.route('/units/<int:user_id>', methods=['GET'])
def get_units(user_id):
    user = g.db.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # This is a mock-up of units and lessons. In a real application, you'd fetch this from a database.
    units = [
        {
            'id': 1,
            'title': 'Greetings and Basics',
            'lessons': [
                {'id': 1, 'title': 'Hello and Goodbye'},
                {'id': 2, 'title': 'Basic Phrases'},
                {'id': 3, 'title': 'Numbers 1-10'},
            ]
        },
        {
            'id': 2,
            'title': 'Travel Essentials',
            'lessons': [
                {'id': 4, 'title': 'At the Airport'},
                {'id': 5, 'title': 'Booking a Hotel'},
                {'id': 6, 'title': 'Asking for Directions'},
            ]
        },
        {
            'id': 3,
            'title': 'Daily Life',
            'lessons': [
                {'id': 7, 'title': 'Telling Time'},
                {'id': 8, 'title': 'Weather and Seasons'},
                {'id': 9, 'title': 'Shopping for Groceries'},
            ]
        }
    ]

    return jsonify({'units': units})

@api_bp.route('/quiz', methods=['GET'])
def get_quiz():
    username = request.args.get('username')
    topic = request.args.get('topic', 'general')

    user = g.db.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    quiz = lesson_generator.generate_quiz(user.target_language, user.proficiency_level, topic)
    return jsonify({'quiz': quiz})

@api_bp.route('/user/progress', methods=['POST'])
def update_user_progress():
    data = request.json
    username = data.get('username')
    points = data.get('points', 0)
    completed_lesson = data.get('completed_lesson', False)

    user = g.db.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.add_points(points)
    if completed_lesson:
        user.increase_streak()

    g.db.commit()

    return jsonify({
        'message': 'User progress updated',
        'points': user.points,
        'streak': user.streak
    })