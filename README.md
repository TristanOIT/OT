# Overtime Management System

## Overview
A comprehensive overtime tracking and management application with advanced user administration features.

## Features
- User Authentication
- Overtime Request Submission
- Admin User Management
- Reporting and Dashboard

## Prerequisites
- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/overtime-management.git
cd overtime-management
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
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

## Troubleshooting

### Common Issues and Solutions

#### Database Migration Errors
1. **No such column error**
   - Delete existing database and migrations
   ```bash
   del instance\app.sqlite
   rmdir /s /q migrations
   ```
   - Reinitialize migrations
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

#### User Management Errors
- Ensure you have the latest model definitions
- Check that email column is present in User model
- Verify database migrations are up to date

## User Management

### Admin Features
- Create new users
- Edit user details
- Delete users
- Set admin privileges

### Access
- Log in as admin
- Navigate to Admin > Manage Users

## Security Notes
- Passwords are hashed
- Admin access is restricted
- Prevent deletion of last admin user

## Development
- Debug mode: `flask run --debug`
- Test environment: Configure in `config.py`

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Your License Here]
