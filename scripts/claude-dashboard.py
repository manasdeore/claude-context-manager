#!/usr/bin/env python3
"""
Claude Context Manager - Interactive Dashboard
Terminal-based startup application for daily project management
"""

import json
import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print Claude dashboard banner"""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            🤖 CLAUDE CONTEXT MANAGER DASHBOARD               ║
║                                                              ║
║              Your AI Development Command Center              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BLUE}Good morning! Ready to continue your projects?{Colors.ENDC}
{Colors.YELLOW}Date: {datetime.now().strftime('%A, %B %d, %Y')}{Colors.ENDC}
{Colors.YELLOW}Time: {datetime.now().strftime('%I:%M %p')}{Colors.ENDC}

"""
    print(banner)

def load_projects():
    """Load projects from projects.json"""
    try:
        script_dir = Path(__file__).parent
        projects_file = script_dir.parent / "projects.json"
        
        if not projects_file.exists():
            print(f"{Colors.RED}❌ projects.json not found!{Colors.ENDC}")
            return None
        
        with open(projects_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Colors.RED}❌ Error loading projects: {e}{Colors.ENDC}")
        return None

def format_status_emoji(status):
    """Get emoji for project status"""
    status_map = {
        'in_progress': '🔄',
        'completed': '✅',
        'paused': '⏸️',
        'cancelled': '❌',
        'pending': '📋'
    }
    return status_map.get(status, '📝')

def format_priority_emoji(priority):
    """Get emoji for priority level"""
    priority_map = {
        'high': '🔥',
        'medium': '⚡',
        'low': '💤'
    }
    return priority_map.get(priority, '📌')

def display_project_summary(data):
    """Display project summary"""
    if not data or 'projects' not in data:
        print(f"{Colors.RED}❌ No projects found!{Colors.ENDC}")
        return []
    
    projects = data['projects']
    metadata = data.get('metadata', {})
    
    print(f"{Colors.GREEN}📊 PROJECT OVERVIEW{Colors.ENDC}")
    print(f"   Total: {metadata.get('total_projects', len(projects))} projects")
    print(f"   Active: {metadata.get('active_projects', 'Unknown')} in progress")
    print(f"   Last sync: {metadata.get('last_sync', 'Unknown')}")
    print()
    
    # Separate active and completed projects
    active_projects = [p for p in projects if p['status'] != 'completed']
    completed_projects = [p for p in projects if p['status'] == 'completed']
    
    # Display active projects
    if active_projects:
        print(f"{Colors.BOLD}{Colors.YELLOW}🚀 ACTIVE PROJECTS - READY TO WORK{Colors.ENDC}")
        print("=" * 60)
        
        for i, project in enumerate(active_projects, 1):
            status_emoji = format_status_emoji(project['status'])
            priority_emoji = format_priority_emoji(project['priority'])
            
            print(f"{Colors.BOLD}[{i}] {status_emoji} {project['name']}{Colors.ENDC}")
            print(f"    {Colors.CYAN}ID:{Colors.ENDC} {project['id']}")
            print(f"    {Colors.CYAN}Status:{Colors.ENDC} {status_emoji} {project['status'].title()}")
            print(f"    {Colors.CYAN}Priority:{Colors.ENDC} {priority_emoji} {project['priority'].title()}")
            
            # Show current task if available
            if 'progress' in project and 'current_task' in project['progress']:
                print(f"    {Colors.GREEN}Current:{Colors.ENDC} {project['progress']['current_task']}")
            
            # Show working directory if available
            if 'working_directory' in project:
                print(f"    {Colors.BLUE}Folder:{Colors.ENDC} {project['working_directory']}")
            elif 'folder_path' in project:
                print(f"    {Colors.BLUE}Folder:{Colors.ENDC} {project['folder_path']}")
            
            print(f"    {Colors.YELLOW}Updated:{Colors.ENDC} {project['last_updated']}")
            print()
    
    # Display completed projects (summary)
    if completed_projects:
        print(f"{Colors.BOLD}{Colors.GREEN}✅ COMPLETED PROJECTS{Colors.ENDC}")
        print("-" * 60)
        for project in completed_projects:
            print(f"   ✅ {project['name']} - {project.get('version', 'v1.0')}")
        print()
    
    return active_projects

