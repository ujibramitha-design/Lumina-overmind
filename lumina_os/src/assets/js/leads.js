// Leads Management JavaScript for HUNTER_AGENT_AI_MARKETING_DIGITAL

document.addEventListener('DOMContentLoaded', function() {
    console.log('Leads management initialized');
    
    // Initialize leads table
    initializeLeadsTable();
    
    // Setup event listeners
    setupLeadsEventListeners();
    
    // Initialize filters
    initializeFilters();
    
    // Setup real-time updates
    setupLeadUpdates();
});

// Initialize Leads Table
function initializeLeadsTable() {
    // Initialize DataTable if available
    if ($.fn.DataTable) {
        $('#leadsTable').DataTable({
            responsive: true,
            pageLength: 25,
            order: [[7, 'desc']], // Sort by date column
            language: {
                search: 'Search leads:',
                lengthMenu: 'Show _MENU_ leads',
                info: 'Showing _START_ to _END_ of _TOTAL_ leads',
                paginate: {
                    first: 'First',
                    last: 'Last',
                    next: 'Next',
                    previous: 'Previous'
                }
            }
        });
    }
    
    // Add row hover effects
    const tableRows = document.querySelectorAll('#leadsTable tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Setup Leads Event Listeners
function setupLeadsEventListeners() {
    // View lead details
    const viewButtons = document.querySelectorAll('[data-action="view-lead"]');
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            showLeadDetails(leadId);
        });
    });
    
    // Contact lead
    const contactButtons = document.querySelectorAll('[data-action="contact-lead"]');
    contactButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            contactLead(leadId);
        });
    });
    
    // Edit lead
    const editButtons = document.querySelectorAll('[data-action="edit-lead"]');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            editLead(leadId);
        });
    });
    
    // Delete lead
    const deleteButtons = document.querySelectorAll('[data-action="delete-lead"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            deleteLead(leadId);
        });
    });
    
    // Bulk actions
    const bulkActions = document.getElementById('bulkActions');
    if (bulkActions) {
        bulkActions.addEventListener('change', function() {
            handleBulkAction(this.value);
        });
    }
    
    // Select all checkbox
    const selectAllCheckbox = document.querySelector('#selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('#leadsTable tbody input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionsVisibility();
        });
    }
    
    // Individual checkboxes
    const checkboxes = document.querySelectorAll('#leadsTable tbody input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActionsVisibility();
        });
    });
}

// Initialize Filters
function initializeFilters() {
    // Status filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            filterLeads('status', this.value);
        });
    }
    
    // Score filter
    const scoreFilter = document.getElementById('scoreFilter');
    if (scoreFilter) {
        scoreFilter.addEventListener('change', function() {
            filterLeads('score', this.value);
        });
    }
    
    // Source filter
    const sourceFilter = document.getElementById('sourceFilter');
    if (sourceFilter) {
        sourceFilter.addEventListener('change', function() {
            filterLeads('source', this.value);
        });
    }
    
    // Date range filter
    const dateRangeFilter = document.getElementById('dateRangeFilter');
    if (dateRangeFilter) {
        dateRangeFilter.addEventListener('change', function() {
            filterLeads('dateRange', this.value);
        });
    }
    
    // Search input
    const searchInput = document.getElementById('leadSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            searchLeads(this.value);
        }, 300));
    }
}

// Show Lead Details
function showLeadDetails(leadId) {
    // Fetch lead details from API
    fetch(`/api/leads/${leadId}`)
        .then(response => response.json())
        .then(lead => {
            populateLeadDetailsModal(lead);
            const modal = new bootstrap.Modal(document.getElementById('leadDetailsModal'));
            modal.show();
        })
        .catch(error => {
            console.log('Error fetching lead details:', error);
            showNotification('Error loading lead details', 'error');
        });
}

