# AI Repository Secret Scanner

Advanced Python tool to identify AI-generated GitHub repositories and scan them for secrets using TruffleHog.

## Features

### AI Detection Methods
- **Emoji Analysis**: Detects excessive emoji usage in README files and commit messages
- **GitHub Copilot Indicators**: Identifies repositories with AI assistant usage patterns
- **Commit Burst Analysis**: Detects unusual commit patterns typical of AI generation
- **Metadata Analysis**: Examines repository characteristics and patterns

### Secret Detection
- **TruffleHog Integration**: Scans detected AI repositories for sensitive information
- **Comprehensive Scanning**: Deep analysis of commit history for secrets
- **Detailed Reporting**: JSON output with complete findings

## Installation

### Prerequisites
1. Python 3.7+
2. GitHub Personal Access Token
3. TruffleHog binary

### Install TruffleHog
```bash
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
```

### Install Python Dependencies
```bash
pip install -r ai_scanner_requirements.txt
```

## Usage

### Basic Usage
```bash
python3 ai_repo_secret_scanner.py --token YOUR_GITHUB_TOKEN
```

### Advanced Usage
```bash
python3 ai_repo_secret_scanner.py \
  --token YOUR_GITHUB_TOKEN \
  --query "stars:>50 created:>2023-01-01 language:python" \
  --max-repos 100 \
  --output detailed_scan_results.json
```

### Command Line Options
- `--token`: GitHub Personal Access Token (required)
- `--query`: GitHub search query (default: stars:>10 created:>2023-01-01)
- `--max-repos`: Maximum repositories to scan (default: 50)
- `--trufflehog-path`: Path to TruffleHog binary (default: trufflehog)
- `--output`: Output file for results (default: ai_repo_scan_results.json)

## AI Detection Criteria

### Emoji Analysis
- README files with 10+ emojis
- 30%+ of commits containing emojis
- Unusual emoji density in descriptions

### Copilot Usage Indicators
- References to GitHub Copilot in README
- AI-generated code comments
- Copilot configuration files
- Automated generation mentions

### Commit Patterns
- 20+ commits within 1-hour windows
- Extremely regular commit intervals
- Burst commit patterns typical of automation

### Confidence Scoring
- 0-100% confidence score for AI generation
- Minimum 60% threshold for TruffleHog scanning
- Weighted scoring across all detection methods

## Search Query Examples

### Recent High-Activity Repositories
```bash
--query "stars:>10 created:>2023-01-01 pushed:>2024-01-01"
```

### Specific Languages
```bash
--query "language:python stars:>5 created:>2023-06-01"
```

### Popular Repositories
```bash
--query "stars:>100 forks:>10 created:>2023-01-01"
```

### Recently Updated
```bash
--query "pushed:>2024-01-01 stars:>20"
```

## Output Format

The scanner generates detailed JSON reports with:

### Scan Summary
```json
{
  "scan_summary": {
    "total_scanned": 50,
    "ai_detected": 8,
    "with_secrets": 3
  }
}
```

### AI Repository Details
```json
{
  "repository": "user/repo",
  "ai_confidence": 85.5,
  "emoji_analysis": {
    "readme_count": 15,
    "commit_ratio": 0.4
  },
  "copilot_analysis": {
    "copilot_score": 4,
    "likely_copilot_usage": true
  }
}
```

### Secret Findings
```json
{
  "repository": "user/repo",
  "secrets_found": 3,
  "secrets": [
    {
      "detector": "AWS",
      "verified": true,
      "source_metadata": {...}
    }
  ]
}
```

## GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with these permissions:
   - `public_repo` (for public repository access)
   - `read:org` (for organization repositories)
3. Set token as environment variable or use --token parameter

## Rate Limiting

The scanner handles GitHub API rate limits:
- Monitors remaining requests
- Automatically waits when limits approached
- Respects GitHub's rate limiting policies
- Uses efficient API calls to maximize coverage

## Ethical Usage

This tool is designed for:
- Security research and penetration testing
- Identifying exposed secrets in AI-generated code
- Academic research on AI code generation patterns
- Compliance and security auditing

**Important**: Only scan repositories you own or have permission to test.

## Troubleshooting

### Common Issues

1. **TruffleHog not found**
   ```bash
   curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
   ```

2. **GitHub API rate limit**
   - The scanner automatically handles this
   - Consider using multiple tokens for large scans

3. **Permission errors**
   - Ensure your token has appropriate permissions
   - Some repositories may be private or restricted

4. **Memory issues with large scans**
   - Reduce --max-repos value
   - Use more specific search queries

## Performance Tips

- Use specific search queries to target relevant repositories
- Start with smaller --max-repos values for testing
- Monitor GitHub API rate limits
- Run during off-peak hours for better performance
- Use SSD storage for temporary TruffleHog files

## Security Considerations

- Never commit GitHub tokens to repositories
- Use environment variables for sensitive data
- Review scan results before sharing
- Be respectful of repository owners and GitHub's terms of service