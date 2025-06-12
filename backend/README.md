
____________________________________________________________________________

### Complete Setup Instructions
1. Project Setup
cd backend

2. Setup Python Virtual Environment
Python Version = 3.12

# Install dependencies
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

3. Install Dependencies
pip install -r requirements.txt

4. Environment Configuration
Create .env file:

bash
# Environment
ENVIRONMENT=development
DEBUG=true

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Database
DATABASE_URL=sqlite:///./quantumeco.db

# Blockchain (Ganache local)
BLOCKCHAIN_URL=http://127.0.0.1:8545
PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d

# External APIs (optional - will use mock data if not provided)
# OPENROUTESERVICE_API_KEY=your_key_here
# OPENWEATHER_API_KEY=your_key_here
# GOOGLE_MAPS_API_KEY=your_key_here

# Demo settings
ENABLE_DEMO_MODE=true
WALMART_STORES_COUNT=10500

5. Blockchain Setup (For the quantum-blockchain directory, Optional but Recommended)
Install Node.js and Ganache:

bash
# Install Node.js (if not already installed)
# Download from https://nodejs.org/

# Install Ganache CLI
npm install -g ganache-cli

# Start Ganache (in a separate terminal)
ganache-cli --deterministic --accounts 10 --host 0.0.0.0 --port 8545

6. Run the Application
bash
# Method 1: Direct Python execution
python -m app.main

# Method 2: Using uvicorn command
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: For production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

7. Verify Installation
Open your browser and test these endpoints:

Main API: http://localhost:8000/

API Documentation: http://localhost:8000/docs

Health Check: http://localhost:8000/health

Quick Demo: http://localhost:8000/demo/quick-start

System Info: http://localhost:8000/system-info

8. Test Key Endpoints
bash
# Test health check
curl http://localhost:8000/health

# Test quick demo
curl http://localhost:8000/demo/quick-start

# Test route optimization (POST request)
curl -X POST "http://localhost:8000/api/routes/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "locations": [
      {"id": "depot", "latitude": 40.7128, "longitude": -74.0060, "demand_kg": 0},
      {"id": "loc1", "latitude": 40.7589, "longitude": -73.9851, "demand_kg": 50}
    ],
    "vehicles": [
      {"id": "truck1", "type": "diesel_truck", "capacity_kg": 1000, "cost_per_km": 0.85, "emission_factor": 0.27}
    ]
  }'

9. Demo Preparation Commands
bash
# Generate impressive demo data
curl http://localhost:8000/api/demo/walmart-nyc

# Get performance showcase
curl http://localhost:8000/api/demo/performance-showcase

# Get analytics dashboard
curl http://localhost:8000/api/analytics/dashboard

# Get Walmart impact report
curl http://localhost:8000/api/analytics/walmart/impact

10. Troubleshooting
If you get import errors:

bash
# Add the project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# On Windows:
set PYTHONPATH=%PYTHONPATH%;%cd%
If Ganache connection fails:

The app will work in mock mode

Check if Ganache is running on port 8545

Verify the BLOCKCHAIN_URL in .env

If database issues occur:

bash
# Delete and recreate database
rm quantumeco.db
python -c "from app.database import init_database; init_database()"
12. Production Deployment
bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
13. Development Tips
bash
# Watch logs in real-time
tail -f logs/app.log

# Check API endpoints
curl http://localhost:8000/openapi.json

# Test with different environments
ENVIRONMENT=production python -m app.main
Quick Start for Demo
Fastest way to get running for demo:

bash
# 1. Clone/create project
mkdir quantumeco-backend && cd quantumeco-backend

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install FastAPI and dependencies
pip install fastapi uvicorn python-dotenv pydantic-settings ortools numpy web3 requests aiohttp sqlalchemy

# 4. Copy the main.py file above into app/main.py

# 5. Create minimal .env file
echo "ENVIRONMENT=development
DEBUG=true
ENABLE_DEMO_MODE=true" > .env

# 6. Run the application
uvicorn app.main:app --reload

# 7. Test the demo
curl http://localhost:8000/demo/quick-start