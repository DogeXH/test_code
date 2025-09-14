# AI Repository Secret Scanner v2.0

An advanced tool for detecting AI-generated GitHub repositories and scanning them for exposed secrets using TruffleHog.

## 🚀 Key Improvements Over v1

- **Removed hardcoded date filters** - No more 2023 limitation
- **Advanced search strategies** - Multiple search patterns to find AI-generated repos
- **Enhanced AI detection** - More sophisticated pattern analysis and scoring
- **Better burst detection** - Improved commit pattern analysis
- **Parallel processing** - Faster scanning with concurrent analysis
- **Detailed confidence scoring** - Clear reasons for AI detection
- **Comprehensive logging** - Better visibility into the scanning process

## 🔍 Detection Methods

### 1. **Advanced Search Strategies**
- Direct AI tool mentions (Copilot, ChatGPT, Claude, etc.)
- Emoji patterns common in AI-generated content
- Common AI project templates (todo apps, calculators, portfolios)
- Rapid development indicators

### 2. **Emoji Analysis**
- Excessive emoji usage in README files
- High emoji density per word/character
- Emoji patterns in commit messages
- Multiple unique emojis (AI tends to use variety)

### 3. **Commit Pattern Analysis**
- Burst detection (many commits in short timeframes)
- Perfect timing patterns (commits exactly 1, 2, 5 minutes apart)
- Generic/repetitive commit messages
- Rapid consecutive commits

### 4. **AI Tool Indicators**
- Copilot configuration files
- AI-related comments in code
- README mentions of AI tools
- AI-specific metadata files

### 5. **Repository Metadata**
- Rapid development (repo completed in hours)
- Template-like structure
- Low engagement despite complete features
- AI-related topics/tags

## 📋 Prerequisites

1. **Python 3.7+**
2. **GitHub Personal Access Token** with repo read permissions
3. **TruffleHog** installed

### Installing TruffleHog

```bash
# Option 1: Using install script (recommended)
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# Option 2: Using Homebrew (macOS)
brew install trufflehog

# Option 3: Download binary from releases
# https://github.com/trufflesecurity/trufflehog/releases
```

## 🛠️ Installation

1. Clone or download the scanner:
```bash
git clone <repository>
cd ai-repo-scanner
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Verify TruffleHog installation:
```bash
trufflehog --version
```

## 🚀 Usage

### Basic Usage
```bash
python ai_repo_scanner_v2.py --token YOUR_GITHUB_TOKEN
```

### Advanced Options
```bash
# Scan more repositories
python ai_repo_scanner_v2.py --token YOUR_GITHUB_TOKEN --max-repos 100

# Lower confidence threshold (default: 40%)
python ai_repo_scanner_v2.py --token YOUR_GITHUB_TOKEN --confidence 30

# Custom TruffleHog path
python ai_repo_scanner_v2.py --token YOUR_GITHUB_TOKEN --trufflehog-path /path/to/trufflehog

# Custom output file
python ai_repo_scanner_v2.py --token YOUR_GITHUB_TOKEN --output results.json
```

### Command Line Arguments
- `--token` (required): GitHub Personal Access Token
- `--max-repos`: Maximum repositories to scan (default: 50)
- `--confidence`: Minimum AI confidence threshold in % (default: 40)
- `--trufflehog-path`: Path to TruffleHog binary (default: trufflehog)
- `--output`: Output file for results (default: ai_repo_scan_results_v2.json)

## 📊 Output

The scanner generates two output files:

1. **JSON Results** (`ai_repo_scan_results_v2.json`):
   - Complete analysis data
   - AI confidence scores and reasons
   - Secret findings with details
   - Detection statistics

2. **CSV Summary** (`ai_repo_scan_results_v2_summary.csv`):
   - Quick overview of findings
   - Repository URLs
   - AI confidence scores
   - Secret counts and types

## 🎯 AI Confidence Scoring

The scanner calculates an AI confidence score (0-100%) based on:

- **Emoji Usage** (20% weight)
  - Excessive emojis in README
  - High emoji-to-word ratio
  - Emoji usage in commits

- **Commit Patterns** (35% weight)
  - Burst commits (many in short time)
  - Perfect timing intervals
  - Generic/repetitive messages
  - Suspicious patterns

- **AI Indicators** (30% weight)
  - Direct mentions of AI tools
  - AI configuration files
  - AI-generated comments
  - Common AI project patterns

- **Metadata** (15% weight)
  - Rapid development time
  - Template indicators
  - Low engagement metrics

## 🔍 Search Strategies

The scanner uses multiple search strategies to find AI-generated repositories:

1. Direct AI mentions in README files
2. Common AI project patterns (todo apps, calculators, etc.)
3. Emoji-heavy repositories
4. Recently created repos with rapid development
5. Repositories with AI-related topics/tags

## ⚠️ Important Notes

1. **API Rate Limits**: The scanner respects GitHub API rate limits and will pause when necessary
2. **Scan Time**: Scanning takes time due to API limits and TruffleHog analysis
3. **False Positives**: Some human-created repos may be flagged - review results carefully
4. **Verified Secrets Only**: TruffleHog is configured to show only verified secrets

## 🐛 Troubleshooting

### TruffleHog not found
```bash
# Install TruffleHog using the install script
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
```

### Rate limit errors
- Wait for rate limit reset (scanner handles this automatically)
- Use a token with higher rate limits
- Reduce `--max-repos` parameter

### No results found
- Try lowering the `--confidence` threshold
- Check if your token has proper permissions
- Verify network connectivity

## 📈 Example Output

```
🤖 AI REPOSITORY SECRET SCANNER v2.0
================================================================================
Searching for AI-generated repositories and scanning for secrets...
Max repos: 50 | Confidence threshold: 40%
================================================================================

INFO: Starting advanced repository search with multiple strategies
INFO: Searching with strategy: "built with copilot" in:readme
INFO: Found 15 repositories, total unique: 15
...

🤖 AI DETECTED: AI-Generated Repository Detected! user/todo-app (Confidence: 75.0%)
  → Excessive emoji usage in README
  → Commit bursts detected (2 bursts)
  → Multiple AI indicators found (score: 8)

INFO: Running TruffleHog scan on: https://github.com/user/todo-app
🔐 CRITICAL: SECRETS FOUND: 3 secrets in user/todo-app
  → AWS in config.js:45
  → Slack in .env:12
  → GitHub in deploy.yml:23

================================================================================
📊 FINAL SUMMARY
================================================================================
Total Repositories Scanned: 50
AI-Generated Repositories: 12
Average AI Confidence: 62.3%
Repositories with Secrets: 4

🔐 REPOSITORIES WITH SECRETS:

1. user/todo-app
   URL: https://github.com/user/todo-app
   Secrets: 3
   Types: AWS, Slack, GitHub
   AI Confidence: 75.0%

✅ Full results saved to: ai_repo_scan_results_v2.json
```

## 🔒 Security Considerations

- Keep your GitHub token secure
- Review found secrets carefully before taking action
- This tool is for security research and testing only
- Always respect repository privacy and terms of service

## 📝 License

This tool is for educational and security research purposes only. Use responsibly and in accordance with GitHub's Terms of Service.

---
Created by HAYA Security Team