// Populate Lead Details Modal
function populateLeadDetailsModal(lead) {
    const modal = document.getElementById('leadDetailsModal');
    if (!modal) return;
    
    // Update personal information
    modal.querySelector('#leadName').textContent = lead.name;
    modal.querySelector('#leadPhone').textContent = lead.phone;
    modal.querySelector('#leadEmail').textContent = lead.email;
    modal.querySelector('#leadLocation').textContent = lead.location;
    
    // Update lead information
    modal.querySelector('#leadScore').innerHTML = `<span class="badge bg-${getScoreColor(lead.score)}">${lead.score}</span>`;
    modal.querySelector('#leadSource').textContent = lead.source;
    modal.querySelector('#leadStatus').innerHTML = `<span class="badge bg-${getStatusColor(lead.status)}">${lead.status}</span>`;
    modal.querySelector('#leadDate').textContent = formatDate(lead.date);
    
    // Update requirements
    modal.querySelector('#leadRequirements').textContent = lead.requirements || 'No specific requirements';
    
    // Update activity history
    const activityHistory = modal.querySelector('#activityHistory');
    if (activityHistory && lead.activities) {
        activityHistory.innerHTML = lead.activities.map(activity => `
            <div class="timeline-item">
                <small class="text-muted">${formatDateTime(activity.timestamp)}</small>
                <p>${activity.description}</p>
            </div>
        `).join('');
    }
    
    // Update action buttons
    const contactBtn = modal.querySelector('#contactLeadBtn');
    if (contactBtn) {
        contactBtn.dataset.leadId = lead.id;
        contactBtn.dataset.leadPhone = lead.phone;
    }
}

// Contact Lead
function contactLead(leadId) {
    const leadPhone = document.querySelector(`[data-action="contact-lead"][data-lead-id="${leadId}"]`)?.dataset.leadPhone;
    
    if (leadPhone) {
        // Open phone dialer
        window.location.href = `tel:${leadPhone}`;
        
        // Log the contact attempt
        logLeadActivity(leadId, 'Contact attempted via phone');
        
        showNotification(`Dialing ${leadPhone}...`, 'info');
    } else {
        showNotification('Phone number not available', 'warning');
    }
}

// Edit Lead
function editLead(leadId) {
    // Fetch lead data and populate edit form
    fetch(`/api/leads/${leadId}`)
        .then(response => response.json())
        .then(lead => {
            populateEditForm(lead);
            const modal = new bootstrap.Modal(document.getElementById('editLeadModal'));
            modal.show();
        })
        .catch(error => {
            console.log('Error fetching lead for edit:', error);
            showNotification('Error loading lead for editing', 'error');
        });
}

// Populate Edit Form
function populateEditForm(lead) {
    const form = document.getElementById('editLeadForm');
    if (!form) return;
    
    form.querySelector('#editName').value = lead.name;
    form.querySelector('#editPhone').value = lead.phone;
    form.querySelector('#editEmail').value = lead.email;
    form.querySelector('#editStatus').value = lead.status;
    form.querySelector('#editScore').value = lead.score;
    form.querySelector('#editNotes').value = lead.notes || '';
    
    form.dataset.leadId = lead.id;
}

