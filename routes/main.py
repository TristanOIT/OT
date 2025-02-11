from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@login_required
def index():
    """Main index page"""
    return render_template('index.html')
