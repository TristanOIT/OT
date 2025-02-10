from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from models.inventory import InventoryItem
from app import db

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stock', methods=['GET'])
@login_required
def stock_home():
    return render_template('stock.html')

@stock_bp.route('/api/stock/scan', methods=['POST'])
@login_required
def scan_barcode():
    data = request.get_json()
    barcode = data.get('barcode')
    if not barcode:
        return jsonify({"status": "error", "message": "No barcode provided"}), 400

    # If the barcode does not exist, create a new inventory record.
    item = InventoryItem.query.filter_by(barcode=barcode).first()
    if not item:
        item = InventoryItem(barcode=barcode, hardware_status="Pending")
        db.session.add(item)
        db.session.commit()
    return jsonify({"status": "success", "barcode": barcode})

@stock_bp.route('/stock/update', methods=['GET', 'POST'])
@login_required
def update_status():
    barcode = request.args.get('barcode')
    if request.method == 'POST':
        status = request.form.get('hardware_status')
        item = InventoryItem.query.filter_by(barcode=barcode).first()
        if item:
            item.hardware_status = status
            db.session.commit()
            flash('Hardware status updated successfully', 'success')
            return redirect(url_for('stock.stock_home'))
        else:
            flash('Inventory item not found', 'danger')
    return render_template('stock_update.html', barcode=barcode)
