#!/bin/bash
# Setup script for AI Repository Scanner v2

echo "🚀 AI Repository Scanner v2 Setup"
echo "================================="

# Check Python version
echo -n "Checking Python version... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "Python $PYTHON_VERSION found ✓"
else
    echo "Python 3 not found ✗"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Install Python dependencies
echo -e "\nInstalling Python dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt

# Check if TruffleHog is installed
echo -e "\nChecking TruffleHog installation..."
if command -v trufflehog &> /dev/null; then
    TRUFFLEHOG_VERSION=$(trufflehog --version 2>&1 | head -n1)
    echo "TruffleHog found: $TRUFFLEHOG_VERSION ✓"
else
    echo "TruffleHog not found ✗"
    echo ""
    echo "Would you like to install TruffleHog now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Installing TruffleHog..."
        if [[ "$OSTYPE" == "darwin"* ]] && command -v brew &> /dev/null; then
            # macOS with Homebrew
            brew install trufflehog
        else
            # Linux/Unix or macOS without Homebrew
            curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
        fi
        
        # Verify installation
        if command -v trufflehog &> /dev/null; then
            echo "TruffleHog installed successfully ✓"
        else
            echo "TruffleHog installation failed ✗"
            echo "Please install manually from: https://github.com/trufflesecurity/trufflehog"
        fi
    else
        echo "Please install TruffleHog manually from: https://github.com/trufflesecurity/trufflehog"
    fi
fi

# Make scripts executable
echo -e "\nMaking scripts executable..."
chmod +x ai_repo_scanner_v2.py
chmod +x demo_ai_scanner.py

# Check for GitHub token
echo -e "\n📋 GitHub Token Setup"
echo "===================="
echo "You'll need a GitHub Personal Access Token to use the scanner."
echo ""
echo "To create one:"
echo "1. Go to https://github.com/settings/tokens"
echo "2. Click 'Generate new token' (classic)"
echo "3. Give it a name (e.g., 'AI Repo Scanner')"
echo "4. Select scopes: 'repo' (for private repos) or 'public_repo' (for public only)"
echo "5. Generate and copy the token"
echo ""
echo "Do you have a GitHub token ready? (y/n)"
read -r has_token

if [[ "$has_token" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Great! You can now run the scanner with:"
    echo "  python3 ai_repo_scanner_v2.py --token YOUR_TOKEN"
    echo ""
    echo "Or try the demo first:"
    echo "  python3 demo_ai_scanner.py"
else
    echo ""
    echo "No problem! Get your token from https://github.com/settings/tokens"
    echo "Then run: python3 ai_repo_scanner_v2.py --token YOUR_TOKEN"
fi

echo -e "\n✅ Setup complete!"
echo ""
echo "Quick Start Commands:"
echo "  • Run demo: python3 demo_ai_scanner.py"
echo "  • Basic scan: python3 ai_repo_scanner_v2.py --token YOUR_TOKEN"
echo "  • Scan 100 repos: python3 ai_repo_scanner_v2.py --token YOUR_TOKEN --max-repos 100"
echo "  • Lower threshold: python3 ai_repo_scanner_v2.py --token YOUR_TOKEN --confidence 30"
echo ""
echo "For more information, see AI_REPO_SCANNER_V2_README.md"