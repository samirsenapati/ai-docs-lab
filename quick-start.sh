#!/bin/bash
# Quick Start Script for AI Docs Lab
# This script automates the initial setup process

set -e  # Exit on any error

echo "🚀 AI Docs Lab - Quick Start Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python is available
echo "1. Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
echo ""
echo "2. Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 is available"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_success "pip is available"
    PIP_CMD="pip"
else
    print_error "pip is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
echo ""
echo "3. Setting up virtual environment..."
if [ ! -d "ai-docs-env" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv ai-docs-env
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source ai-docs-env/bin/activate
print_success "Virtual environment activated"

# Install dependencies
echo ""
echo "4. Installing dependencies..."
if [ -f "requirements.txt" ]; then
    print_info "Installing from requirements.txt..."
    $PIP_CMD install -r requirements.txt
    print_success "Dependencies installed"
else
    print_info "Installing core dependencies..."
    $PIP_CMD install openai httpx mkdocs mkdocs-material
    print_success "Core dependencies installed"
fi

# Create necessary directories
echo ""
echo "5. Creating directory structure..."
mkdir -p docs/generated
mkdir -p docs/drafts
mkdir -p logs
print_success "Directories created"

# Check for OpenAI API key
echo ""
echo "6. Checking OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    print_warning "OpenAI API key not found in environment"
    echo ""
    echo "To set your API key, run one of these commands:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    echo "  echo 'export OPENAI_API_KEY=\"your-api-key-here\"' >> ~/.bashrc"
    echo ""
    print_info "You can get an API key from: https://platform.openai.com"
else
    MASKED_KEY="${OPENAI_API_KEY:0:8}...${OPENAI_API_KEY: -4}"
    print_success "OpenAI API key found: $MASKED_KEY"
fi

# Create sample log file
echo ""
echo "7. Creating sample log file..."
cat > logs/sample.log << 'EOF'
2024-01-15 10:30:22 INFO Application started successfully
2024-01-15 10:30:25 ERROR Database connection failed - timeout after 30s
2024-01-15 10:30:26 WARN Retrying database connection in 5 seconds
2024-01-15 10:30:31 INFO Database connection restored
2024-01-15 10:30:32 ERROR Failed to process user request - invalid token
2024-01-15 10:30:33 WARN High memory usage detected: 85%
2024-01-15 10:30:34 INFO System performance normalized
EOF
print_success "Sample log file created"

# Test the installation
echo ""
echo "8. Testing installation..."
if [ -f "scripts/setup_test.py" ]; then
    print_info "Running comprehensive test suite..."
    python scripts/setup_test.py
else
    print_info "Running basic tests..."
    
    # Test math utilities
    python3 -c "
from src.example import add, multiply
print('✅ Math utilities test passed:', add(5, 3), multiply(4, 6))
" && print_success "Math utilities work correctly"
    
    # Test log extraction
    python scripts/extract_logs.py && print_success "Log extraction works"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your AI Docs Lab installation is ready! Here's what you can do next:"
echo ""
echo "1. 📖 Start the documentation server:"
echo "   mkdocs serve"
echo "   Then visit: http://127.0.0.1:8000"
echo ""
echo "2. 🔄 Run the complete pipeline:"
echo "   python scripts/extract_logs.py"
echo "   python scripts/gen_llm.py  # (requires OpenAI API key)"
echo ""
echo "3. 🧪 Test your setup:"
echo "   python scripts/setup_test.py"
echo ""
echo "4. 📚 Read the documentation:"
echo "   - Installation Guide: docs/installation-guide.md"
echo "   - API Documentation: docs/api-documentation.md"
echo ""

if [ -z "$OPENAI_API_KEY" ]; then
    print_warning "Remember to set your OpenAI API key to use AI report generation!"
fi

echo ""
print_success "Happy documenting! 🚀"

# Keep the virtual environment activated for the user
echo ""
echo "💡 Virtual environment is activated. To deactivate later, run: deactivate"