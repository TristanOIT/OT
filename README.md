# Overtime and Stock Management Portal

This is a Flask-based web application for managing overtime requests and stock inventory.

## Setup Instructions

Follow the steps below to set up your development environment, initialize the database, and start the application on both Windows and Linux.

### Step 1: Create a Virtual Environment

#### Windows
Create and activate your virtual environment with:

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS
Create and activate your virtual environment with:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

Ensure that your `requirements.txt` file includes all necessary packages (e.g., Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login).

### Step 3: Initialize the Database

Set up the database using Flask-Migrate.

#### Set the environment variable for the Flask app:

##### Windows (CMD)
```bash
set FLASK_APP=app.py
```

##### Windows (PowerShell)
```bash
$env:FLASK_APP = "app.py"
```

##### Linux / macOS
```bash
export FLASK_APP=app.py
```

(Optional) Set the environment to development:

##### Windows (CMD)
```bash
set FLASK_ENV=development
```

##### Windows (PowerShell)
```bash
$env:FLASK_ENV = "development"
```

##### Linux / macOS
```bash
export FLASK_ENV=development
```

#### Run the database migrations to create the database and required tables:

```bash
flask db upgrade
```

If you later update your models, create new migrations with:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Step 4: Start the Application

After initializing the database, start the Flask development server.

#### Windows and Linux
```bash
flask run
```

The application will run at [http://localhost:5000](http://localhost:5000). Open this URL in your web browser to start using the app.

## Additional Commands

### Deactivate the Virtual Environment:

```bash
deactivate
```

### Re-activate the Virtual Environment:

#### Windows:
```bash
venv\Scripts\activate
```

#### Linux / macOS:
```bash
source venv/bin/activate
```

## Project Structure

```
OT/
├── app.py
├── config.py
├── extensions.py
├── models/
│   ├── user.py
│   ├── overtime.py
│   └── inventory.py
├── routes/
│   ├── auth.py
│   ├── overtime.py
│   └── stock.py
├── static/
│   └── loading/
│       ├── loading.css
│       └── loading.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── overtime.html
│   ├── overtime_report.html
│   ├── stock.html
│   └── stock_update.html
├── requirements.txt
└── README.md
```

## Troubleshooting

If you encounter any issues:

- Ensure your Python version is 3.7 or higher.
- Verify that your virtual environment is activated.
- Check your terminal for any error messages during the migration or startup process.

Feel free to open issues or contribute to the project on GitHub.
