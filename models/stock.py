from extensions import db
from datetime import datetime
from models.user import User

class StockItem(db.Model):
    __tablename__ = 'stock_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # Inventory tracking
    total_quantity = db.Column(db.Float, default=0)
    minimum_stock_level = db.Column(db.Float, default=0)
    unit_of_measurement = db.Column(db.String(20), nullable=False)  # e.g., 'kg', 'liters', 'pieces'
    
    # Pricing and cost
    unit_price = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, default=0)
    
    # Tracking
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    stock_movements = db.relationship('StockMovement', back_populates='stock_item', lazy='dynamic')
    
    def update_total_value(self):
        """Update the total value based on current quantity and unit price"""
        self.total_value = self.total_quantity * self.unit_price
        self.last_updated = datetime.utcnow()
    
    def is_low_stock(self):
        """Check if the current stock is below the minimum stock level"""
        return self.total_quantity <= self.minimum_stock_level

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    
    MOVEMENT_TYPES = [
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment')
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    stock_item_id = db.Column(db.Integer, db.ForeignKey('stock_items.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)
    
    # Additional context
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    
    # Relationships
    stock_item = db.relationship('StockItem', back_populates='stock_movements')
    user = db.relationship(User, backref='stock_movements')
    
    def apply_movement(self):
        """Apply the stock movement to the associated stock item"""
        if self.movement_type == 'purchase':
            self.stock_item.total_quantity += self.quantity
        elif self.movement_type == 'sale':
            self.stock_item.total_quantity -= self.quantity
        elif self.movement_type == 'adjustment':
            # For manual adjustments, can be positive or negative
            self.stock_item.total_quantity += self.quantity
        
        self.stock_item.update_total_value()
