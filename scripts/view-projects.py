#!/usr/bin/env python3
"""
Claude Context Manager - Project Viewer
Quick dashboard to view all ongoing projects and their statuses
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_projects():
    """Load projects from projects.json"""
    script_dir = Path(__file__).parent
    projects_file = script_dir.parent / "projects.json"
    
    if not projects_file.exists():
        print("❌ projects.json not found!")
        return None
    
    with open(projects_file, 'r') as f:
        return json.load(f)

def format_status(status):
    """Add emoji to status for visual clarity"""
    status_map = {
        'in_progress': '🔄 In Progress',
        'completed': '✅ Completed',
        'paused': '⏸️  Paused',
        'cancelled': '❌ Cancelled',
        'pending': '📋 Pending'
    }
    return status_map.get(status, f"📝 {status}")

def format_priority(priority):
    """Add emoji to priority"""
    priority_map = {
        'high': '🔥 High',
        'medium': '⚡ Medium',
        'low': '💤 Low'
    }
    return priority_map.get(priority, f"📌 {priority}")

def display_projects(data):
    """Display projects in a nice format"""
    if not data or 'projects' not in data:
        print("❌ No projects found!")
        return
    
    projects = data['projects']
    metadata = data.get('metadata', {})
    
    print("=" * 60)
    print("🎯 CLAUDE CONTEXT MANAGER - PROJECT DASHBOARD")
    print("=" * 60)
    print(f"📊 Total Projects: {metadata.get('total_projects', len(projects))}")
    print(f"🏃 Active Projects: {metadata.get('active_projects', 'Unknown')}")
    print(f"🕐 Last Sync: {metadata.get('last_sync', 'Unknown')}")
    print("=" * 60)
    
    for i, project in enumerate(projects, 1):
        print(f"\n📁 PROJECT {i}: {project['name']}")
        print(f"   ID: {project['id']}")
        print(f"   Status: {format_status(project['status'])}")
        print(f"   Priority: {format_priority(project['priority'])}")
        print(f"   Created: {project['created_date']}")
        print(f"   Updated: {project['last_updated']}")
        
        if 'description' in project:
            print(f"   Description: {project['description']}")
        
        # Show progress if available
        if 'progress' in project:
            progress = project['progress']
            completed = len(progress.get('completed_tasks', []))
            print(f"   Progress: {completed} tasks completed")
            
            if 'current_task' in progress:
                print(f"   Current: {progress['current_task']}")
        
        print(f"   Instance: {project.get('claude_instance', 'Unknown')}")
        
        if 'tags' in project:
            tags = ' '.join([f"#{tag}" for tag in project['tags']])
            print(f"   Tags: {tags}")
        
        print("-" * 50)
    
    print(f"\n💡 Tip: Use templates in ./templates/ for new projects")
    print(f"🔧 Update projects.json to modify project details")

def main():
    """Main function"""
    print("Loading Claude Context Manager...")
    
    data = load_projects()
    if data:
        display_projects(data)
    else:
        print("Failed to load project data.")

if __name__ == "__main__":
    main()