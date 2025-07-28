#!/usr/bin/env python3
"""
Comprehensive Repository Validation Script
Validates accuracy, consistency, and confidence levels across all files
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class RepositoryValidator:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.validation_results = {
            'files_checked': 0,
            'total_word_count': 0,
            'issues_found': [],
            'statistics': {},
            'consistency_checks': {},
            'confidence_scores': {}
        }
        
    def validate_all_files(self):
        """Main validation function"""
        print("🔍 Starting Comprehensive Repository Validation...")
        print("=" * 60)
        
        # Get all markdown files
        md_files = list(self.repo_path.rglob("*.md"))
        
        for file_path in md_files:
            self.validate_file(file_path)
            
        self.perform_cross_file_validation()
        self.generate_validation_report()
        
    def validate_file(self, file_path):
        """Validate individual file"""
        relative_path = file_path.relative_to(self.repo_path)
        print(f"\n📄 Validating: {relative_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.validation_results['files_checked'] += 1
            
            # Basic metrics
            word_count = len(content.split())
            self.validation_results['total_word_count'] += word_count
            
            # File-specific validations
            if 'master_storytellers' in str(file_path):
                self.validate_master_storyteller_file(file_path, content)
            elif 'README.md' in str(file_path):
                self.validate_readme_file(file_path, content)
            elif file_path.name.startswith(('01_', '02_', '03_')):
                self.validate_research_module(file_path, content)
                
            print(f"   ✅ Word count: {word_count:,}")
            
        except Exception as e:
            self.validation_results['issues_found'].append({
                'file': str(relative_path),
                'type': 'file_error',
                'message': f"Error reading file: {str(e)}"
            })
            print(f"   ❌ Error: {str(e)}")
            
    def validate_master_storyteller_file(self, file_path, content):
        """Validate master storyteller profile files"""
        relative_path = file_path.relative_to(self.repo_path)
        
        # Check required sections
        required_sections = [
            '📋 Profile Overview',
            '🎬 Cinematic Philosophy & Vision',
            '🏗️ Signature Storytelling Techniques',
            '🎭 Character Development Philosophy',
            '🏆.*Impact',  # Flexible for different impact section titles
            '🎓 Lessons for AI Storytelling'
        ]
        
        missing_sections = []
        for section in required_sections:
            if not re.search(section, content):
                missing_sections.append(section)
                
        if missing_sections:
            self.validation_results['issues_found'].append({
                'file': str(relative_path),
                'type': 'missing_sections',
                'message': f"Missing sections: {', '.join(missing_sections)}"
            })
            
        # Check for citations and references
        citation_count = len(re.findall(r'\*\*[^*]+\*\*:', content))
        if citation_count < 10:
            self.validation_results['issues_found'].append({
                'file': str(relative_path),
                'type': 'low_citations',
                'message': f"Only {citation_count} citations found, expected 10+"
            })
            
        # Word count validation for master storytellers (realistic expectation)
        word_count = len(content.split())
        if word_count < 1500:
            self.validation_results['issues_found'].append({
                'file': str(relative_path),
                'type': 'insufficient_content',
                'message': f"Word count {word_count} below expected 1500+ for master storyteller"
            })
            
    def validate_readme_file(self, file_path, content):
        """Validate README files"""
        relative_path = file_path.relative_to(self.repo_path)
        
        # Check for consistency in statistics
        stats_patterns = {
            'word_count': r'(\d+,?\d*)\+?\s*words',
            'citations': r'(\d+,?\d*)\+?\s*(?:academic\s+)?citations',
            'storytellers': r'(\d+)\s+(?:master\s+)?storytellers?',
            'profiles': r'(\d+)\s+(?:comprehensive\s+)?profiles?'
        }
        
        found_stats = {}
        for stat_name, pattern in stats_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # Convert to numbers for comparison
                numbers = [int(m.replace(',', '')) for m in matches]
                found_stats[stat_name] = numbers
                
        # Store for cross-validation
        self.validation_results['statistics'][str(relative_path)] = found_stats
        
    def validate_research_module(self, file_path, content):
        """Validate research module files"""
        relative_path = file_path.relative_to(self.repo_path)
        
        # Check for academic structure
        academic_indicators = [
            'abstract', 'introduction', 'methodology', 'results', 
            'discussion', 'conclusion', 'references'
        ]
        
        found_indicators = []
        for indicator in academic_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                found_indicators.append(indicator)
                
        if len(found_indicators) < 3:
            self.validation_results['issues_found'].append({
                'file': str(relative_path),
                'type': 'insufficient_academic_structure',
                'message': f"Only found {len(found_indicators)} academic indicators: {found_indicators}"
            })
            
    def perform_cross_file_validation(self):
        """Validate consistency across files"""
        print("\n🔄 Performing Cross-File Validation...")
        
        # Check master storytellers count consistency
        self.validate_storyteller_count_consistency()
        
        # Check statistics consistency
        self.validate_statistics_consistency()
        
        # Check file naming consistency
        self.validate_file_naming_consistency()
        
    def validate_storyteller_count_consistency(self):
        """Validate storyteller counts across files"""
        master_storytellers_dir = self.repo_path / 'research' / 'master_storytellers'
        
        if master_storytellers_dir.exists():
            # Count actual storyteller files (excluding README)
            storyteller_files = [f for f in master_storytellers_dir.glob('*.md') 
                               if f.name != 'README.md' and re.match(r'\d+_', f.name)]
            actual_count = len(storyteller_files)
            
            # Check README claims
            readme_path = master_storytellers_dir / 'README.md'
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                    
                # Extract claimed counts
                claimed_matches = re.findall(r'(\d+)\s+(?:comprehensive\s+)?profiles?', readme_content, re.IGNORECASE)
                if claimed_matches:
                    claimed_count = int(claimed_matches[0])
                    if claimed_count != actual_count:
                        self.validation_results['issues_found'].append({
                            'file': 'master_storytellers/README.md',
                            'type': 'count_mismatch',
                            'message': f"Claims {claimed_count} profiles but found {actual_count} files"
                        })
                        
            self.validation_results['consistency_checks']['storyteller_count'] = {
                'actual': actual_count,
                'files': [f.name for f in storyteller_files]
            }
            
    def validate_statistics_consistency(self):
        """Validate statistics consistency across README files"""
        main_readme_stats = self.validation_results['statistics'].get('README.md', {})
        module_readme_stats = self.validation_results['statistics'].get('research/master_storytellers/README.md', {})
        
        # Compare word counts
        if 'word_count' in main_readme_stats and 'word_count' in module_readme_stats:
            main_words = main_readme_stats['word_count']
            module_words = module_readme_stats['word_count']
            
            # Check for major discrepancies
            if main_words and module_words:
                main_max = max(main_words)
                module_max = max(module_words)
                
                if abs(main_max - module_max) > 10000:  # Allow 10k difference
                    self.validation_results['issues_found'].append({
                        'file': 'cross_file_validation',
                        'type': 'statistics_mismatch',
                        'message': f"Word count mismatch: main README claims {main_max}, module claims {module_max}"
                    })
                    
    def validate_file_naming_consistency(self):
        """Validate file naming patterns"""
        master_storytellers_dir = self.repo_path / 'research' / 'master_storytellers'
        
        if master_storytellers_dir.exists():
            storyteller_files = [f for f in master_storytellers_dir.glob('*.md') 
                               if f.name != 'README.md']
            
            # Check numbering sequence
            numbered_files = []
            for f in storyteller_files:
                match = re.match(r'(\d+)_', f.name)
                if match:
                    numbered_files.append((int(match.group(1)), f.name))
                    
            numbered_files.sort()
            
            # Check for gaps in numbering
            expected_numbers = list(range(1, len(numbered_files) + 1))
            actual_numbers = [num for num, _ in numbered_files]
            
            if actual_numbers != expected_numbers:
                self.validation_results['issues_found'].append({
                    'file': 'master_storytellers/',
                    'type': 'numbering_gaps',
                    'message': f"Expected {expected_numbers}, found {actual_numbers}"
                })
                
    def calculate_confidence_scores(self):
        """Calculate confidence scores for different aspects"""
        total_files = self.validation_results['files_checked']
        total_issues = len(self.validation_results['issues_found'])
        
        # Overall confidence
        overall_confidence = max(0, 100 - (total_issues * 5))  # Deduct 5% per issue
        
        # Content completeness confidence
        expected_word_count = 100000  # Based on realistic claims
        actual_word_count = self.validation_results['total_word_count']
        content_confidence = min(100, (actual_word_count / expected_word_count) * 100)
        
        # Structure consistency confidence
        structure_issues = len([i for i in self.validation_results['issues_found'] 
                              if i['type'] in ['missing_sections', 'insufficient_academic_structure']])
        structure_confidence = max(0, 100 - (structure_issues * 10))
        
        self.validation_results['confidence_scores'] = {
            'overall': round(overall_confidence, 1),
            'content_completeness': round(content_confidence, 1),
            'structure_consistency': round(structure_confidence, 1),
            'cross_file_consistency': 95.0 if total_issues < 3 else 80.0
        }
        
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        self.calculate_confidence_scores()
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 60)
        
        # Summary statistics
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Files Validated: {self.validation_results['files_checked']}")
        print(f"   Total Word Count: {self.validation_results['total_word_count']:,}")
        print(f"   Issues Found: {len(self.validation_results['issues_found'])}")
        
        # Confidence scores
        print(f"\n🎯 CONFIDENCE SCORES:")
        for aspect, score in self.validation_results['confidence_scores'].items():
            status = "🟢" if score >= 90 else "🟡" if score >= 70 else "🔴"
            print(f"   {status} {aspect.replace('_', ' ').title()}: {score}%")
            
        # Issues breakdown
        if self.validation_results['issues_found']:
            print(f"\n⚠️  ISSUES FOUND:")
            issue_types = Counter(issue['type'] for issue in self.validation_results['issues_found'])
            for issue_type, count in issue_types.items():
                print(f"   • {issue_type.replace('_', ' ').title()}: {count}")
                
            print(f"\n📋 DETAILED ISSUES:")
            for i, issue in enumerate(self.validation_results['issues_found'], 1):
                print(f"   {i}. {issue['file']}")
                print(f"      Type: {issue['type']}")
                print(f"      Message: {issue['message']}")
                print()
        else:
            print(f"\n✅ NO ISSUES FOUND - Repository is fully validated!")
            
        # Consistency checks
        if self.validation_results['consistency_checks']:
            print(f"\n🔄 CONSISTENCY CHECKS:")
            for check, result in self.validation_results['consistency_checks'].items():
                print(f"   • {check.replace('_', ' ').title()}: {result}")
                
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if self.validation_results['confidence_scores']['overall'] >= 95:
            print("   ✅ Repository is in excellent condition!")
            print("   ✅ All files meet quality standards")
            print("   ✅ Statistics are consistent across files")
        elif self.validation_results['confidence_scores']['overall'] >= 85:
            print("   🟡 Repository is in good condition with minor issues")
            print("   🟡 Consider addressing the issues listed above")
        else:
            print("   🔴 Repository needs attention")
            print("   🔴 Multiple issues require resolution")
            
        # Save detailed report
        report_path = self.repo_path / 'validation_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, default=str)
        print(f"\n💾 Detailed report saved to: {report_path}")

def main():
    repo_path = "/workspace/super-agi-telugu-story-engine"
    validator = RepositoryValidator(repo_path)
    validator.validate_all_files()

if __name__ == "__main__":
    main()