#!/bin/bash

echo "🚀 Starting SIMBA Frontend and Backend..."

# Stop on error
set -e

# Setup backend
echo "📦 Setting up backend..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Auto-seed curriculum if database is empty or missing
if [ ! -f "instance/simpai.db" ]; then
  echo "🌱 Database not found. Seeding curriculum..."
  python3 seed_curriculum_master.py
elif python3 -c "
from app.main import create_app
from app.models.db_models import Course
app = create_app()
with app.app_context():
    count = Course.query.count()
    exit(0 if count > 0 else 1)
" 2>/dev/null; then
  echo "✅ Database has curriculum data."
else
  echo "🌱 Database is empty. Seeding curriculum..."
  python3 seed_curriculum_master.py
fi

echo "🏃‍♂️ Starting backend..."
python3 wsgi.py &
BACKEND_PID=$!

# Setup frontend
echo "📦 Setting up frontend..."
npm install
echo "🏃‍♂️ Starting frontend..."
npm run dev &
FRONTEND_PID=$!

echo "✅ Both services started! Press Ctrl+C to stop them."
echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:3000"

# Cleanup on Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '🛑 Stopped.'" EXIT

# Wait for all background processes
wait
