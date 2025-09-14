#!/usr/bin/env python3
"""
AI Repository Scanner - Demo Script
==================================
Demonstrates various usage patterns and configurations for the AI Repository Secret Scanner.

This script shows:
1. Basic scanning with default settings
2. Advanced filtering and targeting
3. Custom AI detection thresholds
4. Batch processing scenarios
5. Integration examples

Author: HAYA Security Team
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta

# Import our scanner (assuming it's in the same directory)
try:
    from ai_repo_secret_scanner import AIRepoSecretScanner
except ImportError:
    print("Error: ai_repo_secret_scanner.py not found in current directory")
    sys.exit(1)

def demo_basic_scan():
    """Demo: Basic scanning with default settings"""
    print("="*60)
    print("DEMO 1: Basic AI Repository Scan")
    print("="*60)
    
    # Check for GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Please set GITHUB_TOKEN environment variable")
        print("export GITHUB_TOKEN='your_token_here'")
        return
    
    scanner = AIRepoSecretScanner(github_token)
    
    # Basic scan of recent repositories
    query = "stars:>5 created:>2023-06-01 language:python"
    print(f"Scanning with query: {query}")
    
    results = scanner.scan_repositories(query, max_repos=10)
    
    print(f"\nResults:")
    print(f"- Repositories scanned: {results['scan_summary']['total_scanned']}")
    print(f"- AI-generated found: {results['scan_summary']['ai_detected']}")
    print(f"- With secrets: {results['scan_summary']['with_secrets']}")
    
    return results

def demo_advanced_filtering():
    """Demo: Advanced filtering and targeting"""
    print("\n" + "="*60)
    print("DEMO 2: Advanced Repository Targeting")
    print("="*60)
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("GitHub token required")
        return
    
    scanner = AIRepoSecretScanner(github_token)
    
    # Target specific types of repositories that might be AI-generated
    advanced_queries = [
        {
            'name': 'Recent High-Activity Python Projects',
            'query': 'language:python stars:>10 created:>2023-01-01 pushed:>2024-01-01',
            'max_repos': 5
        },
        {
            'name': 'JavaScript/TypeScript Automation Projects',
            'query': 'language:javascript stars:>5 "automation" OR "bot" created:>2023-01-01',
            'max_repos': 5
        },
        {
            'name': 'Recently Created Popular Repositories',
            'query': 'stars:>20 created:>2024-01-01 forks:>5',
            'max_repos': 5
        }
    ]
    
    all_results = []
    
    for query_info in advanced_queries:
        print(f"\nScanning: {query_info['name']}")
        print(f"Query: {query_info['query']}")
        
        results = scanner.scan_repositories(
            query_info['query'], 
            query_info['max_repos']
        )
        
        all_results.append({
            'category': query_info['name'],
            'results': results
        })
        
        print(f"Found {results['scan_summary']['ai_detected']} AI repositories")
        
        # Small delay between queries
        time.sleep(2)
    
    return all_results

def demo_custom_thresholds():
    """Demo: Custom AI detection thresholds"""
    print("\n" + "="*60)
    print("DEMO 3: Custom AI Detection Thresholds")
    print("="*60)
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("GitHub token required")
        return
    
    scanner = AIRepoSecretScanner(github_token)
    
    # Modify AI detection thresholds for more sensitive detection
    print("Original thresholds:")
    for key, value in scanner.AI_THRESHOLDS.items():
        print(f"  {key}: {value}")
    
    # Make detection more sensitive
    scanner.AI_THRESHOLDS.update({
        'emoji_count_readme': 5,        # Lower emoji threshold
        'emoji_commit_ratio': 0.2,      # Lower commit emoji ratio
        'commit_burst_threshold': 10,   # Smaller burst size
        'min_confidence_score': 40      # Lower confidence threshold
    })
    
    print("\nModified thresholds (more sensitive):")
    for key, value in scanner.AI_THRESHOLDS.items():
        print(f"  {key}: {value}")
    
    # Scan with custom thresholds
    query = "stars:>3 created:>2023-01-01 language:python"
    results = scanner.scan_repositories(query, max_repos=10)
    
    print(f"\nResults with custom thresholds:")
    print(f"- AI repositories detected: {results['scan_summary']['ai_detected']}")
    
    return results

def demo_targeted_secret_hunting():
    """Demo: Targeted secret hunting in AI repositories"""
    print("\n" + "="*60)
    print("DEMO 4: Targeted Secret Hunting")
    print("="*60)
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("GitHub token required")
        return
    
    scanner = AIRepoSecretScanner(github_token)
    
    # Target repositories likely to contain secrets
    secret_hunting_queries = [
        'language:python "api_key" OR "secret" OR "token" created:>2023-01-01',
        'language:javascript "config" OR "env" stars:>5 created:>2023-01-01',
        '"aws" OR "azure" OR "gcp" language:python created:>2023-01-01'
    ]
    
    total_secrets_found = 0
    
    for query in secret_hunting_queries:
        print(f"\nHunting secrets with query: {query[:50]}...")
        
        results = scanner.scan_repositories(query, max_repos=5)
        
        for repo_secrets in results.get('secrets_summary', []):
            total_secrets_found += repo_secrets['secrets_count']
            print(f"  🔍 {repo_secrets['repository']}: {repo_secrets['secrets_count']} secrets")
    
    print(f"\nTotal secrets found: {total_secrets_found}")
    
    return total_secrets_found

def demo_batch_processing():
    """Demo: Batch processing multiple repository lists"""
    print("\n" + "="*60)
    print("DEMO 5: Batch Processing")
    print("="*60)
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("GitHub token required")
        return
    
    scanner = AIRepoSecretScanner(github_token)
    
    # Define multiple batch processing scenarios
    batch_scenarios = [
        {
            'name': 'Recent AI/ML Projects',
            'queries': [
                'topic:machine-learning created:>2023-01-01 stars:>5',
                'topic:artificial-intelligence created:>2023-01-01 stars:>5',
                '"neural network" OR "deep learning" created:>2023-01-01'
            ]
        },
        {
            'name': 'Automation Tools',
            'queries': [
                'topic:automation created:>2023-01-01 stars:>3',
                '"bot" OR "crawler" OR "scraper" created:>2023-01-01',
                'topic:productivity-tools created:>2023-01-01'
            ]
        }
    ]
    
    batch_results = []
    
    for scenario in batch_scenarios:
        print(f"\nProcessing scenario: {scenario['name']}")
        scenario_results = []
        
        for query in scenario['queries']:
            print(f"  Query: {query[:40]}...")
            results = scanner.scan_repositories(query, max_repos=3)
            scenario_results.append(results)
            time.sleep(1)  # Rate limiting
        
        batch_results.append({
            'scenario': scenario['name'],
            'results': scenario_results
        })
    
    # Summarize batch results
    total_ai_repos = 0
    total_secrets = 0
    
    for scenario_result in batch_results:
        scenario_ai = sum(r['scan_summary']['ai_detected'] for r in scenario_result['results'])
        scenario_secrets = sum(r['scan_summary']['with_secrets'] for r in scenario_result['results'])
        
        total_ai_repos += scenario_ai
        total_secrets += scenario_secrets
        
        print(f"\n{scenario_result['scenario']}:")
        print(f"  AI repositories: {scenario_ai}")
        print(f"  With secrets: {scenario_secrets}")
    
    print(f"\nBatch processing summary:")
    print(f"  Total AI repositories: {total_ai_repos}")
    print(f"  Total with secrets: {total_secrets}")
    
    return batch_results

def save_demo_results(all_results):
    """Save all demo results to a comprehensive report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_scanner_demo_results_{timestamp}.json"
    
    report = {
        'demo_timestamp': datetime.now().isoformat(),
        'demo_results': all_results,
        'summary': {
            'total_demos_run': len(all_results),
            'demo_completion_time': datetime.now().isoformat()
        }
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n📊 Demo results saved to: {filename}")
    except Exception as e:
        print(f"Error saving demo results: {str(e)}")

def main():
    """Run all demo scenarios"""
    print("🤖 AI Repository Secret Scanner - Demo Suite")
    print("=" * 80)
    print("This demo will showcase various usage patterns and capabilities")
    print("Make sure you have set GITHUB_TOKEN environment variable")
    print("=" * 80)
    
    # Check prerequisites
    if not os.getenv('GITHUB_TOKEN'):
        print("❌ GITHUB_TOKEN not set. Please export your GitHub token:")
        print("export GITHUB_TOKEN='your_token_here'")
        return
    
    # Check TruffleHog availability
    import subprocess
    try:
        subprocess.run(['trufflehog', '--version'], capture_output=True, timeout=5)
        print("✅ TruffleHog is available")
    except:
        print("⚠️  TruffleHog not found. Secret scanning will be limited.")
        print("Install: curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin")
    
    print("\nStarting demo scenarios...\n")
    
    demo_results = []
    
    try:
        # Run all demos
        demo_results.append(('Basic Scan', demo_basic_scan()))
        demo_results.append(('Advanced Filtering', demo_advanced_filtering()))
        demo_results.append(('Custom Thresholds', demo_custom_thresholds()))
        demo_results.append(('Secret Hunting', demo_targeted_secret_hunting()))
        demo_results.append(('Batch Processing', demo_batch_processing()))
        
        # Save comprehensive results
        save_demo_results(demo_results)
        
        print("\n" + "="*80)
        print("🎉 All demos completed successfully!")
        print("="*80)
        print("The AI Repository Scanner is ready for production use.")
        print("Check the generated JSON files for detailed results.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {str(e)}")

if __name__ == "__main__":
    main()