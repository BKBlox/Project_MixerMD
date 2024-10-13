from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.user import User
from app.models.game_session import GameSession

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/host')
def host():
    return render_template('host.html')

@frontend_bp.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        if not full_name:
            return render_template('player.html', error='Full name is required.')
        # Create user and store user ID in session
        user_id = User.create_user(full_name, {})
        session['user_id'] = user_id
        return redirect(url_for('frontend.submit_story'))
    return render_template('player.html')

@frontend_bp.route('/submit-story', methods=['GET', 'POST'])
def submit_story():
    if 'user_id' not in session:
        return redirect(url_for('frontend.player'))
    if request.method == 'POST':
        story = request.form.get('story')
        if not story:
            return render_template('submit_story.html', error='Story is required.')
        user_id = session['user_id']
        # Check for existing waiting sessions
        waiting_session = GameSession.find_waiting_session(user_id)
        if waiting_session:
            # Join existing session
            GameSession.join_session(waiting_session['_id'], user_id, story)
            session['session_id'] = waiting_session['_id']
            return redirect(url_for('frontend.wait_for_partner'))
        else:
            # Create new session
            session_id = GameSession.create_session(user_id, story)
            session['session_id'] = session_id
            return redirect(url_for('frontend.wait_for_partner'))
    return render_template('submit_story.html')

@frontend_bp.route('/wait-for-partner')
def wait_for_partner():
    # Implement logic to check if a partner has joined
    return render_template('wait_for_partner.html')

# Add additional routes as needed
