from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from functools import wraps

admin_blueprint = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_blueprint.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        is_admin = 'is_admin' in request.form
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('admin.create_user'))

        # Create new user
        new_user = User(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully!', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('admin/create_user.html')

@admin_blueprint.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form
        
        # Only update password if a new one is provided
        if request.form['password']:
            user.set_password(request.form['password'])
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Prevent deleting the current user or the last admin
    user = User.query.get_or_404(user_id)
    
    if user == current_user:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    # Ensure at least one admin remains
    admin_count = User.query.filter_by(is_admin=True).count()
    if admin_count <= 1 and user.is_admin:
        flash('Cannot delete the last admin user.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))
