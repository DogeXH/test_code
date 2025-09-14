#!/usr/bin/env python3
"""
AI-Generated Repository Secret Scanner v2.0
==========================================
Advanced tool to identify AI-generated GitHub repositories and scan them for secrets using TruffleHog.

Improvements over v1:
- Removed hardcoded date filters
- Enhanced AI detection algorithms
- Better search strategies for finding AI-generated repos
- More sophisticated pattern analysis
- Improved scoring system

Author: HAYA Security Team
"""

import requests
import subprocess
import re
import json
import time
import sys
import os
import base64
import argparse
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from urllib3.exceptions import InsecureRequestWarning
import statistics
from typing import List, Dict, Tuple, Optional, Set
import tempfile
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AIRepoScanner:
    def __init__(self, github_token: str, trufflehog_path: str = "trufflehog"):
        self.github_token = github_token
        self.trufflehog_path = trufflehog_path
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'AI-Repo-Scanner-v2-HAYA/2.0'
        })
        
        # Enhanced rate limiting
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = time.time() + 3600
        
        # Advanced AI detection thresholds
        self.AI_THRESHOLDS = {
            'emoji_count_readme': 5,              # Lowered for better detection
            'emoji_density_readme': 0.01,         # Emojis per character
            'emoji_commit_ratio': 0.15,           # Ratio of commits with emojis
            'commit_burst_threshold': 10,         # Commits in burst
            'commit_burst_window': 1800,          # 30 minutes
            'rapid_commit_interval': 60,          # Seconds between commits
            'copilot_indicators': 1,              # Number of copilot indicators
            'min_confidence_score': 40,           # Minimum AI confidence %
            'creation_to_first_commit': 600,      # 10 minutes
            'perfect_timing_ratio': 0.4,          # Ratio of perfectly timed commits
            'repo_completion_hours': 24,          # Hours from first to last commit
            'file_creation_burst': 15,            # Files created in short time
            'ai_pattern_score': 3,                # AI pattern indicators needed
            'readme_ai_keywords': 2,              # AI-related keywords in README
        }
        
        # Comprehensive emoji pattern
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F700-\U0001F77F"  # alchemical symbols
            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U000024C2-\U0001F251"
            u"\U00002600-\U000026FF"  # Miscellaneous Symbols
            u"\U00002700-\U000027BF"  # Dingbats
            "]+", flags=re.UNICODE)
        
        # Enhanced AI/Copilot indicators
        self.ai_indicators = {
            'copilot': [
                r'github\.com/features/copilot',
                r'copilot.*generated',
                r'ai.*assistant',
                r'generated.*by.*copilot',
                r'copilot.*suggestion',
                r'with.*copilot',
                r'powered.*by.*copilot',
            ],
            'ai_tools': [
                r'chatgpt',
                r'openai',
                r'gpt-[34]',
                r'claude',
                r'anthropic',
                r'bard',
                r'ai.*generated',
                r'automatically.*generated',
                r'generated.*automatically',
                r'machine.*generated',
                r'bot.*generated',
            ],
            'ai_comments': [
                r'//.*generated.*by.*ai',
                r'#.*generated.*by.*ai',
                r'/\*.*ai.*generated.*\*/',
                r'<!--.*ai.*generated.*-->',
                r'""".*generated.*by.*"""',
            ],
            'readme_patterns': [
                r'built.*with.*ai',
                r'created.*using.*ai',
                r'generated.*by.*ai',
                r'made.*with.*❤️.*and.*ai',
                r'🤖.*generated',
                r'✨.*ai.*powered',
                r'🚀.*built.*fast',
            ]
        }
        
        # Common AI-generated project patterns
        self.ai_project_patterns = [
            r'todo.*app',
            r'weather.*app',
            r'calculator.*app',
            r'portfolio.*website',
            r'blog.*platform',
            r'chat.*application',
            r'expense.*tracker',
            r'note.*taking.*app',
            r'task.*manager',
            r'quiz.*app',
        ]
        
        # Search queries for finding AI-generated repos
        self.search_strategies = [
            # Direct AI mentions
            '"built with copilot" in:readme',
            '"generated by ai" in:readme',
            '"created with chatgpt" in:readme',
            '"made with claude" in:readme',
            '"ai generated" in:readme',
            '"copilot generated" in:file',
            
            # Common AI project patterns with emojis
            '✨ app in:readme stars:>5',
            '🚀 built in:readme created:>2024-01-01',
            '🤖 project in:readme',
            '💻 simple in:readme',
            
            # Rapid development indicators
            'created:>2024-01-01 pushed:>2024-01-01 stars:>10',
            'todo app in:readme created:>2024-01-01',
            'portfolio website in:readme created:>2024-01-01',
            'calculator app in:readme created:>2024-01-01',
            
            # Multiple emoji patterns
            '✨ 🚀 in:readme',
            '💡 ⚡ in:readme',
            '🎯 🔥 in:readme',
            
            # Generic but with recent activity
            'awesome in:readme stars:5..50 pushed:>2024-01-01',
            'simple in:readme stars:3..30 created:>2024-01-01',
        ]
        
        self.results = {
            'scanned_repos': 0,
            'ai_detected_repos': [],
            'secrets_found': [],
            'scan_timestamp': datetime.now().isoformat(),
            'detection_stats': defaultdict(int)
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def log(self, message: str, level: str = "INFO"):
        """Enhanced logging with colors"""
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[95m",
            "AI_DETECTED": "\033[96m"
        }
        reset = "\033[0m"
        
        if level == "AI_DETECTED":
            print(f"{colors.get(level, '')}🤖 AI DETECTED: {message}{reset}")
        else:
            print(f"{colors.get(level, '')}{level}: {message}{reset}")

    def check_rate_limit(self):
        """Check and handle GitHub API rate limiting"""
        if self.rate_limit_remaining <= 100:
            wait_time = max(0, self.rate_limit_reset - time.time()) + 60
            self.log(f"Rate limit low ({self.rate_limit_remaining}), waiting {wait_time:.0f} seconds", "WARNING")
            time.sleep(wait_time)
            
    def update_rate_limit(self, response):
        """Update rate limit info from response headers"""
        if 'X-RateLimit-Remaining' in response.headers:
            self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
        if 'X-RateLimit-Reset' in response.headers:
            self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])

    def search_repositories_advanced(self, max_results: int = 100) -> List[Dict]:
        """Advanced repository search using multiple strategies"""
        self.log("Starting advanced repository search with multiple strategies")
        all_repositories = {}  # Use dict to avoid duplicates
        
        for strategy in self.search_strategies[:10]:  # Limit strategies to avoid rate limits
            try:
                self.log(f"Searching with strategy: {strategy}")
                repos = self._search_github(strategy, max_results=30)  # Limit per strategy
                
                for repo in repos:
                    repo_key = repo['full_name']
                    if repo_key not in all_repositories:
                        all_repositories[repo_key] = repo
                        
                self.log(f"Found {len(repos)} repositories, total unique: {len(all_repositories)}")
                
                if len(all_repositories) >= max_results:
                    break
                    
                time.sleep(2)  # Rate limit protection
                
            except Exception as e:
                self.log(f"Error with search strategy '{strategy}': {str(e)}", "WARNING")
                continue
        
        # Convert back to list and limit results
        repositories = list(all_repositories.values())[:max_results]
        self.log(f"Total unique repositories found: {len(repositories)}")
        
        return repositories

    def _search_github(self, query: str, max_results: int = 100) -> List[Dict]:
        """Execute a single GitHub search query"""
        repositories = []
        page = 1
        per_page = min(100, max_results)
        
        while len(repositories) < max_results:
            self.check_rate_limit()
            
            params = {
                'q': query,
                'sort': 'updated',
                'order': 'desc',
                'per_page': per_page,
                'page': page
            }
            
            try:
                response = self.session.get('https://api.github.com/search/repositories', params=params)
                self.update_rate_limit(response)
                
                if response.status_code == 200:
                    data = response.json()
                    repos = data.get('items', [])
                    
                    if not repos:
                        break
                        
                    repositories.extend(repos)
                    page += 1
                    
                elif response.status_code == 403:
                    self.log("Rate limit exceeded, waiting...", "WARNING")
                    time.sleep(300)
                    continue
                else:
                    break
                    
            except Exception as e:
                self.log(f"Search error: {str(e)}", "ERROR")
                break
                
        return repositories[:max_results]

    def get_repository_details(self, owner: str, repo: str) -> Optional[Dict]:
        """Get detailed repository information"""
        self.check_rate_limit()
        
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}'
            response = self.session.get(url)
            self.update_rate_limit(response)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            self.log(f"Error getting repo details: {str(e)}", "ERROR")
            
        return None

    def get_repository_content(self, owner: str, repo: str, path: str = '') -> Optional[str]:
        """Get repository file content"""
        self.check_rate_limit()
        
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
            response = self.session.get(url)
            self.update_rate_limit(response)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return None  # Directory listing
                    
                if data.get('encoding') == 'base64':
                    content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                    return content
                    
        except Exception as e:
            self.log(f"Error getting content: {str(e)}", "ERROR")
            
        return None

    def get_commits(self, owner: str, repo: str, limit: int = 100) -> List[Dict]:
        """Get repository commits with enhanced error handling"""
        self.check_rate_limit()
        commits = []
        
        try:
            url = f'https://api.github.com/repos/{owner}/{repo}/commits'
            params = {'per_page': min(100, limit)}
            
            response = self.session.get(url, params=params)
            self.update_rate_limit(response)
            
            if response.status_code == 200:
                commits = response.json()
                
        except Exception as e:
            self.log(f"Error getting commits: {str(e)}", "ERROR")
            
        return commits[:limit]

    def analyze_emoji_usage_advanced(self, text: str) -> Dict:
        """Advanced emoji analysis with density calculations"""
        if not text:
            return {
                'count': 0, 
                'unique_count': 0,
                'emojis': [], 
                'density': 0.0,
                'per_word': 0.0,
                'excessive': False
            }
            
        emojis = self.emoji_pattern.findall(text)
        emoji_count = len(emojis)
        unique_emojis = list(set(emojis))
        text_length = len(text)
        word_count = len(text.split())
        
        # Calculate various metrics
        density = emoji_count / max(text_length, 1)
        per_word = emoji_count / max(word_count, 1)
        
        # Check if emoji usage is excessive (common in AI-generated content)
        excessive = (
            emoji_count > 10 or
            density > 0.01 or
            per_word > 0.05 or
            len(unique_emojis) > 5
        )
        
        return {
            'count': emoji_count,
            'unique_count': len(unique_emojis),
            'emojis': unique_emojis[:10],  # Limit for display
            'density': density,
            'per_word': per_word,
            'excessive': excessive
        }

    def analyze_commit_patterns_advanced(self, commits: List[Dict]) -> Dict:
        """Advanced commit pattern analysis"""
        if not commits:
            return {
                'burst_detected': False,
                'burst_details': [],
                'perfect_timing_ratio': 0,
                'rapid_commits': 0,
                'emoji_commit_ratio': 0,
                'suspicious_patterns': [],
                'ai_confidence_boost': 0
            }
            
        timestamps = []
        emoji_commits = 0
        commit_messages = []
        
        for commit in commits:
            try:
                commit_date = datetime.strptime(
                    commit['commit']['author']['date'], 
                    '%Y-%m-%dT%H:%M:%SZ'
                )
                timestamps.append(commit_date)
                
                message = commit['commit']['message']
                commit_messages.append(message)
                
                if self.emoji_pattern.search(message):
                    emoji_commits += 1
                    
            except Exception:
                continue
                
        if len(timestamps) < 2:
            return {
                'burst_detected': False,
                'burst_details': [],
                'perfect_timing_ratio': 0,
                'rapid_commits': 0,
                'emoji_commit_ratio': emoji_commits / len(commits) if commits else 0,
                'suspicious_patterns': [],
                'ai_confidence_boost': 0
            }
            
        timestamps.sort()
        
        # Analyze commit intervals
        intervals = []
        rapid_commits = 0
        perfect_timing_count = 0
        
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
            
            if interval < self.AI_THRESHOLDS['rapid_commit_interval']:
                rapid_commits += 1
                
            # Check for suspiciously perfect timing (e.g., exactly 1 minute apart)
            if interval in [60, 120, 180, 300, 600]:  # Common AI intervals
                perfect_timing_count += 1
        
        # Detect bursts
        bursts = []
        current_burst = [timestamps[0]]
        
        for i in range(1, len(timestamps)):
            time_diff = (timestamps[i] - timestamps[i-1]).total_seconds()
            
            if time_diff < self.AI_THRESHOLDS['commit_burst_window']:
                current_burst.append(timestamps[i])
            else:
                if len(current_burst) >= self.AI_THRESHOLDS['commit_burst_threshold']:
                    bursts.append({
                        'size': len(current_burst),
                        'duration': (current_burst[-1] - current_burst[0]).total_seconds(),
                        'start': current_burst[0].isoformat()
                    })
                current_burst = [timestamps[i]]
                
        # Check last burst
        if len(current_burst) >= self.AI_THRESHOLDS['commit_burst_threshold']:
            bursts.append({
                'size': len(current_burst),
                'duration': (current_burst[-1] - current_burst[0]).total_seconds(),
                'start': current_burst[0].isoformat()
            })
        
        # Analyze suspicious patterns
        suspicious_patterns = []
        
        # Check for too many similar commit messages
        message_counts = Counter(commit_messages)
        for msg, count in message_counts.items():
            if count > 3 and len(msg) > 10:
                suspicious_patterns.append(f"Repeated message: '{msg[:50]}...' ({count} times)")
        
        # Check for generic AI-like messages
        generic_patterns = [
            r'^update\s+\w+$',
            r'^fix\s+\w+$',
            r'^add\s+\w+$',
            r'^initial commit$',
            r'^update readme$',
            r'^fix bug$',
        ]
        
        generic_count = 0
        for msg in commit_messages:
            for pattern in generic_patterns:
                if re.match(pattern, msg.lower()):
                    generic_count += 1
                    break
                    
        if generic_count > len(commits) * 0.3:
            suspicious_patterns.append(f"High ratio of generic messages ({generic_count}/{len(commits)})")
        
        # Calculate AI confidence boost
        ai_confidence_boost = 0
        if bursts:
            ai_confidence_boost += 20
        if perfect_timing_count > len(intervals) * 0.3:
            ai_confidence_boost += 15
        if rapid_commits > len(intervals) * 0.5:
            ai_confidence_boost += 15
        if suspicious_patterns:
            ai_confidence_boost += 10
            
        return {
            'burst_detected': len(bursts) > 0,
            'burst_details': bursts,
            'perfect_timing_ratio': perfect_timing_count / len(intervals) if intervals else 0,
            'rapid_commits': rapid_commits,
            'emoji_commit_ratio': emoji_commits / len(commits) if commits else 0,
            'suspicious_patterns': suspicious_patterns,
            'ai_confidence_boost': ai_confidence_boost
        }

    def detect_ai_indicators(self, owner: str, repo: str) -> Dict:
        """Comprehensive AI/Copilot usage detection"""
        indicators_found = defaultdict(list)
        total_score = 0
        
        # Check README
        for readme_name in ['README.md', 'readme.md', 'README.MD', 'Readme.md']:
            readme_content = self.get_repository_content(owner, repo, readme_name)
            if readme_content:
                # Check all AI indicators
                for category, patterns in self.ai_indicators.items():
                    for pattern in patterns:
                        matches = re.findall(pattern, readme_content, re.IGNORECASE)
                        if matches:
                            indicators_found[category].append({
                                'pattern': pattern,
                                'matches': len(matches),
                                'location': readme_name
                            })
                            total_score += 2
                break
        
        # Check for AI-specific files
        ai_files = [
            '.ai-generated', '.copilot', 'copilot.yml', '.github/copilot.yml',
            'ai-config.json', '.chatgpt', '.claude', '.openai-config'
        ]
        
        for file_path in ai_files:
            content = self.get_repository_content(owner, repo, file_path)
            if content:
                indicators_found['ai_files'].append(file_path)
                total_score += 5
        
        # Check source files for AI comments
        common_files = ['index.js', 'main.py', 'app.py', 'index.ts', 'main.go']
        for file_name in common_files:
            content = self.get_repository_content(owner, repo, file_name)
            if content:
                for pattern in self.ai_indicators['ai_comments']:
                    if re.search(pattern, content, re.IGNORECASE):
                        indicators_found['ai_comments'].append({
                            'file': file_name,
                            'pattern': pattern
                        })
                        total_score += 3
        
        # Check if repo name matches common AI patterns
        repo_name_lower = repo.lower()
        for pattern in self.ai_project_patterns:
            if re.search(pattern, repo_name_lower):
                indicators_found['project_pattern'].append(pattern)
                total_score += 1
        
        return {
            'indicators': dict(indicators_found),
            'total_score': total_score,
            'categories_found': len(indicators_found),
            'likely_ai_generated': total_score >= self.AI_THRESHOLDS['ai_pattern_score']
        }

    def analyze_repository_metadata(self, repo: Dict) -> Dict:
        """Analyze repository metadata for AI indicators"""
        indicators = []
        score = 0
        
        # Check repository description
        description = repo.get('description', '')
        if description:
            emoji_analysis = self.analyze_emoji_usage_advanced(description)
            if emoji_analysis['excessive']:
                indicators.append("Excessive emojis in description")
                score += 10
        
        # Check topics/tags
        topics = repo.get('topics', [])
        ai_topics = ['ai-generated', 'copilot', 'chatgpt', 'automated', 'bot-created']
        for topic in topics:
            if any(ai_topic in topic.lower() for ai_topic in ai_topics):
                indicators.append(f"AI-related topic: {topic}")
                score += 15
        
        # Check creation and update patterns
        created_at = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        updated_at = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        pushed_at = datetime.strptime(repo['pushed_at'], '%Y-%m-%dT%H:%M:%SZ') if repo.get('pushed_at') else updated_at
        
        # Rapid development check
        development_time = (pushed_at - created_at).total_seconds()
        if development_time < 3600 * self.AI_THRESHOLDS['repo_completion_hours']:
            indicators.append(f"Rapid development: {development_time/3600:.1f} hours")
            score += 10
        
        # Check if it's a template-like repo
        if repo.get('is_template'):
            indicators.append("Repository is marked as template")
            score += 5
        
        # Low engagement but complete project
        if repo.get('stargazers_count', 0) < 10 and repo.get('size', 0) > 100:
            indicators.append("Large repo with low engagement")
            score += 5
        
        return {
            'indicators': indicators,
            'metadata_score': score,
            'creation_date': created_at.isoformat(),
            'last_push': pushed_at.isoformat(),
            'development_hours': development_time / 3600
        }

    def calculate_ai_confidence_advanced(self, analysis_results: Dict) -> Tuple[float, List[str]]:
        """Advanced AI confidence calculation with detailed reasoning"""
        confidence = 0.0
        reasons = []
        
        # Emoji analysis (20% weight)
        emoji_data = analysis_results.get('emoji_analysis', {})
        if emoji_data.get('readme_excessive', False):
            confidence += 15
            reasons.append("Excessive emoji usage in README")
        if emoji_data.get('commit_ratio', 0) > self.AI_THRESHOLDS['emoji_commit_ratio']:
            confidence += 5
            reasons.append(f"High emoji ratio in commits ({emoji_data['commit_ratio']:.0%})")
        
        # Commit pattern analysis (35% weight)
        commit_data = analysis_results.get('commit_analysis', {})
        if commit_data.get('burst_detected', False):
            confidence += 20
            reasons.append(f"Commit bursts detected ({len(commit_data.get('burst_details', []))} bursts)")
        if commit_data.get('perfect_timing_ratio', 0) > self.AI_THRESHOLDS['perfect_timing_ratio']:
            confidence += 10
            reasons.append("Suspiciously perfect commit timing")
        if commit_data.get('suspicious_patterns', []):
            confidence += 5
            reasons.append("Suspicious commit patterns found")
        
        # AI indicators (30% weight)
        ai_data = analysis_results.get('ai_indicators', {})
        if ai_data.get('likely_ai_generated', False):
            confidence += 25
            reasons.append(f"Multiple AI indicators found (score: {ai_data.get('total_score', 0)})")
        elif ai_data.get('total_score', 0) > 0:
            confidence += min(15, ai_data.get('total_score', 0) * 3)
            reasons.append("Some AI indicators present")
        
        # Metadata analysis (15% weight)
        metadata = analysis_results.get('metadata_analysis', {})
        if metadata.get('metadata_score', 0) > 10:
            confidence += min(15, metadata.get('metadata_score', 0))
            if metadata.get('indicators', []):
                reasons.append(f"Metadata indicators: {', '.join(metadata['indicators'][:2])}")
        
        # Add confidence boost from commit analysis
        confidence += commit_data.get('ai_confidence_boost', 0)
        
        # Ensure confidence is within bounds
        confidence = min(100, max(0, confidence))
        
        return confidence, reasons

    def analyze_repository(self, repo: Dict) -> Dict:
        """Comprehensive repository analysis for AI detection"""
        owner = repo['owner']['login']
        repo_name = repo['name']
        
        self.log(f"Analyzing repository: {owner}/{repo_name}")
        
        analysis = {
            'repository': f"{owner}/{repo_name}",
            'url': repo['html_url'],
            'created_at': repo['created_at'],
            'stars': repo['stargazers_count'],
            'language': repo.get('language', 'Unknown'),
            'size': repo.get('size', 0)
        }
        
        try:
            # Get README content
            readme_content = None
            for readme_name in ['README.md', 'readme.md', 'README.MD']:
                readme_content = self.get_repository_content(owner, repo_name, readme_name)
                if readme_content:
                    break
            
            # Analyze README emojis
            readme_emoji_analysis = self.analyze_emoji_usage_advanced(readme_content or '')
            
            # Get commits and analyze patterns
            commits = self.get_commits(owner, repo_name, 100)
            commit_analysis = self.analyze_commit_patterns_advanced(commits)
            
            # Detect AI indicators
            ai_indicators = self.detect_ai_indicators(owner, repo_name)
            
            # Analyze repository metadata
            metadata_analysis = self.analyze_repository_metadata(repo)
            
            # Combine analyses
            analysis.update({
                'emoji_analysis': {
                    'readme_excessive': readme_emoji_analysis['excessive'],
                    'readme_count': readme_emoji_analysis['count'],
                    'readme_density': readme_emoji_analysis['density'],
                    'commit_ratio': commit_analysis['emoji_commit_ratio']
                },
                'commit_analysis': commit_analysis,
                'ai_indicators': ai_indicators,
                'metadata_analysis': metadata_analysis
            })
            
            # Calculate confidence score
            confidence, reasons = self.calculate_ai_confidence_advanced(analysis)
            analysis['ai_confidence'] = confidence
            analysis['confidence_reasons'] = reasons
            analysis['is_likely_ai_generated'] = confidence >= self.AI_THRESHOLDS['min_confidence_score']
            
            # Update detection stats
            if analysis['is_likely_ai_generated']:
                for reason in reasons:
                    self.results['detection_stats'][reason] += 1
            
        except Exception as e:
            self.log(f"Error analyzing repository: {str(e)}", "ERROR")
            analysis['error'] = str(e)
            analysis['ai_confidence'] = 0
            analysis['is_likely_ai_generated'] = False
            
        return analysis

    def run_trufflehog_scan(self, repo_url: str) -> Dict:
        """Run TruffleHog scan with improved error handling"""
        self.log(f"Running TruffleHog scan on: {repo_url}")
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_file = os.path.join(temp_dir, 'trufflehog_results.json')
                
                # Run TruffleHog with optimized settings
                cmd = [
                    self.trufflehog_path,
                    'git',
                    repo_url,
                    '--json',
                    '--output', output_file,
                    '--only-verified',  # Only show verified secrets
                    '--concurrency', '4',
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                secrets_found = []
                
                # Parse JSON output
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    with open(output_file, 'r') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    secret_data = json.loads(line.strip())
                                    # Extract relevant information
                                    secrets_found.append({
                                        'detector': secret_data.get('DetectorName', 'Unknown'),
                                        'file': secret_data.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('file', 'Unknown'),
                                        'line': secret_data.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('line', 0),
                                        'commit': secret_data.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('commit', 'Unknown'),
                                        'verified': secret_data.get('Verified', False),
                                        'raw': secret_data.get('Raw', '')[:100] + '...' if len(secret_data.get('Raw', '')) > 100 else secret_data.get('Raw', '')
                                    })
                                except json.JSONDecodeError:
                                    continue
                
                return {
                    'repository': repo_url,
                    'secrets_found': len(secrets_found),
                    'secrets': secrets_found,
                    'scan_successful': True,
                    'error_message': None
                }
                
        except subprocess.TimeoutExpired:
            return {
                'repository': repo_url,
                'secrets_found': 0,
                'secrets': [],
                'scan_successful': False,
                'error_message': 'Scan timeout (5 minutes)'
            }
        except Exception as e:
            return {
                'repository': repo_url,
                'secrets_found': 0,
                'secrets': [],
                'scan_successful': False,
                'error_message': str(e)
            }

    def scan_repositories(self, max_repos: int = 50, confidence_threshold: int = None) -> Dict:
        """Main scanning function with parallel processing"""
        self.log("=== AI Repository Secret Scanner v2.0 Started ===", "SUCCESS")
        self.log(f"Max Repositories: {max_repos}")
        self.log(f"Confidence Threshold: {confidence_threshold or self.AI_THRESHOLDS['min_confidence_score']}%")
        
        # Use advanced search to find repositories
        repositories = self.search_repositories_advanced(max_repos)
        self.log(f"Found {len(repositories)} repositories to analyze")
        
        ai_detected_repos = []
        secrets_summary = []
        
        # Use thread pool for parallel analysis
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_repo = {}
            
            for repo in repositories:
                future = executor.submit(self.analyze_repository, repo)
                future_to_repo[future] = repo
            
            for i, future in enumerate(as_completed(future_to_repo), 1):
                repo = future_to_repo[future]
                
                try:
                    analysis = future.result()
                    self.results['scanned_repos'] += 1
                    
                    # Check confidence threshold
                    threshold = confidence_threshold or self.AI_THRESHOLDS['min_confidence_score']
                    
                    if analysis['ai_confidence'] >= threshold:
                        self.log(
                            f"AI-Generated Repository Detected! {analysis['repository']} "
                            f"(Confidence: {analysis['ai_confidence']:.1f}%)",
                            "AI_DETECTED"
                        )
                        
                        # Log reasons
                        for reason in analysis.get('confidence_reasons', [])[:3]:
                            self.log(f"  → {reason}", "INFO")
                        
                        ai_detected_repos.append(analysis)
                        self.results['ai_detected_repos'].append(analysis)
                        
                        # Run TruffleHog scan
                        trufflehog_results = self.run_trufflehog_scan(repo['html_url'])
                        
                        if trufflehog_results['secrets_found'] > 0:
                            self.log(
                                f"🔐 SECRETS FOUND: {trufflehog_results['secrets_found']} secrets in {repo['full_name']}",
                                "CRITICAL"
                            )
                            
                            # Show first few secrets
                            for secret in trufflehog_results['secrets'][:3]:
                                self.log(
                                    f"  → {secret['detector']} in {secret['file']}:{secret['line']}",
                                    "WARNING"
                                )
                            
                            secrets_summary.append({
                                'repository': repo['full_name'],
                                'url': repo['html_url'],
                                'secrets_count': trufflehog_results['secrets_found'],
                                'ai_confidence': analysis['ai_confidence'],
                                'secret_types': list(set(s['detector'] for s in trufflehog_results['secrets']))
                            })
                            self.results['secrets_found'].append(trufflehog_results)
                        else:
                            self.log(f"No verified secrets found in {repo['full_name']}")
                    else:
                        self.log(
                            f"Repository appears human-generated: {analysis['repository']} "
                            f"(Confidence: {analysis['ai_confidence']:.1f}%)"
                        )
                    
                except Exception as e:
                    self.log(f"Error analyzing {repo.get('full_name', 'unknown')}: {str(e)}", "ERROR")
                    continue
                
                # Progress update
                if i % 10 == 0:
                    self.log(f"Progress: {i}/{len(repositories)} repositories processed")
                    
                # Small delay between scans
                time.sleep(1)
        
        # Generate summary
        self.log("\n" + "="*80, "SUCCESS")
        self.log("SCAN COMPLETE", "SUCCESS")
        self.log("="*80, "SUCCESS")
        self.log(f"Total Repositories Scanned: {self.results['scanned_repos']}")
        self.log(f"AI-Generated Repositories Found: {len(ai_detected_repos)}")
        self.log(f"Repositories with Secrets: {len(secrets_summary)}")
        
        # Show detection statistics
        if self.results['detection_stats']:
            self.log("\nMost Common AI Indicators:", "INFO")
            for indicator, count in sorted(
                self.results['detection_stats'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]:
                self.log(f"  • {indicator}: {count} repos", "INFO")
        
        return {
            'scan_summary': {
                'total_scanned': self.results['scanned_repos'],
                'ai_detected': len(ai_detected_repos),
                'with_secrets': len(secrets_summary),
                'avg_confidence': sum(r['ai_confidence'] for r in ai_detected_repos) / len(ai_detected_repos) if ai_detected_repos else 0
            },
            'ai_repositories': ai_detected_repos,
            'secrets_summary': secrets_summary,
            'detection_stats': dict(self.results['detection_stats']),
            'full_results': self.results
        }

    def save_results(self, results: Dict, output_file: str):
        """Save scan results to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            self.log(f"Results saved to: {output_file}", "SUCCESS")
            
            # Also save a summary CSV
            csv_file = output_file.replace('.json', '_summary.csv')
            with open(csv_file, 'w', encoding='utf-8') as f:
                f.write("Repository,URL,AI Confidence,Secrets Found,Secret Types\n")
                for repo in results.get('ai_repositories', []):
                    secrets_info = next(
                        (s for s in results.get('secrets_summary', [])
                         if s['repository'] == repo['repository'].split('/')[-1]),
                        None
                    )
                    f.write(f"{repo['repository']},{repo['url']},{repo['ai_confidence']:.1f}%,")
                    if secrets_info:
                        f.write(f"{secrets_info['secrets_count']},\"{','.join(secrets_info['secret_types'])}\"\n")
                    else:
                        f.write("0,None\n")
            self.log(f"Summary CSV saved to: {csv_file}", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error saving results: {str(e)}", "ERROR")

def main():
    parser = argparse.ArgumentParser(
        description='AI Repository Secret Scanner v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scan
  python ai_repo_scanner_v2.py --token YOUR_TOKEN

  # Scan with custom parameters
  python ai_repo_scanner_v2.py --token YOUR_TOKEN --max-repos 100 --confidence 30

  # Use custom TruffleHog path
  python ai_repo_scanner_v2.py --token YOUR_TOKEN --trufflehog-path /usr/local/bin/trufflehog
        """
    )
    
    parser.add_argument('--token', required=True, help='GitHub Personal Access Token')
    parser.add_argument('--max-repos', type=int, default=50, 
                       help='Maximum repositories to scan (default: 50)')
    parser.add_argument('--confidence', type=int, default=None,
                       help='Minimum AI confidence threshold (default: 40)')
    parser.add_argument('--trufflehog-path', default='trufflehog', 
                       help='Path to TruffleHog binary (default: trufflehog)')
    parser.add_argument('--output', default='ai_repo_scan_results_v2.json', 
                       help='Output file for results (default: ai_repo_scan_results_v2.json)')
    
    args = parser.parse_args()
    
    # Check if TruffleHog is available
    try:
        subprocess.run([args.trufflehog_path, '--version'], 
                      capture_output=True, timeout=10, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ ERROR: TruffleHog not found or not working properly.")
        print("\nPlease install TruffleHog using one of these methods:")
        print("\n1. Using curl (recommended):")
        print("   curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin")
        print("\n2. Using brew (macOS):")
        print("   brew install trufflehog")
        print("\n3. Download from: https://github.com/trufflesecurity/trufflehog/releases")
        sys.exit(1)
    
    # Create scanner instance
    scanner = AIRepoScanner(args.token, args.trufflehog_path)
    
    try:
        print("\n" + "="*80)
        print("🤖 AI REPOSITORY SECRET SCANNER v2.0")
        print("="*80)
        print(f"Searching for AI-generated repositories and scanning for secrets...")
        print(f"Max repos: {args.max_repos} | Confidence threshold: {args.confidence or 40}%")
        print("="*80 + "\n")
        
        # Run the scan
        results = scanner.scan_repositories(
            max_repos=args.max_repos,
            confidence_threshold=args.confidence
        )
        
        # Save results
        scanner.save_results(results, args.output)
        
        # Print final summary
        print("\n" + "="*80)
        print("📊 FINAL SUMMARY")
        print("="*80)
        print(f"Total Repositories Scanned: {results['scan_summary']['total_scanned']}")
        print(f"AI-Generated Repositories: {results['scan_summary']['ai_detected']}")
        print(f"Average AI Confidence: {results['scan_summary']['avg_confidence']:.1f}%")
        print(f"Repositories with Secrets: {results['scan_summary']['with_secrets']}")
        
        if results['secrets_summary']:
            print("\n🔐 REPOSITORIES WITH SECRETS:")
            for i, secret_repo in enumerate(results['secrets_summary'][:10], 1):
                print(f"\n{i}. {secret_repo['repository']}")
                print(f"   URL: {secret_repo['url']}")
                print(f"   Secrets: {secret_repo['secrets_count']}")
                print(f"   Types: {', '.join(secret_repo['secret_types'])}")
                print(f"   AI Confidence: {secret_repo['ai_confidence']:.1f}%")
        
        print(f"\n✅ Full results saved to: {args.output}")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()