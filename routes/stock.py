from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import StockItem, StockMovement
from sqlalchemy import func

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stock/manage', methods=['GET', 'POST'])
@login_required
def stock_management():
    """Comprehensive stock management page"""
    # Check inventory access
    if not current_user.has_inventory_access():
        flash('You do not have permission to access inventory features.', 'danger')
        return redirect(url_for('index'))
    
    # Handle adding new stock item
    if request.method == 'POST' and request.form.get('form_type') == 'add_item':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        total_quantity = float(request.form.get('total_quantity', 0))
        minimum_stock_level = float(request.form.get('minimum_stock_level', 0))
        unit_of_measurement = request.form.get('unit_of_measurement')
        unit_price = float(request.form.get('unit_price'))

        # Create new stock item
        new_item = StockItem(
            name=name,
            category=category,
            description=description,
            total_quantity=total_quantity,
            minimum_stock_level=minimum_stock_level,
            unit_of_measurement=unit_of_measurement,
            unit_price=unit_price
        )
        new_item.update_total_value()
        
        # Create initial stock movement
        if total_quantity > 0:
            initial_movement = StockMovement(
                stock_item=new_item,
                quantity=total_quantity,
                movement_type='purchase',
                description='Initial stock entry',
                user_id=current_user.id
            )
            db.session.add(initial_movement)
        
        db.session.add(new_item)
        db.session.commit()
        
        flash('Stock item added successfully', 'success')
        return redirect(url_for('stock.stock_management'))
    
    # Handle stock movement
    if request.method == 'POST' and request.form.get('form_type') == 'stock_movement':
        stock_item_id = request.form.get('stock_item_id')
        quantity = float(request.form.get('quantity'))
        movement_type = request.form.get('movement_type')
        description = request.form.get('description')

        # Find the stock item
        stock_item = StockItem.query.get(stock_item_id)
        if not stock_item:
            flash('Stock item not found', 'danger')
            return redirect(url_for('stock.stock_management'))

        # Create stock movement
        movement = StockMovement(
            stock_item=stock_item,
            quantity=quantity,
            movement_type=movement_type,
            description=description,
            user_id=current_user.id
        )
        
        # Apply the movement
        movement.apply_movement()
        
        db.session.add(movement)
        db.session.commit()
        
        flash(f'Stock {movement_type} recorded successfully', 'success')
        return redirect(url_for('stock.stock_management'))
    
    # Fetch data for the page
    stock_items = StockItem.query.all()
    low_stock_items = [item for item in stock_items if item.is_low_stock()]
    total_stock_value = sum(item.total_value for item in stock_items)
    recent_movements = StockMovement.query.order_by(StockMovement.timestamp.desc()).limit(10).all()
    
    return render_template('stock_management.html', 
                           stock_items=stock_items, 
                           low_stock_items=low_stock_items,
                           total_stock_value=total_stock_value,
                           recent_movements=recent_movements)

@stock_bp.route('/stock/reports', methods=['GET'])
@login_required
def stock_reports():
    """Generate stock reports"""
    # Check inventory access
    if not current_user.has_inventory_access():
        flash('You do not have permission to access inventory features.', 'danger')
        return redirect(url_for('index'))
    
    # Total stock value
    total_stock_value = db.session.query(func.sum(StockItem.total_value)).scalar() or 0
    
    # Low stock items
    low_stock_items = StockItem.query.filter(StockItem.total_quantity <= StockItem.minimum_stock_level).all()
    
    # Recent stock movements
    recent_movements = StockMovement.query.order_by(StockMovement.timestamp.desc()).limit(50).all()
    
    return render_template('stock_reports.html', 
                           total_stock_value=total_stock_value,
                           low_stock_items=low_stock_items,
                           recent_movements=recent_movements)

@stock_bp.route('/stock/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def stock_item_details(item_id):
    """View and edit stock item details"""
    # Check inventory access
    if not current_user.has_inventory_access():
        flash('You do not have permission to access inventory features.', 'danger')
        return redirect(url_for('index'))
    
    stock_item = StockItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        # Update stock item details
        stock_item.name = request.form.get('name')
        stock_item.category = request.form.get('category')
        stock_item.description = request.form.get('description')
        stock_item.minimum_stock_level = float(request.form.get('minimum_stock_level'))
        stock_item.unit_price = float(request.form.get('unit_price'))
        
        stock_item.update_total_value()
        db.session.commit()
        
        flash('Stock item updated successfully', 'success')
        return redirect(url_for('stock.stock_item_details', item_id=item_id))
    
    # Get stock movement history
    movement_history = stock_item.stock_movements.order_by(StockMovement.timestamp.desc()).all()
    
    return render_template('stock_item_details.html', 
                           stock_item=stock_item, 
                           movement_history=movement_history)
