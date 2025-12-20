#!/bin/bash

# MIND Dashboard Quick Start Script
# Sets up the local environment and runs the application

echo "=============================================="
echo "MIND Dashboard - Quick Start"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Check if secrets file exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  WARNING: .streamlit/secrets.toml not found!"
    echo ""
    echo "Please configure your secrets:"
    echo "1. Copy .streamlit/secrets.toml.example to .streamlit/secrets.toml"
    echo "2. Edit .streamlit/secrets.toml with your BigQuery credentials"
    echo ""
    echo "Run: cp .streamlit/secrets.toml.example .streamlit/secrets.toml"
    echo ""
    read -p "Press Enter to continue anyway (app will fail without secrets)..."
fi

echo ""
echo "🚀 Starting MIND Dashboard..."
echo ""
echo "The dashboard will open in your browser at: http://localhost:8501"
echo ""
echo "Default credentials:"
echo "  Admin:     admin / admin123"
echo "  Faculty:   faculty / faculty123"
echo "  Developer: developer / dev123"
echo "  Student:   student / student123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=============================================="
echo ""

# Run Streamlit
streamlit run app.py
