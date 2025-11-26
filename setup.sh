#!/bin/bash
# Setup script for Recipe Agent Testing with Scenario
# Works on macOS and Linux (Ubuntu/Debian)

set -e  # Exit on error

echo "=========================================="
echo "Recipe Agent - Setup Script"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected OS: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "Detected OS: macOS"
else
    OS="unknown"
    echo "⚠️  Unknown OS: $OSTYPE"
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo ""
    echo "📦 Installing uv package manager..."
    
    if [ "$OS" == "linux" ]; then
        # Linux installation
        curl -LsSf https://astral.sh/uv/install.sh | sh
        # Add to PATH for current session
        export PATH="$HOME/.cargo/bin:$PATH"
    elif [ "$OS" == "macos" ]; then
        # macOS installation
        if command -v brew &> /dev/null; then
            brew install uv
        else
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        fi
    else
        echo "❌ Please install uv manually: https://github.com/astral-sh/uv"
        exit 1
    fi
    
    # Verify installation
    if ! command -v uv &> /dev/null; then
        echo "⚠️  uv installed but not in PATH. Please add ~/.cargo/bin to your PATH"
        echo "   Run: export PATH=\"\$HOME/.cargo/bin:\$PATH\""
        exit 1
    fi
    
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed"
fi

# Check Python version
echo ""
echo "🐍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "   Found Python $PYTHON_VERSION"
    
    # Check if Python 3.11+
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 11 ]); then
        echo "⚠️  Python 3.11+ required. Found $PYTHON_VERSION"
        echo "   uv will install Python 3.11 automatically if needed"
    fi
else
    echo "⚠️  python3 not found. uv will install Python automatically"
fi

# Initialize project if not already done
if [ ! -f "pyproject.toml" ]; then
    echo ""
    echo "📝 Initializing uv project..."
    uv init -p 3.11 --no-readme
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
uv add langwatch-scenario openai pytest pytest-asyncio python-dotenv

# Create .env from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo "⚠️  Please edit .env and add your API keys"
    else
        echo "⚠️  .env.example not found, skipping .env creation"
    fi
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x run_scenario.py list_models.py 2>/dev/null || true

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run tests: uv run pytest -q"
echo "3. List models: uv run python list_models.py"
echo "4. Run scenario: uv run python run_scenario.py"
echo ""

