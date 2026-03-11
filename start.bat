@echo off
REM Dhritrashtra Development Environment Startup Script

echo 🚀 Starting Dhritrashtra Development Environment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

REM Create .env files if they don't exist
if not exist "backend\.env" (
    copy backend\.env.example backend\.env
    echo ✅ Created backend\.env
)

if not exist "frontend\.env" (
    copy frontend\.env.example frontend\.env
    echo ✅ Created frontend\.env
)

REM Start Docker containers
echo 🐳 Starting Docker containers...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak

REM Check services
echo ✅ Services started!
echo.
echo 📊 Dhritrashtra is running:
echo    Backend API: http://localhost:5000
echo    Frontend:   http://localhost:3000
echo    Database:   localhost:5432
echo.
echo 📝 Logs:
echo    docker-compose logs -f
echo.
echo ❌ To stop:
echo    docker-compose down
