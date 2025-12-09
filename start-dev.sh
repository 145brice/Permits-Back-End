#!/bin/bash
# Contractor Leads Backend - Development Startup Script
# Starts both servers: Permits API (8081) and Admin+Frontend (8082)

echo "🚀 Starting Contractor Leads Backend Servers..."
echo ""

# Function to start a server in background
start_server() {
    local port=$1
    local script=$2
    local name=$3

    echo "📡 Starting $name server on port $port..."
    python3 $script --port=$port &
    local pid=$!
    echo "✅ $name server started (PID: $pid)"
    echo ""
}

# Start Permits API (app.py) on port 8081
start_server 8081 app.py "Permits API"

# Wait a moment for first server to start
sleep 2

# Start Admin + Frontend server (backend.py) on port 8082
start_server 8082 backend.py "Admin + Frontend"

echo "🎉 Both servers are running!"
echo "   📊 Admin Dashboard: http://localhost:8082/admin"
echo "   🔗 Frontend: http://localhost:8082/"
echo "   🔧 API Health: http://localhost:8081/health"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap 'echo ""; echo "🛑 Stopping servers..."; pkill -f "python3 app.py"; pkill -f "python3 backend.py"; echo "✅ All servers stopped"; exit 0' INT

# Keep script running
wait