def show_quick_links():
    """Display quick access information"""
    print(f"{Colors.BOLD}{Colors.BLUE}🔗 QUICK ACCESS{Colors.ENDC}")
    print("=" * 60)
    print(f"{Colors.GREEN}🌐 Live Systems:{Colors.ENDC}")
    print("   • Parts Reference: https://the-clever-studio-f3b16.web.app/")
    print("   • Pi File Server: http://192.168.1.25 (or \\\\192.168.1.25\\KinbenFiles)")
    print()
    print(f"{Colors.GREEN}📁 Main Working Directories:{Colors.ENDC}")
    print("   • Pi Dev: Desktop\\Kinben ERP Setup")
    print("   • Electronics: Documents\\Kinben Electronics Repo Folder\\Code")
    print("   • Parts System: Desktop\\Kinben-Unified-Parts-Reference-System")
    print()
    print(f"{Colors.GREEN}📋 GitHub Repositories:{Colors.ENDC}")
    print("   • Context Manager: https://github.com/manasdeore/claude-context-manager (🔒 private)")
    print("   • Parts System: https://github.com/Kinben-Electronics-Team/Kinben-Unified-Parts-Reference-System")
    print()

def show_menu_options():
    """Display menu options"""
    print(f"{Colors.BOLD}{Colors.CYAN}🎯 WHAT WOULD YOU LIKE TO DO?{Colors.ENDC}")
    print("=" * 60)
    print(f"{Colors.YELLOW}[1-9]{Colors.ENDC} - Work on specific project (enter project number)")
    print(f"{Colors.YELLOW}[l]{Colors.ENDC}   - Show quick Links and access info")
    print(f"{Colors.YELLOW}[r]{Colors.ENDC}   - Refresh project status")
    print(f"{Colors.YELLOW}[h]{Colors.ENDC}   - Show Help and usage instructions")
    print(f"{Colors.YELLOW}[q]{Colors.ENDC}   - Quit dashboard")
    print()

