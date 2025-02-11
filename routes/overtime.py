from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models.overtime import OvertimeRequest
from models.user import User
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Rename blueprint to avoid potential conflicts
overtime_blueprint = Blueprint('overtime', __name__)

@overtime_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Get user's overtime requests for the last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        user_requests = OvertimeRequest.query.filter(
            OvertimeRequest.manager_name == current_user.username,
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        # Get total hours logged in the last 30 days
        total_hours = sum(float(req.time_logged) for req in user_requests)
        
        return render_template('dashboard.html', 
                               requests=user_requests, 
                               total_hours=total_hours)
    except OperationalError:
        # If status column is missing, add a default status
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE overtime_request ADD COLUMN status TEXT DEFAULT "pending"'))
        db.session.commit()
        
        # Retry the query
        user_requests = OvertimeRequest.query.filter(
            OvertimeRequest.manager_name == current_user.username,
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        total_hours = sum(float(req.time_logged) for req in user_requests)
        
        return render_template('dashboard.html', 
                               requests=user_requests, 
                               total_hours=total_hours)

@overtime_blueprint.route('/overtime', methods=['GET'])
@login_required
def overtime_form():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    return render_template('overtime.html')

@overtime_blueprint.route('/api/overtime/submit', methods=['POST'])
@login_required
def submit_overtime():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    ticket_number = request.form.get('ticket_number')
    time_logged = request.form.get('time_logged')
    client_name = request.form.get('client_name')
    manager_name = request.form.get('manager_name')
    date_str = request.form.get('date')

    # Validate date format
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('overtime.overtime_form'))

    new_request = OvertimeRequest(
        ticket_number=ticket_number,
        time_logged=time_logged,
        client_name=client_name,
        manager_name=manager_name,
        date=date,
        status='pending'  # Explicitly set default status
    )
    db.session.add(new_request)
    db.session.commit()
    flash('Overtime request submitted successfully', 'success')
    return redirect(url_for('overtime.dashboard'))

@overtime_blueprint.route('/admin/overtime/approve', methods=['GET', 'POST'])
@login_required
def admin_overtime_approval():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('overtime.dashboard'))
    
    # Get pending overtime requests
    pending_requests = OvertimeRequest.query.filter_by(status='pending').all()
    
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        action = request.form.get('action')
        
        overtime_request = OvertimeRequest.query.get(request_id)
        if overtime_request:
            if action == 'approve':
                overtime_request.status = 'approved'
                flash(f'Overtime request for {overtime_request.ticket_number} approved', 'success')
            elif action == 'deny':
                overtime_request.status = 'denied'
                flash(f'Overtime request for {overtime_request.ticket_number} denied', 'warning')
            
            db.session.commit()
            return redirect(url_for('overtime.admin_overtime_approval'))
    
    return render_template('admin_overtime_approval.html', requests=pending_requests)

@overtime_blueprint.route('/overtime/report', methods=['GET'])
@login_required
def overtime_report():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('overtime.dashboard'))

    # Get filter parameters from the query string
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    manager_name = request.args.get('manager_name')
    client_name = request.args.get('client_name')

    query = OvertimeRequest.query
    if start_date and end_date:
        try:
            sd = datetime.strptime(start_date, '%Y-%m-%d').date()
            ed = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(OvertimeRequest.date.between(sd, ed))
        except ValueError:
            flash('Invalid date format for filtering', 'danger')
    if manager_name:
        query = query.filter(OvertimeRequest.manager_name.ilike(f"%{manager_name}%"))
    if client_name:
        query = query.filter(OvertimeRequest.client_name.ilike(f"%{client_name}%"))

    overtime_requests = query.all()
    return render_template('overtime_report.html', requests=overtime_requests)

@overtime_blueprint.route('/admin/reports', methods=['GET', 'POST'])
@login_required
def admin_reports():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('main.index'))
    
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('overtime.dashboard'))
    
    # Get all users for the dropdown
    users = User.query.all()
    
    # Default date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get filter parameters
    form_start_date = request.form.get('start_date')
    form_end_date = request.form.get('end_date')
    status = request.form.get('status', 'all')
    manager_name = request.form.get('manager_name', '')
    client_name = request.form.get('client_name', '')
    selected_user_id = request.form.get('user_id', '')
    
    # Parse dates
    try:
        if form_start_date:
            start_date = datetime.strptime(form_start_date, '%Y-%m-%d').date()
        if form_end_date:
            end_date = datetime.strptime(form_end_date, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'danger')
    
    # Filter requests
    query = OvertimeRequest.query.filter(
        OvertimeRequest.date.between(start_date, end_date)
    )
    
    # Additional filters
    if status and status != 'all':
        query = query.filter(OvertimeRequest.status == status)
    
    if manager_name:
        query = query.filter(OvertimeRequest.manager_name.ilike(f"%{manager_name}%"))
    
    if client_name:
        query = query.filter(OvertimeRequest.client_name.ilike(f"%{client_name}%"))
    
    # Filter by selected user
    if selected_user_id:
        selected_user = User.query.get(selected_user_id)
        if selected_user:
            query = query.filter(OvertimeRequest.user_id == selected_user_id)
    
    # Execute query
    requests = query.order_by(OvertimeRequest.date.desc()).all()
    
    # Calculate total hours
    total_hours = sum(float(req.time_logged) for req in requests)
    
    return render_template(
        'admin_reports.html', 
        requests=requests, 
        start_date=start_date, 
        end_date=end_date, 
        status=status, 
        manager_name=manager_name, 
        client_name=client_name,
        users=users,
        selected_user_id=selected_user_id,
        total_hours=total_hours
    )

