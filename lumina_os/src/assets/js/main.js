// HUNTER_AGENT_AI_MARKETING_DIGITAL Main JavaScript

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('HUNTER_AGENT_AI Marketing Digital System Initialized');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-refresh dashboard data
    if (document.getElementById('dashboard')) {
        setInterval(refreshDashboardData, 30000); // Refresh every 30 seconds
    }
    
    // Initialize real-time updates
    initializeRealTimeUpdates();
});

// Dashboard data refresh
function refreshDashboardData() {
    // Simulate data refresh
    const elements = {
        'total-leads': Math.floor(Math.random() * 100) + 1200,
        'conversion-rate': (Math.random() * 2 + 11).toFixed(1),
        'roi': Math.floor(Math.random() * 50) + 300,
        'satisfaction': (Math.random() * 0.5 + 4.2).toFixed(1)
    };
    
    Object.keys(elements).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            animateValue(element, parseInt(element.textContent), elements[id], 1000);
        }
    });
}

// Animate number changes
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(function() {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Real-time updates
function initializeRealTimeUpdates() {
    // Simulate WebSocket connection for real-time updates
    const eventSource = new EventSource('/api/real-time-updates');
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleRealTimeUpdate(data);
    };
    
    eventSource.onerror = function(event) {
        console.log('Real-time connection error, falling back to polling');
        // Fallback to polling
        setInterval(pollForUpdates, 5000);
    };
}

// Handle real-time updates
function handleRealTimeUpdate(data) {
    switch(data.type) {
        case 'new_lead':
            showNotification('New lead detected!', 'success');
            updateLeadCount(data.count);
            break;
        case 'conversion':
            showNotification('Lead converted!', 'success');
            updateConversionRate(data.rate);
            break;
        case 'system_alert':
            showNotification(data.message, 'warning');
            break;
        default:
            console.log('Unknown update type:', data.type);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Update lead count
function updateLeadCount(count) {
    const element = document.getElementById('total-leads');
    if (element) {
        animateValue(element, parseInt(element.textContent), count, 1000);
    }
}

// Update conversion rate
function updateConversionRate(rate) {
    const element = document.getElementById('conversion-rate');
    if (element) {
        element.textContent = rate + '%';
    }
}

// Polling fallback for real-time updates
function pollForUpdates() {
    fetch('/api/get-updates')
        .then(response => response.json())
        .then(data => {
            data.forEach(update => handleRealTimeUpdate(update));
        })
        .catch(error => {
            console.log('Polling error:', error);
        });
}

// Export data functionality
function exportData(format = 'csv') {
    const data = collectTableData();
    
    if (format === 'csv') {
        downloadCSV(data, 'leads_export.csv');
    } else if (format === 'json') {
        downloadJSON(data, 'leads_export.json');
    } else if (format === 'excel') {
        // Would need a library like SheetJS for Excel export
        showNotification('Excel export coming soon!', 'info');
    }
}

// Collect table data
function collectTableData() {
    const table = document.getElementById('leadsTable');
    if (!table) return [];
    
    const rows = table.querySelectorAll('tbody tr');
    const data = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const rowData = {
            name: cells[1].textContent.trim(),
            contact: cells[2].textContent.trim(),
            score: cells[3].textContent.trim(),
            source: cells[4].textContent.trim(),
            status: cells[5].textContent.trim(),
            date: cells[6].textContent.trim()
        };
        data.push(rowData);
    });
    
    return data;
}

// Download CSV
function downloadCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Convert data to CSV
function convertToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = data.map(row => {
        return headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        }).join(',');
    });
    
    return csvHeaders + '\n' + csvRows.join('\n');
}

// Download JSON
function downloadJSON(data, filename) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Filter functionality
function filterTable(searchTerm) {
    const table = document.getElementById('leadsTable');
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matches = text.includes(searchTerm.toLowerCase());
        row.style.display = matches ? '' : 'none';
    });
}

// Search input handler
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            filterTable(e.target.value);
        });
    }
});

// Print functionality
function printTable() {
    const table = document.getElementById('leadsTable');
    if (!table) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Leads Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <h1>Leads Report</h1>
                <p>Generated: ${new Date().toLocaleString()}</p>
                ${table.outerHTML}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + E for export
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportData();
    }
    
    // Ctrl/Cmd + P for print
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault();
        printTable();
    }
    
    // Ctrl/Cmd + F for search (override default)
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Theme toggle (if implemented)
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('id-ID').format(new Date(date));
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

// Export functions for use in other scripts
window.HunterAgent = {
    exportData,
    filterTable,
    printTable,
    showNotification,
    refreshDashboardData,
    formatCurrency,
    formatDate,
    debounce
};
