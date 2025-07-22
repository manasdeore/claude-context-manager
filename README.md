# Claude Context Manager

A centralized system for tracking all Claude AI instances, ongoing projects, and their statuses across different devices and sessions.

## 🎯 Purpose

When you run multiple Claude instances across different devices, it's easy to lose track of ongoing projects. This system provides:

- **Centralized project tracking** - All projects in one place
- **Session continuity** - Save and restore context between Claude sessions
- **Quick status overview** - Dashboard view of all ongoing work
- **Consistent documentation** - Templates for project organization

## 📁 Structure

```
claude-context-manager/
├── projects.json           # Main project tracking database
├── projects/              # Individual project documentation
│   └── [project-id].md   # Detailed project files
├── contexts/              # Saved Claude conversation contexts
│   └── [context-id].json # Session snapshots
├── templates/             # Templates for consistency
│   ├── project-template.md
│   └── context-template.json
└── scripts/               # Utility tools
    ├── view-projects.py   # Python dashboard
    └── view-projects.bat  # Windows batch viewer
```

## 🚀 Quick Start

### View Current Projects
```bash
# Windows
scripts\view-projects.bat

# Python (cross-platform)
python scripts/view-projects.py
```

### Start New Project
1. Copy `templates/project-template.md` to `projects/[new-project-id].md`
2. Update the template with your project details
3. Add entry to `projects.json`
4. Start working!

### Save Session Context
Before ending a Claude session:
1. Copy `templates/context-template.json`
2. Fill in current state, progress, and continuation notes
3. Save to `contexts/[context-id].json`

## 📋 Project Status Types

- **in_progress** 🔄 - Currently active
- **completed** ✅ - Finished successfully  
- **paused** ⏸️ - Temporarily stopped
- **cancelled** ❌ - Discontinued
- **pending** 📋 - Not yet started

## 🔧 Workflow

1. **Session Start**: Check `projects.json` for ongoing work
2. **During Work**: Update project status in real-time
3. **Session End**: Save context using template
4. **Regular Sync**: Commit and push changes to GitHub

## 💡 Tips

- Use descriptive project IDs (e.g., `website-redesign-2025`)
- Tag projects for easy filtering
- Save context frequently during long sessions
- Use the viewer scripts to get quick overviews
- Keep the `projects.json` file updated

## 🛠️ Customization

- Modify templates to match your workflow
- Add custom fields to `projects.json` structure
- Extend viewer scripts with filtering/sorting
- Create additional utility scripts as needed

## 📊 Example Usage

```json
{
  "projects": [
    {
      "id": "api-integration-001",
      "name": "REST API Integration",
      "status": "in_progress",
      "priority": "high",
      "claude_instance": "Laptop - Dev Environment",
      "last_updated": "2025-07-22",
      "tags": ["backend", "api", "urgent"]
    }
  ]
}
```

---

**Created**: 2025-07-22  
**Purpose**: Centralized Claude AI project and context management  
**Status**: Active and ready for use

🤖 *Generated with Claude Code* - Your AI-powered development assistant