@echo off
echo ==============================================================================
echo                      STARTING VERITRUST AI PLATFORM
echo               SIH26261 ^| AICTE ^| Smart Automation Scrutiny
echo ==============================================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "VERITRUST AI Backend" cmd /k "backend\venv\Scripts\python.exe backend\run.py"

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
cd frontend
start "VERITRUST AI Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==============================================================================
echo   VERITRUST AI is launching!
echo   Frontend:  http://localhost:5173
echo   Backend:   http://127.0.0.1:8000
echo   API Docs:  http://127.0.0.1:8000/docs
echo ==============================================================================
echo.
pause
