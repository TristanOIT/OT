# Overtime Management System

## Overview
A comprehensive overtime tracking and management application with advanced user administration features, designed to streamline workforce time management and reporting.

## Recent Improvements
- Enhanced UI/UX with modern, responsive design
- Improved overtime request visualization
- Refined dashboard and reporting functionality
- Optimized performance and user experience

## Features
- 🔐 User Authentication
- 📝 Overtime Request Submission
- 👥 Admin User Management
- 📊 Advanced Reporting and Dashboard
- 📦 Integrated Stock Management System

## Technology Stack
- **Backend**: Python 3.8+, Flask
- **Database**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, Modern CSS with Gradient Backgrounds
- **Design**: Responsive, Blur-effect UI

## Prerequisites
- Python 3.8+
- pip
- Virtual environment support

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/overtime-management.git
cd overtime-management
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Create Admin User
```bash
python create_admin.py Manager S3cur1ty?! manager@example.com
```

### 6. Run the Application
```bash
flask run
```

## UI/UX Design
The application features a modern, responsive design with:
- Gradient background animations
- Blur-effect containers
- Responsive typography
- Dark mode compatibility
- Intuitive navigation

## Security Features
- Secure user authentication
- Role-based access control
- Protected routes
- Secure password management

## Stock Management Integration
The integrated Stock Management System provides:
- Real-time inventory tracking
- Comprehensive stock movement records
- Detailed reporting capabilities
- Seamless integration with overtime management

## Troubleshooting

### Comprehensive Troubleshooting Guide

#### 1. Application Startup Issues
- **Problem**: Application fails to start
  - Check Python version compatibility
  - Verify all dependencies are installed
  - Ensure virtual environment is activated
  ```bash
  python --version  # Confirm Python 3.8+
  pip list  # Check installed packages
  ```

- **Problem**: Flask not found or import errors
  ```bash
  pip install flask
  pip install -r requirements.txt --upgrade
  ```

#### 2. Database Connection Problems
- **Symptoms**: 
  - Connection refused
  - Migration errors
  - Database lock issues

- **Solutions**:
  ```bash
  # Reset database completely
  del instance\app.sqlite
  rmdir /s /q migrations
  
  # Reinitialize database
  flask db init
  flask db migrate -m "Reset database"
  flask db upgrade
  ```

#### 3. Authentication Troubleshooting
- **Problem**: Login failures
  - Verify user credentials
  - Check password hashing
  - Confirm user account exists

- **Debugging Steps**:
  ```python
  # In Python shell or debug route
  from app import db
  from models import User
  
  # List all users
  users = User.query.all()
  for user in users:
      print(user.username, user.email)
  ```

#### 4. Stock Management Issues
- **Problem**: Incorrect stock calculations
  - Verify minimum stock level settings
  - Check unit of measurement
  - Validate stock movement entries

- **Diagnostic Commands**:
  ```python
  # Check stock item details
  stock_items = StockItem.query.all()
  for item in stock_items:
      print(f"Item: {item.name}")
      print(f"Current Quantity: {item.total_quantity}")
      print(f"Minimum Level: {item.minimum_stock_level}")
  ```

#### 5. Performance and Logging
- **Enable Detailed Logging**:
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```

#### 6. Common Environment Issues
- **Windows-Specific**:
  - Ensure Python is in system PATH
  - Use PowerShell or Command Prompt compatible commands
  - Check file path separators

- **Virtual Environment**:
  ```bash
  # Recreate virtual environment
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

#### 7. Network and Firewall
- Check local port availability (default 5000)
- Disable firewall temporarily for testing
- Verify no conflicting services on the port

#### 8. Dependency Conflicts
```bash
# Check for potential conflicts
pip check
pip list --outdated
```

### Advanced Debugging

#### Logging Configuration
Add to `config.py`:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
```

#### Performance Profiling
```python
from flask_profiler import Profiler

profiler = Profiler(app)
profiler.init_app(app)
```

### Emergency Recovery
- **Complete Reset**:
  ```bash
  # Dangerous: Removes all data
  del instance\app.sqlite
  rmdir /s /q migrations
  rmdir /s /q venv
  
  # Recreate everything
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  flask db init
  flask db migrate
  flask db upgrade
  python create_admin.py
  ```

### Support
- Open GitHub Issues
- Email: support@overtimemanagement.com
- Include:
  - Full error traceback
  - Python version
  - Operating system
  - Dependency list (`pip freeze`)

## Navigation and Menu Structure

### User Dropdown
- Submit Overtime
- My Overtime Requests
- Overtime Dashboard

### Admin Dropdown
- Manage Users
- Create User
- Overtime Approval
- Overtime Reports
- Stock Reports

### Permissions
- Regular users can access Overtime submission, requests, and dashboard
- Admin users have additional access to user management and administrative reports

## User Management

### Admin Features
- Create new users
- Edit user details
- Delete users
- Set admin privileges

### Access
- Log in as admin
- Navigate to Admin > Manage Users

## Stock Management

### Overview
The Stock Management System is a comprehensive inventory tracking solution integrated into the Overtime Management Application. It provides real-time insights into your inventory, helping you make informed decisions about stock levels, purchases, and sales.

### Key Features

#### Inventory Tracking
- Create and manage stock items with detailed attributes
- Track item quantities, unit prices, and total value
- Support for multiple units of measurement
- Categorize items (Raw Materials, Finished Goods, Consumables, Equipment)

#### Stock Movement Tracking
- Record detailed stock movements:
  - Purchases
  - Sales
  - Transfers
  - Adjustments
- Automatic calculation of stock levels
- Timestamp and user tracking for all movements

#### Reporting and Alerts
- Generate comprehensive stock reports
- Calculate total stock value
- Identify low stock items
- View detailed movement history for each item

### Stock Item Attributes
- Name
- Category
- Description
- Current Quantity
- Minimum Stock Level
- Unit of Measurement
- Unit Price
- Total Value

### Usage
1. Navigate to Stock Management in the application
2. Add new stock items
3. Record stock movements
4. Monitor inventory through reports and dashboards

### Best Practices
- Regularly update stock levels
- Set appropriate minimum stock levels
- Use movement descriptions for clarity
- Leverage reports for inventory planning

## Security Notes
- Passwords are hashed
- Admin access is restricted
- Prevent deletion of last admin user

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/overtime-management](https://github.com/yourusername/overtime-management)
