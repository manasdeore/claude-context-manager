# Project: Claude Context Manager Setup

## Project ID
claude-context-manager-001

## Description
Creating a centralized GitHub repository system to track all Claude AI instances, ongoing projects, and their statuses across different devices and sessions.

## Status
- **Current Status**: in_progress
- **Priority**: high
- **Created**: 2025-07-22
- **Last Updated**: 2025-07-22

## Context
- **Claude Instance**: Desktop - Primary Windows PC
- **Working Directory**: C:\Users\manas\OneDrive - KINBEN INNOVATION PRIVATE LIMITED\Desktop\claude-context-manager
- **GitHub Repo**: TBD (to be created)

## Progress Tracking

### Completed Tasks ✅
- [x] Created project plan file
- [x] Set up folder structure (projects/, contexts/, templates/, scripts/)
- [x] Created main projects.json tracking file
- [x] Built project documentation template
- [x] Built context saving template
- [x] Created Python project viewer script
- [x] Created Windows batch project viewer
- [x] Documented this conversation as first project

### Current Task 🔄
Preparing for git initialization and GitHub repository creation

### Next Tasks 📋
- [ ] Initialize git repository
- [ ] Create GitHub repository
- [ ] Push initial commit to GitHub
- [ ] Test the project viewer scripts
- [ ] Create README.md for the repository

## Files & Resources
- **Main Files**: 
  - `projects.json` - Central project tracking database
  - `claude-context-manager-plan.md` - Project planning document
- **Templates**:
  - `templates/project-template.md` - For new project documentation
  - `templates/context-template.json` - For saving Claude contexts
- **Scripts**:
  - `scripts/view-projects.py` - Python dashboard viewer
  - `scripts/view-projects.bat` - Windows batch viewer
- **Documentation**: Context saved in `contexts/claude-context-manager-001.json`

## Usage Instructions
1. When starting new Claude session: Check projects.json for ongoing work
2. Update project status as work progresses
3. Save context before ending session using context template
4. Run view-projects script for quick overview
5. Push updates to GitHub regularly

## Commands to Remember
```bash
# View projects (Windows)
scripts\view-projects.bat

# View projects (Python)
python scripts\view-projects.py

# Git commands (once initialized)
git add .
git commit -m "Update project status"
git push
```

## Issues & Blockers
- Need to create GitHub repository manually
- Git not yet initialized (waiting for user preference on repo location)

## System Architecture
```
claude-context-manager/
├── projects.json           # Main project tracker
├── projects/              # Individual project folders
│   └── claude-context-manager-001.md
├── contexts/              # Saved Claude contexts
│   └── claude-context-manager-001.json
├── templates/             # Project templates
│   ├── project-template.md
│   └── context-template.json
└── scripts/               # Utility scripts
    ├── view-projects.py
    └── view-projects.bat
```

---
*Last updated by Claude instance: Desktop Primary on 2025-07-22*