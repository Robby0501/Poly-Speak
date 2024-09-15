from flask import Blueprint, jsonify, request
from app.models.user import User
from app.services.lesson_generator import LessonGenerator
import os

api_bp = Blueprint('api', __name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
lesson_generator = LessonGenerator(openai_api_key=openai_api_key)
LessonGenerator()

# Temporary storage for users (replace with a database in a real application)
users = {}

@api_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        username = data.get('username')
        target_language = data.get('target_language')
        proficiency_level = data.get('proficiency_level')

        if not all([username, target_language, proficiency_level]):
            return jsonify({'error': 'Missing required fields'}), 400

        if username in users:
            return jsonify({'error': 'User already exists'}), 400

        user = User(username, target_language, proficiency_level)
        users[username] = user
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api_bp.route('/lesson', methods=['GET'])
def get_lesson():
    username = request.args.get('username')
    lesson_type = request.args.get('lesson_type', 'vocabulary')

    if username not in users:
        return jsonify({'error': 'User not found'}), 404

    user = users[username]
    lesson = lesson_generator.generate_lesson(user.target_language, user.proficiency_level, lesson_type)
    return jsonify({'lesson': lesson})

@api_bp.route('/quiz', methods=['GET'])
def get_quiz():
    username = request.args.get('username')
    topic = request.args.get('topic', 'general')

    if username not in users:
        return jsonify({'error': 'User not found'}), 404

    user = users[username]
    quiz = lesson_generator.generate_quiz(user.target_language, user.proficiency_level, topic)
    return jsonify({'quiz': quiz})

@api_bp.route('/user/progress', methods=['POST'])
def update_user_progress():
    data = request.json
    username = data.get('username')
    points = data.get('points', 0)
    completed_lesson = data.get('completed_lesson', False)

    if username not in users:
        return jsonify({'error': 'User not found'}), 404

    user = users[username]
    user.add_points(points)

    if completed_lesson:
        user.increase_streak()

    return jsonify({
        'message': 'User progress updated',
        'points': user.points,
        'streak': user.streak
    })