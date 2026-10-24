#!/usr/bin/env bash
echo "=============================================================================="
echo "                     STARTING VERITRUST AI PLATFORM"
echo "              SIH26261 | AICTE | Smart Automation Scrutiny"
echo "=============================================================================="
echo ""

# Activate Python venv & run backend in background
python3 -m venv backend/venv 2>/dev/null
source backend/venv/bin/activate
pip install -r backend/requirements.txt
python backend/run.py &
BACKEND_PID=$!
echo "Backend running on PID $BACKEND_PID (http://127.0.0.1:8000)"

# Start Frontend
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
echo "Frontend running on PID $FRONTEND_PID (http://localhost:5173)"
cd ..

echo ""
echo "VERITRUST AI is active!"
echo "Frontend: http://localhost:5173"
echo "Backend:  http://127.0.0.1:8000"
echo "Press CTRL+C to terminate both servers."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
