Overtime and Stock Management Portal
This is a Flask-based web application for managing overtime requests and stock inventory. Follow the instructions below to set up your development environment, initialize the database, and start the application on both Windows and Linux.

Prerequisites
Python 3.7 or higher
pip
(Optional) virtualenv or use Python's built-in venv module
Setup
1. Clone the Repository
Open your terminal or command prompt and clone the repository:

git clone https://github.com/TristanOIT/OT.git
cd OT


2. Create a Virtual Environment
You can use Python's built-in venv module to create a virtual environment.

Windows
bash
python -m venv venv
venv\Scripts\activate
Linux / macOS
bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Once the virtual environment is activated, install the required packages:

bash
pip install -r requirements.txt
Make sure that your requirements.txt file includes all necessary packages, e.g., Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, etc.

4. Initialize the Database
Before starting the application for the first time, set up the database using Flask-Migrate.

Windows and Linux
Export the Flask app environment variable:

Windows (CMD):

bash
set FLASK_APP=app.py
Windows (PowerShell):

bash
$env:FLASK_APP = "app.py"
Linux / macOS:

bash
export FLASK_APP=app.py
(Optional) Set the environment to development:

Windows (CMD):

bash
set FLASK_ENV=development
Windows (PowerShell):

bash
$env:FLASK_ENV = "development"
Linux / macOS:

bash
export FLASK_ENV=development
Run the database migrations to create the database and required tables:

bash
flask db upgrade
Note: If you need to generate new migrations after modifying your models, run:

bash
flask db migrate -m "Description of changes"
flask db upgrade
5. Start the Application
After setting up the database, you can start the Flask development server.

Windows and Linux
bash
flask run
The application will run on http://localhost:5000. Open this URL in your web browser to start using the app.

Additional Commands
Deactivate the Virtual Environment:

bash
deactivate
Re-activating the Virtual Environment:

Windows:
bash
venv\Scripts\activate
Linux / macOS:
bash
source venv/bin/activate
Project Structure
Code
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
Troubleshooting
If you encounter any issues:

Ensure your Python version is correct.
Verify that your virtual environment is activated.
Check the console for any error messages during the migration process.
Feel free to open issues or contribute to the project on GitHub.

Happy coding!
