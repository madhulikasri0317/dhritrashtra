#!/bin/bash

echo "🚀 Starting Dhritrashtra Development Environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo "✅ Created frontend/.env"
fi

# Start Docker containers
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check services
echo "✅ Services started!"
echo ""
echo "📊 Dhritrashtra is running:"
echo "   Backend API: http://localhost:5000"
echo "   Frontend:   http://localhost:3000"
echo "   Database:   localhost:5432"
echo ""
echo "📝 Logs:"
echo "   docker-compose logs -f"
echo ""
echo "❌ To stop:"
echo "   docker-compose down"
