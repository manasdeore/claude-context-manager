#!/usr/bin/env python3
"""
Enhanced Progress Report Generator
Visits all project directories and generates comprehensive progress reports
"""

import json
import os
import sys
import subprocess
import glob
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import re

class ProgressReportGenerator:
    def __init__(self):
        self.repo_path = Path(__file__).parent.parent
        self.projects_file = self.repo_path / "projects.json"
        self.reports_dir = self.repo_path / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Base directory for projects (parent of claude-context-manager)
        self.base_dir = self.repo_path.parent
        
        self.current_time = datetime.now()
        self.report_data = {
            'generated_at': self.current_time.isoformat(),
            'projects': [],
            'summary': {},
            'system_info': {}
        }

    def load_projects(self):
        """Load projects configuration"""
        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading projects: {e}")
            return None

    def run_git_command(self, directory, command):
        """Run git command in specified directory"""
        try:
            result = subprocess.run(
                command, 
                cwd=directory, 
                capture_output=True, 
                text=True, 
                timeout=30,
                shell=True
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    def analyze_directory(self, directory_path):
        """Analyze a project directory for progress information"""
        analysis = {
            'exists': False,
            'files': {'total': 0, 'recent': 0, 'by_type': {}},
            'git_info': {'is_repo': False, 'status': None, 'recent_commits': []},
            'last_modified': None,
            'size_mb': 0,
            'structure': {}
        }
        
        if not directory_path or not Path(directory_path).exists():
            return analysis
            
        directory_path = Path(directory_path)
        analysis['exists'] = True
        
        try:
            # File system analysis
            file_count = 0
            recent_count = 0
            size_bytes = 0
            file_types = defaultdict(int)
            recent_threshold = self.current_time - timedelta(days=7)
            latest_mod_time = None
            
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    try:
                        stat = file_path.stat()
                        file_count += 1
                        size_bytes += stat.st_size
                        
                        # File type analysis
                        suffix = file_path.suffix.lower() or 'no_extension'
                        file_types[suffix] += 1
                        
                        # Recent files analysis
                        mod_time = datetime.fromtimestamp(stat.st_mtime)
                        if mod_time > recent_threshold:
                            recent_count += 1
                        
                        # Track latest modification
                        if latest_mod_time is None or mod_time > latest_mod_time:
                            latest_mod_time = mod_time
                            
                    except (OSError, PermissionError):
                        continue
            
            analysis['files']['total'] = file_count
            analysis['files']['recent'] = recent_count
            analysis['files']['by_type'] = dict(file_types)
            analysis['size_mb'] = round(size_bytes / (1024 * 1024), 2)
            analysis['last_modified'] = latest_mod_time.isoformat() if latest_mod_time else None
            
            # Directory structure analysis
            structure = {}
            for item in directory_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    try:
                        item_files = len(list(item.rglob('*')))
                        structure[item.name] = item_files
                    except (OSError, PermissionError):
                        structure[item.name] = 0
            analysis['structure'] = structure
            
            # Git analysis
            if (directory_path / '.git').exists():
                analysis['git_info']['is_repo'] = True
                
                # Git status
                status = self.run_git_command(directory_path, 'git status --porcelain')
                if status is not None:
                    analysis['git_info']['status'] = {
                        'clean': len(status) == 0,
                        'modified_files': len([line for line in status.split('\n') if line.strip()]),
                        'changes': status.split('\n')[:10]  # First 10 changes
                    }
                
                # Recent commits
                log = self.run_git_command(directory_path, 'git log --oneline -10')
                if log:
                    analysis['git_info']['recent_commits'] = log.split('\n')[:5]
                
                # Branch info
                branch = self.run_git_command(directory_path, 'git branch --show-current')
                if branch:
                    analysis['git_info']['current_branch'] = branch
        
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis

    def detect_project_activity(self, project, directory_analysis):
        """Detect recent activity and infer progress"""
        activity_score = 0
        activity_indicators = []
        
        # Handle case where directory doesn't exist
        if not directory_analysis or not directory_analysis.get('exists', False):
            return {
                'score': 0,
                'level': "Unknown",
                'indicators': ["Directory not found or inaccessible"]
            }
        
        if directory_analysis.get('files', {}).get('recent', 0) > 0:
            recent_files = directory_analysis['files']['recent']
            activity_score += min(recent_files * 10, 50)
            activity_indicators.append(f"{recent_files} files modified in last 7 days")
        
        if directory_analysis.get('git_info', {}).get('is_repo', False):
            git_status = directory_analysis['git_info'].get('status', {})
            if git_status and not git_status.get('clean', True):
                activity_score += 20
                activity_indicators.append(f"{git_status.get('modified_files', 0)} uncommitted changes")
            
            commits = directory_analysis['git_info'].get('recent_commits', [])
            if commits:
                activity_score += len(commits) * 5
                activity_indicators.append(f"{len(commits)} recent commits")
        
        # Determine activity level
        if activity_score >= 50:
            activity_level = "High"
        elif activity_score >= 20:
            activity_level = "Medium" 
        elif activity_score > 0:
            activity_level = "Low"
        else:
            activity_level = "Inactive"
        
        return {
            'score': activity_score,
            'level': activity_level,
            'indicators': activity_indicators
        }

    def generate_project_report(self, project):
        """Generate detailed report for a single project"""
        print(f"Analyzing project: {project['name']}")
        
        # Determine project directory
        working_dir = None
        if 'working_directory' in project:
            working_dir = project['working_directory']
        elif 'folder_path' in project and project['folder_path'].startswith('./'):
            # Relative path from context manager
            relative_path = project['folder_path'][2:]  # Remove './'
            working_dir = str(self.repo_path / relative_path)
        elif 'folder_path' in project:
            working_dir = project['folder_path']
        
        # If no specific directory, try to find it in parent directory
        if not working_dir or not Path(working_dir).exists():
            # Look for project directory by name patterns
            project_name_patterns = [
                project['name'].lower().replace(' ', '-'),
                project['id'],
                project['name'].replace(' ', '_'),
                project['name'].replace(' ', '')
            ]
            
            for pattern in project_name_patterns:
                potential_dirs = list(self.base_dir.glob(f"*{pattern}*"))
                if potential_dirs:
                    working_dir = str(potential_dirs[0])
                    break
        
        # Analyze the directory
        directory_analysis = self.analyze_directory(working_dir)
        
        # Detect activity
        activity = self.detect_project_activity(project, directory_analysis)
        
        # Create comprehensive project report
        report = {
            'project_info': {
                'id': project['id'],
                'name': project['name'],
                'description': project.get('description', ''),
                'status': project.get('status', 'unknown'),
                'priority': project.get('priority', 'medium'),
                'created_date': project.get('created_date', ''),
                'last_updated': project.get('last_updated', ''),
                'tags': project.get('tags', [])
            },
            'directory_info': {
                'path': working_dir,
                'exists': directory_analysis['exists'],
                'analysis': directory_analysis
            },
            'activity': activity,
            'progress': project.get('progress', {}),
            'technology_stack': project.get('technology_stack', []),
            'github_repo': project.get('github_repo', ''),
            'live_url': project.get('live_url', ''),
            'context_file': project.get('context_file', '')
        }
        
        return report

    def generate_summary(self, project_reports):
        """Generate overall summary statistics"""
        summary = {
            'total_projects': len(project_reports),
            'status_breakdown': defaultdict(int),
            'priority_breakdown': defaultdict(int),
            'activity_breakdown': defaultdict(int),
            'technology_usage': defaultdict(int),
            'recent_activity': 0,
            'total_files': 0,
            'total_size_mb': 0,
            'git_repos': 0,
            'active_projects': 0
        }
        
        for report in project_reports:
            # Status and priority
            summary['status_breakdown'][report['project_info']['status']] += 1
            summary['priority_breakdown'][report['project_info']['priority']] += 1
            summary['activity_breakdown'][report['activity']['level']] += 1
            
            # Technology stack
            for tech in report['technology_stack']:
                summary['technology_usage'][tech] += 1
            
            # File and size stats
            if report['directory_info']['exists']:
                analysis = report['directory_info']['analysis']
                summary['total_files'] += analysis['files']['total']
                summary['total_size_mb'] += analysis['size_mb']
                summary['recent_activity'] += analysis['files']['recent']
                
                if analysis['git_info']['is_repo']:
                    summary['git_repos'] += 1
                
                if report['activity']['level'] in ['High', 'Medium']:
                    summary['active_projects'] += 1
        
        return dict(summary)

    def save_json_report(self, filename='progress_report.json'):
        """Save detailed JSON report"""
        report_file = self.reports_dir / filename
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, indent=2, ensure_ascii=False)
        return report_file

    def save_markdown_report(self, filename='progress_report.md'):
        """Save human-readable markdown report"""
        report_file = self.reports_dir / filename
        
        md_content = f"""# Claude Context Manager - Progress Report
Generated: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Total Projects**: {self.report_data['summary']['total_projects']}
- **Active Projects**: {self.report_data['summary']['active_projects']}
- **Git Repositories**: {self.report_data['summary']['git_repos']}
- **Total Files**: {self.report_data['summary']['total_files']:,}
- **Total Size**: {self.report_data['summary']['total_size_mb']:.1f} MB
- **Recent Activity**: {self.report_data['summary']['recent_activity']} files modified in last 7 days

## Status Overview

"""
        
        # Status breakdown
        for status, count in self.report_data['summary']['status_breakdown'].items():
            md_content += f"- **{status.title()}**: {count} projects\n"
        
        md_content += "\n## Activity Levels\n\n"
        for level, count in self.report_data['summary']['activity_breakdown'].items():
            md_content += f"- **{level}**: {count} projects\n"
        
        md_content += "\n## Technology Stack Usage\n\n"
        tech_usage = sorted(self.report_data['summary']['technology_usage'].items(), 
                           key=lambda x: x[1], reverse=True)
        for tech, count in tech_usage[:10]:  # Top 10
            md_content += f"- **{tech}**: {count} projects\n"
        
        md_content += "\n## Project Details\n\n"
        
        # Project details
        for project in self.report_data['projects']:
            info = project['project_info']
            activity = project['activity']
            
            md_content += f"### {info['name']}\n\n"
            md_content += f"- **ID**: {info['id']}\n"
            md_content += f"- **Status**: {info['status']}\n"
            md_content += f"- **Priority**: {info['priority']}\n"
            md_content += f"- **Activity Level**: {activity['level']} (Score: {activity['score']})\n"
            
            if project['directory_info']['exists']:
                analysis = project['directory_info']['analysis']
                md_content += f"- **Directory**: {project['directory_info']['path']}\n"
                md_content += f"- **Files**: {analysis['files']['total']:,} total, {analysis['files']['recent']} recent\n"
                md_content += f"- **Size**: {analysis['size_mb']} MB\n"
                
                if analysis['git_info']['is_repo']:
                    git_status = analysis['git_info'].get('status', {})
                    if git_status and isinstance(git_status, dict):
                        md_content += f"- **Git**: {git_status.get('modified_files', 0)} uncommitted changes\n"
            else:
                md_content += f"- **Directory**: Not found or inaccessible\n"
            
            # Activity indicators
            if activity['indicators']:
                md_content += "- **Recent Activity**:\n"
                for indicator in activity['indicators']:
                    md_content += f"  - {indicator}\n"
            
            # Progress information
            progress = project['progress']
            if progress:
                completed_tasks = len(progress.get('completed_tasks', []))
                if completed_tasks > 0:
                    md_content += f"- **Completed Tasks**: {completed_tasks}\n"
                if 'current_task' in progress:
                    md_content += f"- **Current Task**: {progress['current_task']}\n"
            
            md_content += "\n"
        
        md_content += f"\n---\n*Report generated by Claude Context Manager on {self.current_time.strftime('%Y-%m-%d at %H:%M:%S')}*\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return report_file

    def save_html_report(self, filename='progress_report.html'):
        """Save interactive HTML report"""
        report_file = self.reports_dir / filename
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Context Manager - Progress Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; }}
        .header h1 {{ margin: 0; font-size: 2.2em; }}
        .header .subtitle {{ opacity: 0.9; margin-top: 10px; }}
        .content {{ padding: 30px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #333; }}
        .summary-card .value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .project-card {{ border: 1px solid #ddd; border-radius: 8px; margin: 20px 0; overflow: hidden; }}
        .project-header {{ background: #f8f9fa; padding: 20px; border-bottom: 1px solid #ddd; }}
        .project-content {{ padding: 20px; }}
        .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }}
        .status-completed {{ background: #d4edda; color: #155724; }}
        .status-in_progress {{ background: #fff3cd; color: #856404; }}
        .status-paused {{ background: #f8d7da; color: #721c24; }}
        .activity-high {{ color: #dc3545; font-weight: bold; }}
        .activity-medium {{ color: #ffc107; font-weight: bold; }}
        .activity-low {{ color: #28a745; }}
        .activity-inactive {{ color: #6c757d; }}
        .tech-stack {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
        .tech-tag {{ background: #e9ecef; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }}
        .chart-container {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Claude Context Manager</h1>
            <div class="subtitle">Progress Report - Generated {self.current_time.strftime('%Y-%m-%d at %H:%M:%S')}</div>
        </div>
        
        <div class="content">
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Total Projects</h3>
                    <div class="value">{self.report_data['summary']['total_projects']}</div>
                </div>
                <div class="summary-card">
                    <h3>Active Projects</h3>
                    <div class="value">{self.report_data['summary']['active_projects']}</div>
                </div>
                <div class="summary-card">
                    <h3>Git Repositories</h3>
                    <div class="value">{self.report_data['summary']['git_repos']}</div>
                </div>
                <div class="summary-card">
                    <h3>Total Files</h3>
                    <div class="value">{self.report_data['summary']['total_files']:,}</div>
                </div>
                <div class="summary-card">
                    <h3>Total Size</h3>
                    <div class="value">{self.report_data['summary']['total_size_mb']:.1f} MB</div>
                </div>
                <div class="summary-card">
                    <h3>Recent Activity</h3>
                    <div class="value">{self.report_data['summary']['recent_activity']}</div>
                </div>
            </div>
"""
        
        # Add project cards
        for project in self.report_data['projects']:
            info = project['project_info']
            activity = project['activity']
            
            status_class = f"status-{info['status'].replace(' ', '_')}"
            activity_class = f"activity-{activity['level'].lower()}"
            
            html_content += f"""
            <div class="project-card">
                <div class="project-header">
                    <h2>{info['name']}</h2>
                    <span class="status-badge {status_class}">{info['status'].title()}</span>
                    <span style="margin-left: 10px; class="{activity_class}">Activity: {activity['level']}</span>
                </div>
                <div class="project-content">
                    <p><strong>Description:</strong> {info['description']}</p>
                    <p><strong>Priority:</strong> {info['priority'].title()}</p>
                    <p><strong>Created:</strong> {info['created_date']}</p>
                    <p><strong>Last Updated:</strong> {info['last_updated']}</p>
"""
            
            if project['directory_info']['exists']:
                analysis = project['directory_info']['analysis']
                html_content += f"""
                    <p><strong>Directory:</strong> {project['directory_info']['path']}</p>
                    <p><strong>Files:</strong> {analysis['files']['total']:,} total, {analysis['files']['recent']} modified recently</p>
                    <p><strong>Size:</strong> {analysis['size_mb']} MB</p>
"""
                
                if analysis['git_info']['is_repo']:
                    git_status = analysis['git_info'].get('status', {})
                    if git_status and isinstance(git_status, dict):
                        html_content += f"<p><strong>Git Status:</strong> {git_status.get('modified_files', 0)} uncommitted changes</p>"
            
            if project['technology_stack']:
                html_content += '<div class="tech-stack">'
                for tech in project['technology_stack']:
                    html_content += f'<span class="tech-tag">{tech}</span>'
                html_content += '</div>'
            
            if activity['indicators']:
                html_content += '<p><strong>Activity Indicators:</strong></p><ul>'
                for indicator in activity['indicators']:
                    html_content += f'<li>{indicator}</li>'
                html_content += '</ul>'
            
            html_content += """
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_file

    def run(self):
        """Main execution function"""
        print("[INFO] Starting comprehensive progress report generation...")
        print(f"[INFO] Base directory: {self.base_dir}")
        print(f"[INFO] Reports will be saved to: {self.reports_dir}")
        
        # Load projects
        projects_data = self.load_projects()
        if not projects_data:
            print("[ERROR] Failed to load projects data")
            return False
        
        print(f"[INFO] Found {len(projects_data['projects'])} projects to analyze")
        
        # Generate reports for each project
        project_reports = []
        for project in projects_data['projects']:
            try:
                report = self.generate_project_report(project)
                project_reports.append(report)
            except Exception as e:
                print(f"[WARNING] Error analyzing project {project.get('name', 'Unknown')}: {e}")
                continue
        
        # Generate summary
        summary = self.generate_summary(project_reports)
        
        # Prepare final report data
        self.report_data['projects'] = project_reports
        self.report_data['summary'] = summary
        self.report_data['system_info'] = {
            'base_directory': str(self.base_dir),
            'context_manager_path': str(self.repo_path),
            'python_version': sys.version,
            'platform': os.name
        }
        
        # Save reports in multiple formats
        try:
            json_file = self.save_json_report()
            print(f"[SUCCESS] JSON report saved: {json_file}")
            
            md_file = self.save_markdown_report()
            print(f"[SUCCESS] Markdown report saved: {md_file}")
            
            html_file = self.save_html_report()
            print(f"[SUCCESS] HTML report saved: {html_file}")
            
            print(f"\n[SUCCESS] Progress report generation completed successfully!")
            print(f"[STATS] Analyzed {len(project_reports)} projects")
            print(f"[STATS] {summary['active_projects']} projects show recent activity")
            print(f"[STATS] {summary['total_files']:,} total files across all projects")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error saving reports: {e}")
            return False

def main():
    """Main entry point"""
    generator = ProgressReportGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()