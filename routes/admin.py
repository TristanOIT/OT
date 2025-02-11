from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash
from functools import wraps

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route('/users', methods=['GET'])
@admin_required
def manage_users():
    """Manage users page"""
    users = User.query.all()
    return render_template('admin_manage_users.html', users=users)

@admin_blueprint.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create a new user with role-based access"""
    if request.method == 'POST':
        # Extract form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Role selection
        is_admin = request.form.get('is_admin') == 'on'
        can_access_overtime = request.form.get('can_access_overtime') == 'on'
        can_access_inventory = request.form.get('can_access_inventory') == 'on'
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('admin.create_user'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            is_admin=is_admin,
            can_access_overtime=can_access_overtime,
            can_access_inventory=can_access_inventory
        )
        
        # Set password
        new_user.set_password(password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('User created successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin_create_user.html')

@admin_blueprint.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user roles and details"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Update user details
        user.email = request.form.get('email')
        
        # Update roles
        user.is_admin = request.form.get('is_admin') == 'on'
        user.can_access_overtime = request.form.get('can_access_overtime') == 'on'
        user.can_access_inventory = request.form.get('can_access_inventory') == 'on'
        
        # Optional password change
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        # Save changes
        db.session.commit()
        
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin_edit_user.html', user=user)

@admin_blueprint.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user"""
    # Prevent deleting the last admin or current user
    user = User.query.get_or_404(user_id)
    if user.is_admin and User.query.filter_by(is_admin=True).count() <= 1:
        flash('Cannot delete the last admin user.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    if user.id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))
