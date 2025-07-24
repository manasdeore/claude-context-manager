#!/usr/bin/env python3
"""
Project Progress Updater
Triggered from the web dashboard to update project status and sync with GitHub
"""

import json
import os
import sys
import subprocess
import requests
from datetime import datetime
from pathlib import Path

class ProjectUpdater:
    def __init__(self):
        self.repo_path = Path(__file__).parent.parent  # Go up one level from scripts/
        self.projects_file = self.repo_path / "projects.json"
        
    def load_projects(self):
        """Load current projects data"""
        try:
            with open(self.projects_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading projects: {e}")
            return None
    
    def save_projects(self, data):
        """Save updated projects data"""
        try:
            with open(self.projects_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving projects: {e}")
            return False
    
    def update_sync_time(self):
        """Update the last sync timestamp"""
        data = self.load_projects()
        if not data:
            return False
        
        # Update metadata
        if 'metadata' not in data:
            data['metadata'] = {}
        
        data['metadata']['last_sync'] = datetime.now().isoformat() + 'Z'
        data['metadata']['last_update_source'] = 'web_dashboard'
        
        return self.save_projects(data)
    
    def simulate_progress_update(self):
        """Simulate updating project progress (for demo purposes)"""
        data = self.load_projects()
        if not data or 'projects' not in data:
            return False
        
        # Find an in-progress project to update
        for project in data['projects']:
            if project['status'] == 'in_progress':
                # Update current task with timestamp
                if 'progress' not in project:
                    project['progress'] = {}
                
                current_time = datetime.now().strftime('%H:%M')
                project['progress']['current_task'] = f"Updated via web dashboard at {current_time}"
                project['last_updated'] = datetime.now().strftime('%Y-%m-%d')
                break
        
        return self.save_projects(data)
    
    def git_commit_and_push(self):
        """Commit changes and push to GitHub"""
        try:
            # Change to repo directory
            os.chdir(self.repo_path)
            
            # Add changes
            subprocess.run(['git', 'add', 'projects.json'], check=True)
            
            # Commit
            commit_message = f"Update project progress via web dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push (this would work if the script runs on a system with git credentials)
            # For demo purposes, we'll just print what would happen
            print(f"Would push commit: {commit_message}")
            # subprocess.run(['git', 'push'], check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def run_update(self):
        """Main update process"""
        print("🔄 Starting project progress update...")
        
        # Update sync time
        if not self.update_sync_time():
            print("❌ Failed to update sync time")
            return False
        
        # Simulate progress update
        if not self.simulate_progress_update():
            print("❌ Failed to update project progress")
            return False
        
        # Commit and push changes
        if not self.git_commit_and_push():
            print("❌ Failed to commit changes")
            return False
        
        print("✅ Project progress updated successfully!")
        return True

def main():
    """Main entry point"""
    updater = ProjectUpdater()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("🧪 Running in test mode...")
        
    success = updater.run_update()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()