#!/bin/bash
echo "========================================"
echo "Image to Desmos - Setup Script"
echo "========================================"
echo ""

echo "[1/3] Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..
echo ""

echo "[2/3] Installing Node.js dependencies..."
cd frontend
npm install
cd ..
echo ""

echo "[3/3] Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p backend/output
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "1. Run ./start-backend.sh in one terminal"
echo "2. Run ./start-frontend.sh in another terminal"
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "Note: You may need to make the scripts executable:"
echo "  chmod +x start-backend.sh start-frontend.sh setup.sh"
echo ""
