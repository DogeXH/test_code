#!/usr/bin/env python3
"""
Demo script for AI Repository Scanner v2
Shows example usage and capabilities
"""

import json
import sys

def display_sample_results():
    """Display sample results to demonstrate scanner output"""
    
    sample_results = {
        "scan_summary": {
            "total_scanned": 50,
            "ai_detected": 12,
            "with_secrets": 4,
            "avg_confidence": 65.8
        },
        "ai_repositories": [
            {
                "repository": "johndoe/awesome-todo-app",
                "url": "https://github.com/johndoe/awesome-todo-app",
                "ai_confidence": 82.5,
                "confidence_reasons": [
                    "Excessive emoji usage in README",
                    "Commit bursts detected (3 bursts)",
                    "Multiple AI indicators found (score: 12)",
                    "Rapid development: 4.2 hours"
                ],
                "language": "JavaScript",
                "stars": 2
            },
            {
                "repository": "alice/my-portfolio-site",
                "url": "https://github.com/alice/my-portfolio-site",
                "ai_confidence": 71.0,
                "confidence_reasons": [
                    "High emoji ratio in commits (45%)",
                    "Some AI indicators present",
                    "Suspiciously perfect commit timing",
                    "Metadata indicators: Large repo with low engagement"
                ],
                "language": "HTML",
                "stars": 0
            },
            {
                "repository": "bot123/calculator-app",
                "url": "https://github.com/bot123/calculator-app",
                "ai_confidence": 94.0,
                "confidence_reasons": [
                    "Multiple AI indicators found (score: 18)",
                    "Commit bursts detected (5 bursts)",
                    "Excessive emoji usage in README",
                    "Rapid development: 1.5 hours",
                    "AI-related topic: ai-generated"
                ],
                "language": "Python",
                "stars": 1
            }
        ],
        "secrets_summary": [
            {
                "repository": "johndoe/awesome-todo-app",
                "url": "https://github.com/johndoe/awesome-todo-app",
                "secrets_count": 3,
                "ai_confidence": 82.5,
                "secret_types": ["AWS", "MongoDB", "JWT"]
            },
            {
                "repository": "bot123/calculator-app",
                "url": "https://github.com/bot123/calculator-app",
                "secrets_count": 1,
                "ai_confidence": 94.0,
                "secret_types": ["OpenAI"]
            }
        ],
        "detection_stats": {
            "Excessive emoji usage in README": 8,
            "Commit bursts detected": 7,
            "Multiple AI indicators found": 6,
            "High emoji ratio in commits": 5,
            "Rapid development": 4,
            "Some AI indicators present": 4,
            "Suspiciously perfect commit timing": 3
        }
    }
    
    print("\n" + "="*80)
    print("🤖 AI REPOSITORY SCANNER v2 - DEMO RESULTS")
    print("="*80)
    
    # Summary
    summary = sample_results["scan_summary"]
    print(f"\n📊 SCAN SUMMARY:")
    print(f"   Total Repositories Scanned: {summary['total_scanned']}")
    print(f"   AI-Generated Detected: {summary['ai_detected']} ({summary['ai_detected']/summary['total_scanned']*100:.1f}%)")
    print(f"   With Exposed Secrets: {summary['with_secrets']}")
    print(f"   Average AI Confidence: {summary['avg_confidence']:.1f}%")
    
    # Top AI-Generated Repos
    print(f"\n🤖 TOP AI-GENERATED REPOSITORIES:")
    for i, repo in enumerate(sample_results["ai_repositories"][:3], 1):
        print(f"\n{i}. {repo['repository']} (Confidence: {repo['ai_confidence']:.1f}%)")
        print(f"   URL: {repo['url']}")
        print(f"   Language: {repo['language']} | Stars: {repo['stars']}")
        print(f"   Detection Reasons:")
        for reason in repo['confidence_reasons'][:3]:
            print(f"     • {reason}")
    
    # Secrets Found
    if sample_results["secrets_summary"]:
        print(f"\n🔐 REPOSITORIES WITH SECRETS:")
        for secret_repo in sample_results["secrets_summary"]:
            print(f"\n   {secret_repo['repository']}")
            print(f"   Secrets Found: {secret_repo['secrets_count']} ({', '.join(secret_repo['secret_types'])})")
            print(f"   AI Confidence: {secret_repo['ai_confidence']:.1f}%")
    
    # Detection Statistics
    print(f"\n📈 MOST COMMON AI INDICATORS:")
    for indicator, count in list(sample_results["detection_stats"].items())[:5]:
        print(f"   • {indicator}: {count} repositories")
    
    print("\n" + "="*80)
    print("This is a demo showing sample output format.")
    print("To run actual scans, use: python ai_repo_scanner_v2.py --token YOUR_TOKEN")
    print("="*80 + "\n")

def main():
    print("\n🚀 AI Repository Scanner v2 Demo")
    print("\nThis demo shows what the scanner output looks like.")
    print("The scanner can detect AI-generated repositories using:")
    print("  • Emoji pattern analysis")
    print("  • Commit burst detection")
    print("  • AI tool indicators")
    print("  • Repository metadata analysis")
    print("  • And more...")
    
    input("\nPress Enter to see sample results...")
    
    display_sample_results()
    
    print("\n📝 Key Features:")
    print("  ✓ No hardcoded date filters")
    print("  ✓ Advanced search strategies")
    print("  ✓ Detailed confidence scoring")
    print("  ✓ Parallel processing for speed")
    print("  ✓ TruffleHog integration for secret scanning")
    print("  ✓ CSV export for easy analysis")
    
    print("\n🔧 To use the actual scanner:")
    print("  1. Get a GitHub Personal Access Token")
    print("  2. Install TruffleHog")
    print("  3. Run: python ai_repo_scanner_v2.py --token YOUR_TOKEN")
    
    print("\nFor more information, see AI_REPO_SCANNER_V2_README.md")

if __name__ == "__main__":
    main()