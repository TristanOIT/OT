from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.overtime import OvertimeRequest
from app import db
from datetime import datetime

overtime_bp = Blueprint('overtime', __name__)

@overtime_bp.route('/overtime', methods=['GET'])
@login_required
def overtime_form():
    return render_template('overtime.html')

@overtime_bp.route('/api/overtime/submit', methods=['POST'])
@login_required
def submit_overtime():
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
        date=date
    )
    db.session.add(new_request)
    db.session.commit()
    flash('Overtime request submitted successfully', 'success')
    return redirect(url_for('overtime.overtime_form'))

@overtime_bp.route('/overtime/report', methods=['GET'])
@login_required
def overtime_report():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('overtime.overtime_form'))

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
