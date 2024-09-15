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
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        language_to_learn = data.get('language_to_learn')
        proficiency_level = data.get('proficiency_level')
        daily_goal = data.get('daily_goal')
        start_option = data.get('start_option')

        if not all([name, email, password, language_to_learn, proficiency_level, daily_goal, start_option]):
            return jsonify({'error': 'Missing required fields'}), 400

        existing_user = g.db.query(User).filter(User.email == email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400

        # TODO: Hash the password before storing it
        new_user = User(
            name=name,
            email=email,
            password_hash=password,  # Replace this with a hashed password
            language_to_learn=language_to_learn,
            proficiency_level=proficiency_level,
            daily_goal=daily_goal,
            start_option=start_option
        )
        g.db.add(new_user)
        g.db.commit()
        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        g.db.rollback()
        return jsonify({'error': str(e)}), 500
    
@api_bp.route('/lesson', methods=['GET'])
def get_lesson():
    username = request.args.get('username')
    lesson_type = request.args.get('lesson_type', 'vocabulary')

    user = g.db.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    lesson = lesson_generator.generate_lesson(user.target_language, user.proficiency_level, lesson_type)
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