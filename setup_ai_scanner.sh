#!/bin/bash
"""
AI Repository Scanner - Setup Script
====================================
Automated setup for the AI Repository Secret Scanner

This script will:
1. Check Python installation
2. Install required dependencies
3. Download and install TruffleHog
4. Verify GitHub token setup
5. Run basic functionality tests

Author: HAYA Security Team
"""

set -e

echo "🤖 AI Repository Scanner Setup"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python installation
check_python() {
    log_info "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python 3 found: $PYTHON_VERSION"
        
        # Check if version is 3.7+
        if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)"; then
            log_success "Python version is compatible (3.7+)"
        else
            log_error "Python 3.7+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python 3 not found. Please install Python 3.7+"
        exit 1
    fi
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if [ -f "ai_scanner_requirements.txt" ]; then
        pip3 install -r ai_scanner_requirements.txt
        log_success "Python dependencies installed"
    else
        log_warning "requirements.txt not found, installing basic dependencies"
        pip3 install requests urllib3
    fi
}

# Install TruffleHog
install_trufflehog() {
    log_info "Checking TruffleHog installation..."
    
    if command -v trufflehog &> /dev/null; then
        TRUFFLEHOG_VERSION=$(trufflehog --version | head -n1)
        log_success "TruffleHog already installed: $TRUFFLEHOG_VERSION"
    else
        log_info "Installing TruffleHog..."
        
        # Download and install TruffleHog
        curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
        
        # Verify installation
        if command -v trufflehog &> /dev/null; then
            log_success "TruffleHog installed successfully"
        else
            log_error "TruffleHog installation failed"
            log_info "Try manual installation:"
            log_info "  curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin"
            exit 1
        fi
    fi
}

# Check GitHub token
check_github_token() {
    log_info "Checking GitHub token setup..."
    
    if [ -n "$GITHUB_TOKEN" ]; then
        log_success "GITHUB_TOKEN environment variable is set"
        
        # Test token validity
        RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | jq -r '.login // "error"')
        
        if [ "$RESPONSE" != "error" ] && [ "$RESPONSE" != "null" ]; then
            log_success "GitHub token is valid for user: $RESPONSE"
        else
            log_warning "GitHub token may be invalid or expired"
        fi
    else
        log_warning "GITHUB_TOKEN environment variable not set"
        log_info "To set your token:"
        log_info "  export GITHUB_TOKEN='your_token_here'"
        log_info "  # Or add to your ~/.bashrc or ~/.zshrc"
        log_info ""
        log_info "Get a token from: https://github.com/settings/tokens"
        log_info "Required permissions: public_repo, read:org"
    fi
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Check if main script exists
    if [ -f "ai_repo_secret_scanner.py" ]; then
        log_success "Main scanner script found"
        
        # Test basic import
        if python3 -c "from ai_repo_secret_scanner import AIRepoSecretScanner" &> /dev/null; then
            log_success "Python script imports successfully"
        else
            log_error "Python script has import errors"
            return 1
        fi
    else
        log_error "ai_repo_secret_scanner.py not found"
        return 1
    fi
    
    # Check demo script
    if [ -f "ai_scanner_demo.py" ]; then
        log_success "Demo script available"
    fi
    
    # Check documentation
    if [ -f "AI_REPO_SCANNER_README.md" ]; then
        log_success "Documentation available"
    fi
    
    log_success "Installation verification complete"
}

# Create basic configuration
create_config() {
    log_info "Creating configuration template..."
    
    cat > ai_scanner_config.json << 'EOF'
{
    "ai_thresholds": {
        "emoji_count_readme": 10,
        "emoji_commit_ratio": 0.3,
        "commit_burst_threshold": 20,
        "commit_burst_window": 3600,
        "copilot_indicators": 3,
        "min_confidence_score": 60
    },
    "default_queries": [
        "stars:>10 created:>2023-01-01",
        "language:python stars:>5 created:>2023-06-01",
        "language:javascript stars:>5 created:>2023-06-01"
    ],
    "scan_settings": {
        "max_repos_per_scan": 50,
        "rate_limit_delay": 1,
        "timeout_seconds": 300
    }
}
EOF
    
    log_success "Configuration template created: ai_scanner_config.json"
}

# Run basic test
run_basic_test() {
    if [ -z "$GITHUB_TOKEN" ]; then
        log_warning "Skipping basic test - no GitHub token set"
        return 0
    fi
    
    log_info "Running basic functionality test..."
    
    # Create a minimal test
    python3 -c "
from ai_repo_secret_scanner import AIRepoSecretScanner
import os

token = os.getenv('GITHUB_TOKEN')
if token:
    scanner = AIRepoSecretScanner(token)
    print('✅ Scanner initialized successfully')
    
    # Test API connectivity
    repos = scanner.search_repositories('stars:>1000', max_results=1)
    if repos:
        print(f'✅ API connectivity test passed - found {len(repos)} repository')
    else:
        print('⚠️  API connectivity test failed')
else:
    print('⚠️  No GitHub token for testing')
"
    
    if [ $? -eq 0 ]; then
        log_success "Basic functionality test passed"
    else
        log_warning "Basic functionality test had issues"
    fi
}

# Print usage instructions
print_usage() {
    echo ""
    echo "🎉 Setup complete! Here's how to use the AI Repository Scanner:"
    echo ""
    echo "Basic usage:"
    echo "  python3 ai_repo_secret_scanner.py --token \$GITHUB_TOKEN"
    echo ""
    echo "Advanced usage:"
    echo "  python3 ai_repo_secret_scanner.py \\"
    echo "    --token \$GITHUB_TOKEN \\"
    echo "    --query 'stars:>10 created:>2023-01-01 language:python' \\"
    echo "    --max-repos 50 \\"
    echo "    --output results.json"
    echo ""
    echo "Run demo:"
    echo "  python3 ai_scanner_demo.py"
    echo ""
    echo "Read documentation:"
    echo "  less AI_REPO_SCANNER_README.md"
    echo ""
    echo "Configuration file: ai_scanner_config.json"
    echo ""
}

# Main execution
main() {
    echo ""
    log_info "Starting AI Repository Scanner setup..."
    echo ""
    
    check_python
    install_python_deps
    install_trufflehog
    check_github_token
    create_config
    verify_installation
    run_basic_test
    
    echo ""
    log_success "🎉 AI Repository Scanner setup completed successfully!"
    print_usage
}

# Run main function
main "$@"