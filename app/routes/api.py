from flask import Blueprint, jsonify, request, g
from app.models.user import User
from app.services.lesson_generator import LessonGenerator
import os
from sqlalchemy.orm import Session

api_bp = Blueprint('api', __name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
lesson_generator = LessonGenerator(openai_api_key=openai_api_key)
LessonGenerator()

# Temporary storage for users (replace with a database in a real application)

# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()

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

        existing_user = g.db.query(User).filter(User.email == email).first()
        if existing_user:
            print("User with this email already exists")  # Debug print
            return jsonify({'error': 'User with this email already exists'}), 400

        hashed_password = User.hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            language_to_learn=language_to_learn,
            proficiency_level=proficiency_level,
            daily_goal=int(daily_goal),  # Ensure daily_goal is an integer
            start_option=start_option
        )
        g.db.add(new_user)
        g.db.commit()
        print("User created successfully:", new_user.id)  # Debug print
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        g.db.rollback()
        print("Error creating user:", str(e))  # Debug print
        import traceback
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