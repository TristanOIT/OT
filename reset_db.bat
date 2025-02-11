@echo off
echo Resetting the database...

REM Remove existing database and migrations
if exist instance\app.db del instance\app.db
if exist migrations rmdir /s /q migrations

REM Recreate migrations and upgrade
call flask db init
call flask db migrate -m "Initial migration"
call flask db upgrade

REM Create initial admin user
python reset_db.py

if %ERRORLEVEL% NEQ 0 (
    echo Error occurred while resetting the database.
    echo Please check the error message above.
    pause
    exit /b %ERRORLEVEL%
)

echo Database reset complete.
pause
