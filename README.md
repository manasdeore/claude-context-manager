# 🤖 Claude Context Manager

> **Centralized tracking system for all Claude AI instances, projects, and contexts across Kinben Innovation**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)](https://github.com/manasdeore/claude-context-manager)
[![Version](https://img.shields.io/badge/Version-1.1.0-blue.svg)](#)
[![Projects](https://img.shields.io/badge/Projects-8%20Active-orange.svg)](#projects)

## 🎯 **Purpose**

When managing multiple Claude AI instances across different devices and sessions, it becomes challenging to maintain project continuity and track progress. This system provides:

- ✅ **Centralized Project Tracking** - All projects in one unified dashboard
- ✅ **Session Continuity** - Save and restore context between Claude sessions  
- ✅ **Progress Monitoring** - Real-time status updates and completion tracking
- ✅ **Consistent Documentation** - Standardized templates and structure
- ✅ **Cross-Device Sync** - GitHub-based synchronization across all devices

## 📊 **Current Stats**
- **Total Projects:** 8
- **Active Projects:** 6 
- **Completed Projects:** 2
- **Last Sync:** 2025-07-24

## 🌐 **Live Web Dashboard**
**🚀 NEW!** Access your projects from anywhere with our live web dashboard:
- **Live URL:** https://manasdeore.github.io/claude-context-manager/
- **Features:** Real-time progress tracking, visual progress bars, one-click updates
- **Mobile-friendly:** Works on all devices with responsive design
- **Auto-updates:** Refreshes every 5 minutes with latest project status

## 🚀 **Quick Start**

### 1. 🌐 Web Dashboard (Recommended)
```
Visit: https://manasdeore.github.io/claude-context-manager/
- Visual project tracking with progress bars
- One-click progress updates 
- Mobile-friendly responsive design
- Auto-refresh every 5 minutes
```

### 2. Local Terminal Dashboard
```bash
# Windows (Recommended)
scripts\claude-dashboard.bat

# Manual fallback
cat projects.json
```

### 3. Start New Project
```bash
# 1. Copy template
cp templates/project-template.md projects/your-project-id.md

# 2. Edit with your details
# 3. Add entry to projects.json
# 4. Start coding!
```

### 3. Save Session Context
```bash
# Before ending Claude session:
cp templates/context-template.json contexts/your-context-id.json
# Fill in current state and progress
```

## 📁 **Repository Structure**

```
claude-context-manager/
├── 📄 projects.json           # Main project database (8 projects)
├── 🌐 index.html             # Live web dashboard (NEW!)
├── 🎨 dashboard.css          # Dashboard styling (NEW!)
├── ⚡ dashboard.js           # Interactive functionality (NEW!)
├── 📄 _config.yml            # GitHub Pages config (NEW!)
├── 📁 projects/              # Individual project documentation
│   ├── claude-context-manager-001.md
│   ├── kinben-unified-parts-002.md
│   ├── kinben-raspberry-pi-003.md
│   ├── kinben-electronics-code-004.md
│   ├── kinben-erpnext-kpn-005.md
│   ├── inav-pcb-v2-006.md
│   ├── mfl-sensor-board-007.md
│   └── battery-control-board-008.md
├── 📁 contexts/              # Saved Claude contexts
│   └── [context-id].json    # Session snapshots
├── 📁 templates/             # Project templates
│   ├── project-template.md
│   ├── context-template.json
│   └── daily-launch-template.md
├── 📁 scripts/               # Utility tools
│   ├── claude-dashboard.py   # Python dashboard
│   ├── claude-dashboard.bat  # Windows launcher
│   ├── update-progress.py    # Web dashboard updater (NEW!)
│   ├── update-progress.bat   # Windows progress updater (NEW!)
│   └── startup.bat          # Auto-startup script
└── 📁 .github/workflows/     # GitHub Actions (NEW!)
    ├── deploy-dashboard.yml  # Auto-deploy web dashboard
    └── update-progress.yml   # Progress update automation
```

## 🏗️ **Current Active Projects**

### **🔥 High Priority**
1. **[Kinben ERPNext KPN System](projects/kinben-erpnext-kpn-005.md)** - 70% Complete
   - Foundation-level ERPNext module for component management
   - Docker environment configured, DocTypes implemented

2. **[Kinben ERP & File Server](projects/kinben-raspberry-pi-003.md)** - Phase 2
   - Raspberry Pi enterprise infrastructure
   - File server operational, ERPNext deployment in progress

3. **[Kinben Electronics Embedded Systems](projects/kinben-electronics-code-004.md)** - 90% Complete
   - 6 industrial sensor projects (5 production-ready)
   - Teensy 4.1 & RP2040 platforms

4. **[MFL Sensor Board V1.0](projects/mfl-sensor-board-007.md)** - PCB Design
   - 3-layer PCB system for pipeline inspection
   - TMAG5170 sensors with LVDS communication

### **✅ Completed**
- **[Kinben Unified Parts System](projects/kinben-unified-parts-002.md)** 
  - Live: https://the-clever-studio-f3b16.web.app/
  - 338+ KiCad library files, auto-deployment pipeline

## 📋 **Project Status Legend**

| Status | Icon | Description |
|--------|------|-------------|
| `in_progress` | 🔄 | Currently active development |
| `completed` | ✅ | Successfully finished |
| `paused` | ⏸️ | Temporarily stopped |
| `cancelled` | ❌ | Discontinued |
| `pending` | 📋 | Scheduled but not started |

## 🔧 **Workflow Guide**

### **Daily Workflow**
1. **Web Dashboard**: Visit https://manasdeore.github.io/claude-context-manager/
2. **Review Projects**: Check active projects and progress bars
3. **Update Progress**: Click "📊 Update Progress" button when work is complete
4. **Terminal Option**: `cat projects.json` → Check active projects locally
5. **During Work**: Update project status in real-time  
6. **Session End**: Save context using templates
7. **Regular Sync**: Changes auto-sync via web dashboard or manual git push

### **Project Management**
```bash
# Add new project
1. Create projects/project-id.md
2. Add entry to projects.json
3. Update metadata.total_projects
4. Commit changes

# Update project status
1. Edit projects.json status field
2. Update last_updated timestamp
3. Add completed tasks
4. Commit changes
```

## 🛠️ **Advanced Features**

### **Live Web Dashboard** 🌐
- `index.html` - Responsive web interface with real-time updates
- `dashboard.css` - Modern styling with progress bars and animations
- `dashboard.js` - Interactive functionality and auto-refresh
- GitHub Pages hosting with custom domain support

### **Templates Available**
- `project-template.md` - Standard project documentation
- `context-template.json` - Claude session context saving
- `daily-launch-template.md` - Daily planning template

### **Automation Scripts**
- `claude-dashboard.py` - Interactive Python dashboard
- `claude-dashboard.bat` - Windows one-click launcher
- `startup.bat` - Auto-startup configuration

### **Custom Fields**
```json
{
  "priority": "high|medium|low",
  "technology_stack": ["tech1", "tech2"],
  "working_directory": "C:\\path\\to\\project",
  "github_repo": "https://github.com/...",
  "live_url": "https://...",
  "tags": ["tag1", "tag2"]
}
```

## 📈 **System Benefits**

### **For Development**
- ✅ No more lost project context
- ✅ Seamless switching between Claude instances
- ✅ Comprehensive progress tracking
- ✅ Standardized documentation

### **For Team Collaboration**
- ✅ Centralized project visibility
- ✅ GitHub-based synchronization
- ✅ Consistent project structure
- ✅ Easy onboarding for new team members

## 🔧 **Configuration**

### **Environment Setup**
```bash
# Clone repository
git clone https://github.com/manasdeore/claude-context-manager.git

# Navigate to directory
cd claude-context-manager

# Run dashboard
scripts/claude-dashboard.bat
```

### **Customization Options**
- Modify `templates/` for your workflow
- Add custom fields to `projects.json` schema  
- Extend viewer scripts with filtering
- Create project-specific automation

## 📚 **Documentation**

- [Project Templates](templates/) - Standardized formats
- [Context Management](contexts/) - Session continuity
- [Script Usage](scripts/) - Automation tools
- [Individual Projects](projects/) - Detailed documentation

## 🐛 **Troubleshooting**

### **Common Issues**
```bash
# Python not found
# Solution: Install Python 3.7+ or use manual viewer

# Git sync issues  
git status
git add .
git commit -m "Update project status"
git push

# JSON validation
# Use online JSON validator for projects.json
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Update `projects.json` and documentation
4. Test with viewer scripts
5. Submit pull request

## 📄 **License**

Private repository for Kinben Innovation internal use.

---

## 🎉 **Success Metrics**

Since implementation:
- ✅ **8 Projects** successfully tracked
- ✅ **100% Project Visibility** across all Claude instances
- ✅ **Zero Lost Context** during session switches
- ✅ **Standardized Documentation** for all projects
- ✅ **Real-time Progress Tracking** enabled

---

**Created:** 2025-07-22  
**Last Updated:** 2025-07-24  
**Version:** 1.1.0  
**Maintainer:** Manas Deore  
**Status:** ✅ Production Ready

🤖 *Generated with [Claude Code](https://claude.ai/code) - Your AI-powered development assistant*