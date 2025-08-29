@echo off
echo Starting FinVoice Application...

echo Starting Backend Server...
start cmd /k "cd backend && npm start"

echo Starting ML Service...
start cmd /k "cd ml_service && python main.py"

echo Starting Frontend...
start cmd /k "cd frontend && npm start"

echo All services started! The application will be available at:
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000
echo ML Service: http://localhost:8000