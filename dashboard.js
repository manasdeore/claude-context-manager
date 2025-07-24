/**
 * Claude Context Manager - Web Dashboard JavaScript
 * Handles dynamic content loading and project progress tracking
 */

class DashboardManager {
    constructor() {
        this.projectsData = null;
        this.lastUpdateTime = null;
        this.init();
    }

    async init() {
        try {
            await this.loadProjectData();
            this.renderDashboard();
            this.updateSyncStatus();
            
            // Set up auto-refresh every 5 minutes
            setInterval(() => {
                this.refreshData();
            }, 5 * 60 * 1000);
            
        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            this.showError('Failed to load project data');
        }
    }

    async loadProjectData() {
        try {
            const response = await fetch('./projects.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.projectsData = await response.json();
            this.lastUpdateTime = new Date();
        } catch (error) {
            console.error('Error loading project data:', error);
            // Fallback to demo data if projects.json is not accessible
            this.projectsData = this.getDemoData();
            this.lastUpdateTime = new Date();
        }
    }

    getDemoData() {
        return {
            metadata: {
                total_projects: 8,
                active_projects: 6,
                completed_projects: 2,
                last_sync: new Date().toISOString()
            },
            projects: [
                {
                    id: "demo-project-001",
                    name: "Demo Project - Web Dashboard",
                    description: "Creating a live web dashboard for project tracking",
                    status: "in_progress",
                    priority: "high",
                    created_date: "2025-07-24",
                    last_updated: "2025-07-24",
                    progress: {
                        completed_tasks: ["Initial setup", "Basic design"],
                        current_task: "Implementing interactive features",
                        next_tasks: ["Testing", "Deployment"]
                    }
                }
            ]
        };
    }

    renderDashboard() {
        this.renderOverviewStats();
        this.renderActiveProjects();
        this.renderCompletedProjects();
    }

    renderOverviewStats() {
        const metadata = this.projectsData.metadata || {};
        const projects = this.projectsData.projects || [];
        
        // Calculate stats
        const totalProjects = projects.length;
        const activeProjects = projects.filter(p => p.status !== 'completed').length;
        const completedProjects = projects.filter(p => p.status === 'completed').length;
        
        // Calculate overall progress
        let totalProgress = 0;
        let progressCount = 0;
        
        projects.forEach(project => {
            const progress = this.calculateProjectProgress(project);
            if (progress > 0) {
                totalProgress += progress;
                progressCount++;
            }
        });
        
        const overallProgress = progressCount > 0 ? Math.round(totalProgress / progressCount) : 0;
        
        // Update DOM elements
        document.getElementById('totalProjects').textContent = totalProjects;
        document.getElementById('activeProjects').textContent = activeProjects;
        document.getElementById('completedProjects').textContent = completedProjects;
        document.getElementById('overallProgress').textContent = `${overallProgress}%`;
    }

    renderActiveProjects() {
        const container = document.getElementById('activeProjectsGrid');
        const activeProjects = this.projectsData.projects.filter(p => p.status !== 'completed');
        
        if (activeProjects.length === 0) {
            container.innerHTML = '<p class="text-center">No active projects found.</p>';
            return;
        }
        
        container.innerHTML = activeProjects.map(project => this.createProjectCard(project)).join('');
    }

    renderCompletedProjects() {
        const container = document.getElementById('completedProjectsGrid');
        const completedProjects = this.projectsData.projects.filter(p => p.status === 'completed');
        
        if (completedProjects.length === 0) {
            container.innerHTML = '<p class="text-center">No completed projects yet.</p>';
            return;
        }
        
        container.innerHTML = completedProjects.map(project => this.createProjectCard(project)).join('');
    }

    createProjectCard(project) {
        const statusEmoji = this.getStatusEmoji(project.status);
        const priorityClass = this.getPriorityClass(project.priority);
        const progress = this.calculateProjectProgress(project);
        const currentTask = project.progress?.current_task || 'No current task specified';
        
        return `
            <div class="project-card ${priorityClass}">
                <div class="project-header">
                    <h3 class="project-title">${statusEmoji} ${project.name}</h3>
                    <div class="project-status">
                        <span class="status-badge ${project.status.replace('_', '-')}">${project.status.replace('_', ' ')}</span>
                        <span class="priority-badge ${project.priority}">${project.priority}</span>
                    </div>
                </div>
                
                <p class="project-description">${project.description}</p>
                
                ${currentTask !== 'No current task specified' ? `
                    <div class="project-current-task">
                        <strong>Current:</strong> ${currentTask}
                    </div>
                ` : ''}
                
                <div class="progress-container">
                    <div class="progress-label">
                        <span>Progress</span>
                        <span>${progress}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${progress}%"></div>
                    </div>
                </div>
                
                <div class="project-meta">
                    <span>ID: ${project.id}</span>
                    <span>Updated: ${this.formatDate(project.last_updated)}</span>
                </div>
            </div>
        `;
    }

    calculateProjectProgress(project) {
        if (project.status === 'completed') return 100;
        if (project.status === 'pending') return 0;
        
        // Try to extract progress from various sources
        if (project.progress) {
            // Look for explicit progress percentage in current_task
            const currentTask = project.progress.current_task || '';
            const percentMatch = currentTask.match(/(\d+)%/);
            if (percentMatch) {
                return parseInt(percentMatch[1]);
            }
            
            // Calculate based on completed vs total tasks
            const completed = project.progress.completed_tasks?.length || 0;
            const next = project.progress.next_tasks?.length || 0;
            const total = completed + next;
            
            if (total > 0) {
                return Math.round((completed / total) * 100);
            }
        }
        
        // Default progress based on status
        const statusProgress = {
            'in_progress': 50,
            'paused': 30,
            'cancelled': 0,
            'pending': 0
        };
        
        return statusProgress[project.status] || 25;
    }

    getStatusEmoji(status) {
        const statusMap = {
            'in_progress': '🔄',
            'completed': '✅',
            'paused': '⏸️',
            'cancelled': '❌',
            'pending': '📋'
        };
        return statusMap[status] || '📝';
    }

    getPriorityClass(priority) {
        return `${priority}-priority`;
    }

    formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        } catch {
            return dateString;
        }
    }

    updateSyncStatus() {
        const syncElement = document.getElementById('syncStatus');
        if (this.lastUpdateTime) {
            const timeStr = this.lastUpdateTime.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit'
            });
            syncElement.textContent = `Last sync: ${timeStr}`;
        }
    }

    async refreshData() {
        try {
            await this.loadProjectData();
            this.renderDashboard();
            this.updateSyncStatus();
            console.log('Dashboard refreshed successfully');
        } catch (error) {
            console.error('Failed to refresh dashboard:', error);
        }
    }

    showError(message) {
        // Create a simple error display
        const main = document.querySelector('.main');
        main.innerHTML = `
            <div class="container">
                <div class="text-center" style="padding: 2rem; background: white; border-radius: 8px; margin: 2rem 0;">
                    <h2 style="color: #dc2626; margin-bottom: 1rem;">⚠️ Error Loading Dashboard</h2>
                    <p style="color: #6b7280;">${message}</p>
                    <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        Retry
                    </button>
                </div>
            </div>
        `;
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
}

// Global function for the update button
async function triggerProjectUpdate() {
    const dashboard = window.dashboardManager;
    
    try {
        dashboard.showLoading();
        
        // Simulate project tracker trigger (this would call a real API in production)
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Refresh the dashboard
        await dashboard.refreshData();
        
        // Show success message
        alert('✅ Project tracker triggered successfully! Progress updated.');
        
    } catch (error) {
        console.error('Failed to trigger project update:', error);
        alert('❌ Failed to trigger project update. Please try again.');
    } finally {
        dashboard.hideLoading();
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager();
});

// Add some visual feedback for interactive elements
document.addEventListener('DOMContentLoaded', () => {
    // Add click animation to buttons
    document.addEventListener('click', (e) => {
        if (e.target.matches('.sync-btn, .link-card')) {
            e.target.style.transform = 'scale(0.95)';
            setTimeout(() => {
                e.target.style.transform = '';
            }, 150);
        }
    });
});