def show_help():
    """Display help information"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.BLUE}📚 CLAUDE DASHBOARD HELP{Colors.ENDC}")
    print("=" * 60)
    print()
    print(f"{Colors.BOLD}Daily Workflow:{Colors.ENDC}")
    print("1. Start your day by running this dashboard")
    print("2. Review active projects and their current status")
    print("3. Choose a project to work on (1-9)")
    print("4. Work on the project using Claude")
    print("5. Update project status when done")
    print()
    print(f"{Colors.BOLD}Project Management:{Colors.ENDC}")
    print("• Each project has detailed documentation in projects/[project-id].md")
    print("• Context files store session history in contexts/")
    print("• Use templates for consistent progress reporting")
    print("• Update projects.json to reflect current status")
    print()
    print(f"{Colors.BOLD}Key Files:{Colors.ENDC}")
    print("• DAILY_LAUNCH_INSTRUCTIONS.md - Comprehensive startup guide")
    print("• projects.json - Main project database")
    print("• templates/ - Templates for documentation")
    print("• scripts/ - Utility scripts including this dashboard")
    print()
    print(f"{Colors.BOLD}Tips:{Colors.ENDC}")
    print("• Run 'scripts\\view-projects.bat' for detailed project view")
    print("• Check GitHub repositories for issues and updates")
    print("• Use progress templates for consistent tracking")
    print("• Commit changes to GitHub regularly")
    print()
    print(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.ENDC}")
    input()

def open_project_folder(project):
    """Open project working directory"""
    folder = project.get('working_directory', project.get('folder_path', ''))
    if folder and folder != 'N/A':
        try:
            if os.name == 'nt':  # Windows
                # Convert forward slashes and handle relative paths
                if folder.startswith('./projects/'):
                    script_dir = Path(__file__).parent.parent
                    folder = script_dir / folder[2:]
                folder = str(folder).replace('/', '\\')
                subprocess.run(['explorer', folder], check=True)
            else:  # Unix/Linux/Mac
                subprocess.run(['open', folder], check=True)
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Could not open folder: {e}{Colors.ENDC}")
            return False
    return False

def project_action_menu(project):
    """Show actions for selected project"""
    clear_screen()
    print_banner()
    
    status_emoji = format_status_emoji(project['status'])
    priority_emoji = format_priority_emoji(project['priority'])
    
    print(f"{Colors.BOLD}{Colors.GREEN}📁 PROJECT SELECTED{Colors.ENDC}")
    print("=" * 60)
    print(f"{Colors.BOLD}{status_emoji} {project['name']}{Colors.ENDC}")
    print(f"   Status: {status_emoji} {project['status'].title()}")
    print(f"   Priority: {priority_emoji} {project['priority'].title()}")
    print(f"   Description: {project['description']}")
    print()
    
    if 'progress' in project and 'current_task' in project['progress']:
        print(f"{Colors.YELLOW}🔄 Current Task:{Colors.ENDC} {project['progress']['current_task']}")
        print()
    
    print(f"{Colors.BOLD}{Colors.CYAN}🎯 PROJECT ACTIONS{Colors.ENDC}")
    print("-" * 40)
    print(f"{Colors.YELLOW}[1]{Colors.ENDC} Open project folder")
    print(f"{Colors.YELLOW}[2]{Colors.ENDC} View detailed project documentation")
    print(f"{Colors.YELLOW}[3]{Colors.ENDC} Show recent context/progress")
    print(f"{Colors.YELLOW}[4]{Colors.ENDC} Copy project info to clipboard")
    print(f"{Colors.YELLOW}[b]{Colors.ENDC} Back to main menu")
    print()
    
    while True:
        choice = input(f"{Colors.BOLD}Choose action: {Colors.ENDC}").strip().lower()
        
        if choice == '1':
            if open_project_folder(project):
                print(f"{Colors.GREEN}✅ Opened project folder!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Could not open project folder{Colors.ENDC}")
            time.sleep(2)
            break
            
        elif choice == '2':
            project_file = f"./projects/{project['id']}.md"
            if os.path.exists(project_file):
                if os.name == 'nt':
                    os.system(f'start notepad "{project_file}"')
                else:
                    os.system(f'open "{project_file}"')
                print(f"{Colors.GREEN}✅ Opening project documentation...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Project documentation not found{Colors.ENDC}")
            time.sleep(2)
            break
            
        elif choice == '3':
            print(f"{Colors.BLUE}📋 Recent Progress:{Colors.ENDC}")
            if 'progress' in project:
                progress = project['progress']
                if 'completed_tasks' in progress:
                    print(f"{Colors.GREEN}✅ Completed:{Colors.ENDC}")
                    for task in progress['completed_tasks'][-3:]:  # Last 3 tasks
                        print(f"   • {task}")
                if 'next_tasks' in progress:
                    print(f"{Colors.YELLOW}📋 Next Tasks:{Colors.ENDC}")
                    for task in progress['next_tasks'][:3]:  # First 3 tasks
                        print(f"   • {task}")
            print(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            input()
            break
            
        elif choice == '4':
            project_info = f"Project: {project['name']}\nID: {project['id']}\nStatus: {project['status']}\nFolder: {project.get('working_directory', 'N/A')}"
            print(f"{Colors.GREEN}✅ Project info ready to copy:{Colors.ENDC}\n{project_info}")
            print(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            input()
            break
            
        elif choice == 'b':
            break
        else:
            print(f"{Colors.RED}❌ Invalid choice. Please try again.{Colors.ENDC}")

def main():
    """Main dashboard loop"""
    try:
        while True:
            clear_screen()
            print_banner()
            
            data = load_projects()
            if not data:
                print(f"{Colors.RED}❌ Could not load project data. Exiting.{Colors.ENDC}")
                return
            
            active_projects = display_project_summary(data)
            show_menu_options()
            
            choice = input(f"{Colors.BOLD}Your choice: {Colors.ENDC}").strip().lower()
            
            # Handle project selection (1-9)
            if choice.isdigit():
                project_num = int(choice)
                if 1 <= project_num <= len(active_projects):
                    selected_project = active_projects[project_num - 1]
                    project_action_menu(selected_project)
                else:
                    print(f"{Colors.RED}❌ Invalid project number. Try again.{Colors.ENDC}")
                    time.sleep(2)
            
            # Handle menu options
            elif choice == 'l':
                clear_screen()
                print_banner()
                show_quick_links()
                print(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
                input()
            
            elif choice == 'r':
                print(f"{Colors.BLUE}🔄 Refreshing project data...{Colors.ENDC}")
                time.sleep(1)
                continue
            
            elif choice == 'h':
                show_help()
            
            elif choice == 'q':
                print(f"\n{Colors.BOLD}{Colors.GREEN}👋 Happy coding! See you next session.{Colors.ENDC}")
                print(f"{Colors.CYAN}💡 Tip: Run this dashboard anytime to check project status{Colors.ENDC}\n")
                break
            
            else:
                print(f"{Colors.RED}❌ Invalid choice. Please try again.{Colors.ENDC}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}👋 Dashboard closed. Happy coding!{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ An error occurred: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Please check the logs and try again.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()