// Delete Lead
function deleteLead(leadId) {
    if (confirm('Are you sure you want to delete this lead?')) {
        fetch(`/api/leads/${leadId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove row from table
                const row = document.querySelector(`[data-lead-id="${leadId}"]`).closest('tr');
                row.remove();
                
                showNotification('Lead deleted successfully', 'success');
                updateLeadStatistics();
            } else {
                showNotification('Error deleting lead', 'error');
            }
        })
        .catch(error => {
            console.log('Error deleting lead:', error);
            showNotification('Error deleting lead', 'error');
        });
    }
}

// Handle Bulk Actions
function handleBulkAction(action) {
    const selectedLeads = getSelectedLeads();
    
    if (selectedLeads.length === 0) {
        showNotification('No leads selected', 'warning');
        return;
    }
    
    switch(action) {
        case 'export':
            exportSelectedLeads(selectedLeads);
            break;
        case 'delete':
            deleteSelectedLeads(selectedLeads);
            break;
        case 'assign':
            assignSelectedLeads(selectedLeads);
            break;
        case 'tag':
            tagSelectedLeads(selectedLeads);
            break;
        default:
            console.log('Unknown bulk action:', action);
    }
    
    // Reset bulk action selector
    document.getElementById('bulkActions').value = '';
}

// Get Selected Leads
function getSelectedLeads() {
    const checkboxes = document.querySelectorAll('#leadsTable tbody input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(checkbox => {
        const row = checkbox.closest('tr');
        return row.querySelector('[data-action="view-lead"]').dataset.leadId;
    });
}

// Export Selected Leads
function exportSelectedLeads(leadIds) {
    fetch('/api/leads/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ leadIds })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'selected_leads_export.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showNotification('Selected leads exported successfully', 'success');
    })
    .catch(error => {
        console.log('Error exporting leads:', error);
        showNotification('Error exporting leads', 'error');
    });
}

// Delete Selected Leads
function deleteSelectedLeads(leadIds) {
    if (confirm(`Are you sure you want to delete ${leadIds.length} leads?`)) {
        fetch('/api/leads/bulk-delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ leadIds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove rows from table
                leadIds.forEach(leadId => {
                    const row = document.querySelector(`[data-lead-id="${leadId}"]`)?.closest('tr');
                    if (row) row.remove();
                });
                
                showNotification(`${leadIds.length} leads deleted successfully`, 'success');
                updateLeadStatistics();
            } else {
                showNotification('Error deleting leads', 'error');
            }
        })
        .catch(error => {
            console.log('Error deleting leads:', error);
            showNotification('Error deleting leads', 'error');
        });
    }
}

// Assign Selected Leads
function assignSelectedLeads(leadIds) {
    // Show assignment modal
    const modal = new bootstrap.Modal(document.getElementById('assignLeadsModal'));
    modal.show();
    
    // Store lead IDs for later use
    document.getElementById('assignLeadsForm').dataset.leadIds = JSON.stringify(leadIds);
}

// Tag Selected Leads
function tagSelectedLeads(leadIds) {
    // Show tagging modal
    const modal = new bootstrap.Modal(document.getElementById('tagLeadsModal'));
    modal.show();
    
    // Store lead IDs for later use
    document.getElementById('tagLeadsForm').dataset.leadIds = JSON.stringify(leadIds);
}

// Filter Leads
function filterLeads(filterType, filterValue) {
    const table = document.getElementById('leadsTable');
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        let showRow = true;
        
        switch(filterType) {
            case 'status':
                const statusCell = row.querySelector('td:nth-child(6)');
                showRow = !filterValue || statusCell.textContent.trim() === filterValue;
                break;
            case 'score':
                const scoreCell = row.querySelector('td:nth-child(4)');
                const score = parseFloat(scoreCell.textContent);
                showRow = evaluateScoreFilter(score, filterValue);
                break;
            case 'source':
                const sourceCell = row.querySelector('td:nth-child(5)');
                showRow = !filterValue || sourceCell.textContent.trim() === filterValue;
                break;
            case 'dateRange':
                const dateCell = row.querySelector('td:nth-child(7)');
                showRow = evaluateDateFilter(dateCell.textContent, filterValue);
                break;
        }
        
        row.style.display = showRow ? '' : 'none';
    });
}

// Evaluate Score Filter
function evaluateScoreFilter(score, filter) {
    switch(filter) {
        case 'high': return score >= 8;
        case 'medium': return score >= 5 && score < 8;
        case 'low': return score < 5;
        default: return true;
    }
}

// Evaluate Date Filter
function evaluateDateFilter(dateString, filter) {
    const date = new Date(dateString);
    const today = new Date();
    
    switch(filter) {
        case 'today':
            return date.toDateString() === today.toDateString();
        case 'week':
            const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
            return date >= weekAgo;
        case 'month':
            const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);
            return date >= monthAgo;
        default:
            return true;
    }
}

// Search Leads
function searchLeads(searchTerm) {
    const table = document.getElementById('leadsTable');
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

// Setup Lead Updates
function setupLeadUpdates() {
    // Simulate real-time lead updates
    const eventSource = new EventSource('/api/lead-updates');
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleLeadUpdate(data);
    };
    
    eventSource.onerror = function() {
        console.log('Lead updates connection lost');
        // Fallback to polling
        setInterval(pollLeadUpdates, 30000);
    };
}

// Handle Lead Update
function handleLeadUpdate(data) {
    switch(data.type) {
        case 'new_lead':
            addNewLeadRow(data.lead);
            showNotification(`New lead: ${data.lead.name}`, 'success');
            updateLeadStatistics();
            break;
        case 'lead_updated':
            updateLeadRow(data.lead);
            showNotification(`Lead updated: ${data.lead.name}`, 'info');
            break;
        case 'lead_deleted':
            removeLeadRow(data.leadId);
            showNotification('Lead deleted', 'info');
            updateLeadStatistics();
            break;
    }
}

// Add New Lead Row
function addNewLeadRow(lead) {
    const table = document.getElementById('leadsTable').querySelector('tbody');
    const row = createLeadRow(lead);
    table.insertBefore(row, table.firstChild);
    
    // Add fade-in animation
    row.classList.add('fade-in');
}

// Create Lead Row
function createLeadRow(lead) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td><input type="checkbox" class="form-check-input"></td>
        <td>
            <div class="d-flex align-items-center">
                <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center me-2" style="width: 40px; height: 40px;">
                    ${getInitials(lead.name)}
                </div>
                <div>
                    <strong>${lead.name}</strong>
                    <br><small class="text-muted">${lead.requirements || 'No requirements'}</small>
                </div>
            </div>
        </td>
        <td>
            <div>
                <i class="fas fa-phone me-1"></i> ${lead.phone}
                <br>
                <i class="fas fa-envelope me-1"></i> ${lead.email}
            </div>
        </td>
        <td>
            <span class="badge bg-${getScoreColor(lead.score)}">${lead.score}</span>
            <br><small class="text-muted">${getScoreLabel(lead.score)}</small>
        </td>
        <td>
            <span class="badge bg-primary">${lead.source}</span>
        </td>
        <td>
            <span class="badge bg-${getStatusColor(lead.status)}">${lead.status}</span>
        </td>
        <td>${formatDate(lead.date)}</td>
        <td>
            <div class="btn-group" role="group">
                <button class="btn btn-sm btn-outline-primary" data-action="view-lead" data-lead-id="${lead.id}">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" data-action="contact-lead" data-lead-id="${lead.id}" data-lead-phone="${lead.phone}">
                    <i class="fas fa-phone"></i>
                </button>
                <button class="btn btn-sm btn-outline-info" data-action="edit-lead" data-lead-id="${lead.id}">
                    <i class="fas fa-edit"></i>
                </button>
            </div>
        </td>
    `;
    return row;
}

// Update Lead Row
function updateLeadRow(lead) {
    const row = document.querySelector(`[data-lead-id="${lead.id}"]`)?.closest('tr');
    if (row) {
        const newRow = createLeadRow(lead);
        row.replaceWith(newRow);
    }
}

// Remove Lead Row
function removeLeadRow(leadId) {
    const row = document.querySelector(`[data-lead-id="${leadId}"]`)?.closest('tr');
    if (row) {
        row.remove();
    }
}

// Update Lead Statistics
function updateLeadStatistics() {
    // Update statistics cards
    const totalLeads = document.querySelectorAll('#leadsTable tbody tr').length;
    const newLeads = document.querySelectorAll('#leadsTable tbody .badge.bg-success').length;
    const inProgressLeads = document.querySelectorAll('#leadsTable tbody .badge.bg-warning').length;
    const convertedLeads = document.querySelectorAll('#leadsTable tbody .badge.bg-info').length;
    
    updateStatCard('total-leads-stat', totalLeads);
    updateStatCard('new-leads-stat', newLeads);
    updateStatCard('in-progress-stat', inProgressLeads);
    updateStatCard('converted-stat', convertedLeads);
}

// Update Stat Card
function updateStatCard(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        const current = parseInt(element.textContent);
        animateValue(element, current, value, 500);
    }
}

// Utility Functions
function getInitials(name) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

function getScoreColor(score) {
    if (score >= 8) return 'success';
    if (score >= 5) return 'warning';
    return 'danger';
}

function getScoreLabel(score) {
    if (score >= 8) return 'High Intent';
    if (score >= 5) return 'Warm';
    return 'Cold';
}

function getStatusColor(status) {
    const colors = {
        'New': 'success',
        'Contacted': 'secondary',
        'In Progress': 'warning',
        'Qualified': 'info',
        'Converted': 'primary'
    };
    return colors[status] || 'secondary';
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('id-ID');
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('id-ID');
}

function logLeadActivity(leadId, description) {
    fetch('/api/leads/activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            leadId: leadId,
            description: description,
            timestamp: new Date().toISOString()
        })
    });
}

function updateBulkActionsVisibility() {
    const selectedCount = document.querySelectorAll('#leadsTable tbody input[type="checkbox"]:checked').length;
    const bulkActions = document.getElementById('bulkActions');
    if (bulkActions) {
        bulkActions.disabled = selectedCount === 0;
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Export leads functions
window.Leads = {
    showLeadDetails,
    contactLead,
    editLead,
    deleteLead,
    filterLeads,
    searchLeads,
    exportSelectedLeads,
    showNotification
};