@overtime_blueprint.route('/admin/reports/pdf', methods=['POST'])
@login_required
def generate_pdf_report():
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('index'))
    
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('overtime.dashboard'))
    
    # Get filter parameters
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    status = request.form.get('status', 'all')
    manager_name = request.form.get('manager_name', '')
    client_name = request.form.get('client_name', '')
    selected_user_id = request.form.get('user_id', '')
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else datetime.now().date() - timedelta(days=30)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else datetime.now().date()
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('overtime.admin_reports'))
    
    # Filter requests
    query = OvertimeRequest.query.filter(
        OvertimeRequest.date.between(start_date, end_date)
    )
    
    # Additional filters
    if status and status != 'all':
        query = query.filter(OvertimeRequest.status == status)
    
    if manager_name:
        query = query.filter(OvertimeRequest.manager_name.ilike(f"%{manager_name}%"))
    
    if client_name:
        query = query.filter(OvertimeRequest.client_name.ilike(f"%{client_name}%"))
    
    # Filter by selected user
    if selected_user_id:
        selected_user = User.query.get(selected_user_id)
        if selected_user:
            query = query.filter(OvertimeRequest.user_id == selected_user_id)
    
    # Execute query
    overtime_requests = query.order_by(OvertimeRequest.date.desc()).all()
    
    # Calculate total hours
    total_hours = sum(float(req.time_logged) for req in overtime_requests)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Prepare table data
    table_data = [
        ['Date', 'Ticket Number', 'Manager', 'Client', 'Hours', 'Status']
    ]
    
    for req in overtime_requests:
        table_data.append([
            req.date.strftime('%Y-%m-%d'),
            req.ticket_number,
            req.manager_name,
            req.client_name,
            req.time_logged,
            req.status
        ])
    
    # Add total hours row
    table_data.append([
        'Total', '', '', '', f'{total_hours:.2f}', ''
    ])
    
    # Create table
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    # Title and subtitle
    title = Paragraph(f"Overtime Report", styles['Title'])
    
    # Create a custom subtitle style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.darkgrey,
        alignment=1,  # Center alignment
        spaceAfter=12
    )
    subtitle = Paragraph(f"From {start_date} to {end_date}", subtitle_style)
    
    # Build PDF
    elements = [title, subtitle, table]
    doc.build(elements)
    
    # Prepare the response
    buffer.seek(0)
    return send_file(
        buffer, 
        as_attachment=True, 
        download_name=f'overtime_report_{start_date}_to_{end_date}.pdf',
        mimetype='application/pdf'
    )

@overtime_blueprint.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_overtime_dashboard():
    """Admin overtime dashboard to view and manage all overtime requests"""
    # Check admin access
    if not current_user.is_admin and not current_user.can_access_overtime:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        # Get all overtime requests for the last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        all_requests = OvertimeRequest.query.filter(
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        # Aggregate statistics
        total_requests = len(all_requests)
        pending_requests = sum(1 for req in all_requests if req.status == 'pending')
        approved_requests = sum(1 for req in all_requests if req.status == 'approved')
        rejected_requests = sum(1 for req in all_requests if req.status == 'rejected')
        total_hours = sum(float(req.time_logged) for req in all_requests)
        
        return render_template('admin_overtime_dashboard.html', 
                               requests=all_requests, 
                               total_requests=total_requests,
                               pending_requests=pending_requests,
                               approved_requests=approved_requests,
                               rejected_requests=rejected_requests,
                               total_hours=total_hours)
    except OperationalError:
        # If status column is missing, add a default status
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE overtime_request ADD COLUMN status TEXT DEFAULT "pending"'))
        db.session.commit()
        
        # Retry the query
        all_requests = OvertimeRequest.query.filter(
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        # Aggregate statistics
        total_requests = len(all_requests)
        pending_requests = sum(1 for req in all_requests if req.status == 'pending')
        approved_requests = sum(1 for req in all_requests if req.status == 'approved')
        rejected_requests = sum(1 for req in all_requests if req.status == 'rejected')
        total_hours = sum(float(req.time_logged) for req in all_requests)
        
        return render_template('admin_overtime_dashboard.html', 
                               requests=all_requests, 
                               total_requests=total_requests,
                               pending_requests=pending_requests,
                               approved_requests=approved_requests,
                               rejected_requests=rejected_requests,
                               total_hours=total_hours)

@overtime_blueprint.route('/overtime_requests', methods=['GET'])
@login_required
def overtime_requests():
    """View user's overtime requests"""
    # Check overtime access
    if not current_user.has_overtime_access():
        flash('You do not have permission to access overtime features.', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        # Get user's overtime requests for the last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        user_requests = OvertimeRequest.query.filter(
            OvertimeRequest.manager_name == current_user.username,
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        # Get total hours logged in the last 30 days
        total_hours = sum(float(req.time_logged) for req in user_requests)
        
        return render_template('overtime_requests.html', 
                               requests=user_requests, 
                               total_hours=total_hours)
    except OperationalError:
        # If status column is missing, add a default status
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE overtime_request ADD COLUMN status TEXT DEFAULT "pending"'))
        db.session.commit()
        
        # Retry the query
        user_requests = OvertimeRequest.query.filter(
            OvertimeRequest.manager_name == current_user.username,
            OvertimeRequest.date >= thirty_days_ago
        ).order_by(OvertimeRequest.date.desc()).all()
        
        total_hours = sum(float(req.time_logged) for req in user_requests)
        
        return render_template('overtime_requests.html', 
                               requests=user_requests, 
                               total_hours=total_hours)
