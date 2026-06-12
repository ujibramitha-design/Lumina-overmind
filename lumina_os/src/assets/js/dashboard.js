// Lumina OS Dashboard JavaScript - Property Intelligence System
// API Integration for Real-time Data

// Global state
let dashboardState = {
    stats: null,
    leads: [],
    analytics: null,
    loading: false,
    lastUpdate: null,
    charts: {
        trends: null,
        category: null
    }
};

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Lumina OS Dashboard initialized');
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Load initial data
    loadDashboardData();
    
    // Setup periodic updates
    setInterval(loadDashboardData, 30000); // Update every 30 seconds
});

// Load Dashboard Data
async function loadDashboardData() {
    if (dashboardState.loading) return;
    
    dashboardState.loading = true;
    showLoadingState();
    
    try {
        // Parallel API calls
        const [statsResponse, leadsResponse, analyticsResponse] = await Promise.all([
            fetchDashboardStats(),
            fetchLeadsData(),
            fetchAnalytics()
        ]);
        
        // Update UI with new data
        updateDashboardStats(statsResponse);
        updateLeadsTable(leadsResponse);
        updateAnalyticsCharts(analyticsResponse);
        
        dashboardState.lastUpdate = new Date();
        console.log('Dashboard data updated successfully');
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showErrorMessage('Failed to load dashboard data');
        
        // Fallback to mock data
        loadMockData();
    } finally {
        dashboardState.loading = false;
        hideLoadingState();
    }
}

// Fetch Dashboard Statistics
async function fetchDashboardStats() {
    try {
        const response = await fetch('/api/leads/stats');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Transform API response to dashboard format
        return {
            totalLeads: data.total_leads || 0,
            avgScore: data.avg_ai_score || 0,
            hotLeads: data.hot_leads || 0,
            conversionRate: data.conversion_rate || 0
        };
        
    } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        throw error;
    }
}

// Fetch Leads Data
async function fetchLeadsData() {
    try {
        const response = await fetch('/api/leads/recent');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Store leads in dashboard state for edit modal
        dashboardState.leads = data.data || [];
        
        // Return leads array or empty array
        return data.data || [];
        
    } catch (error) {
        console.error('Error fetching leads data:', error);
        return [];
    }
}

// Update Dashboard Statistics
function updateDashboardStats(stats) {
    if (!stats) return;
    
    // Update total leads with animation
    animateValue('total-leads', 0, stats.totalLeads, 2000);
    
    // Update average AI score
    animateValue('avg-score', 0, stats.avgScore, 2000, value => value.toFixed(1));
    
    // Update hot leads
    animateValue('hot-leads', 0, stats.hotLeads, 2000);
    
    // Update conversion rate
    animateValue('conversion-rate', 0, stats.conversionRate, 2000, value => value.toFixed(1) + '%');
    
    dashboardState.stats = stats;
}

// Update Leads Table
function updateLeadsTable(leads) {
    const tbody = document.getElementById('leads-table-body');
    if (!tbody) return;
    
    if (!leads || leads.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-8 text-center">
                    <div class="text-zinc-400">
                        <i data-lucide="inbox" class="w-8 h-8 mx-auto mb-2"></i>
                        <p>No leads data available</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = leads.map(lead => `
        <tr class="border-b border-zinc-800 hover:bg-zinc-900/50 transition-colors">
            <td class="px-6 py-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-zinc-800 rounded-full flex items-center justify-center">
                        <span class="text-xs text-white font-medium">${getInitials(lead.nama || 'Unknown')}</span>
                    </div>
                    <div>
                        <div class="text-white font-medium">${lead.nama || 'Unknown'}</div>
                        <div class="text-zinc-400 text-sm">${lead.email || 'No email'}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4">
                <div class="flex items-center space-x-2">
                    <div class="w-12 bg-zinc-800 rounded-full h-1.5">
                        <div class="h-1.5 rounded-full ${getScoreColor(lead.skor_akhir || 0)}" style="width: ${lead.skor_akhir || 0}%"></div>
                    </div>
                    <span class="text-white font-medium">${(lead.skor_akhir || 0).toFixed(1)}</span>
                </div>
            </td>
            <td class="px-6 py-4">
                ${getCategoryBadge(lead.kategori || 'Cold')}
            </td>
            <td class="px-6 py-4">
                ${getStatusBadge(lead.status || 'new')}
            </td>
            <td class="px-6 py-4">
                <div class="text-zinc-400 text-sm">${lead.sumber || 'Unknown'}</div>
            </td>
            <td class="px-6 py-4">
                <button onclick="viewLeadDetails('${lead.id || lead.nama}')" class="px-3 py-1 bg-white text-black rounded hover:bg-zinc-200 transition-colors text-sm font-medium">
                    View
                </button>
            </td>
        </tr>
    `).join('');
    
    // Re-initialize Lucide icons for new elements
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    dashboardState.leads = leads;
}

// Helper Functions

function getInitials(name) {
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

function getScoreColor(score) {
    if (score >= 80) return 'bg-emerald-500';
    if (score >= 60) return 'bg-amber-500';
    return 'bg-red-500';
}

function getCategoryBadge(category) {
    const colors = {
        'Hot': 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
        'Warm': 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
        'Cold': 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
    };
    
    const colorClass = colors[category] || colors['Cold'];
    return `<span class="px-2 py-1 rounded-full text-xs font-medium ${colorClass}">${category}</span>`;
}

function getStatusBadge(status) {
    const colors = {
        'new': 'bg-zinc-500/10 text-zinc-400 border border-zinc-500/20',
        'contacted': 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
        'qualified': 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
        'converted': 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
    };
    
    const colorClass = colors[status] || colors['new'];
    return `<span class="px-2 py-1 rounded-full text-xs font-medium ${colorClass}">${status}</span>`;
}

// Animation Functions

function animateValue(elementId, start, end, duration, formatter = null) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = formatter ? formatter(end) : end;
            clearInterval(timer);
        } else {
            element.textContent = formatter ? formatter(current) : Math.floor(current);
        }
    }, 16);
}

// Loading State Functions

function showLoadingState() {
    // Show loading skeleton for stats cards
    const statElements = ['total-leads', 'avg-score', 'hot-leads', 'conversion-rate'];
    statElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.className = 'skeleton bg-zinc-900 rounded-md h-8 w-20';
            element.textContent = '';
        }
    });
    
    // Show loading for leads table
    const tbody = document.getElementById('leads-table-body');
    if (tbody) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-8">
                    <div class="flex justify-center items-center space-y-4">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
                        <p class="text-zinc-400">Loading leads data...</p>
                    </div>
                </td>
            </tr>
        `;
    }
}

function hideLoadingState() {
    // Loading state will be hidden when data is populated
}

// Error Handling

function showErrorMessage(message) {
    console.error(message);
    
    // Show error notification (you can enhance this with a toast component)
    const errorDiv = document.createElement('div');
    errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Mock Data Fallback

function loadMockData() {
    const mockStats = {
        totalLeads: 1250,
        avgScore: 75.3,
        hotLeads: 320,
        conversionRate: 12.5
    };
    
    const mockLeads = [
        {
            id: 1,
            nama: 'John Doe',
            email: 'john@example.com',
            skor_akhir: 85.5,
            kategori: 'Hot',
            status: 'new',
            sumber: 'OLX'
        },
        {
            id: 2,
            nama: 'Jane Smith',
            email: 'jane@example.com',
            skor_akhir: 62.3,
            kategori: 'Warm',
            status: 'contacted',
            sumber: 'Facebook'
        },
        {
            id: 3,
            nama: 'Bob Johnson',
            email: 'bob@example.com',
            skor_akhir: 45.1,
            kategori: 'Cold',
            status: 'new',
            sumber: 'Google'
        }
    ];
    
    const mockAnalytics = {
        daily_trends: [
            { date: '2026-05-22', total_leads: 12, hot_leads: 3, warm_leads: 5, cold_leads: 4 },
            { date: '2026-05-23', total_leads: 15, hot_leads: 4, warm_leads: 6, cold_leads: 5 },
            { date: '2026-05-24', total_leads: 8, hot_leads: 2, warm_leads: 3, cold_leads: 3 },
            { date: '2026-05-25', total_leads: 18, hot_leads: 5, warm_leads: 7, cold_leads: 6 },
            { date: '2026-05-26', total_leads: 22, hot_leads: 6, warm_leads: 8, cold_leads: 8 },
            { date: '2026-05-27', total_leads: 14, hot_leads: 4, warm_leads: 5, cold_leads: 5 },
            { date: '2026-05-28', total_leads: 16, hot_leads: 5, warm_leads: 6, cold_leads: 5 }
        ],
        category_distribution: {
            labels: ['Hot (32%)', 'Warm (42%)', 'Cold (26%)'],
            data: [320, 420, 260],
            colors: ['#10b981', '#f59e0b', '#3b82f6']
        },
        conversion_forecast: {
            hot_leads_30d: 45,
            avg_score: 78.5,
            conversion_rate: 25.5,
            estimated_conversions: 11,
            forecast_revenue: 88000000
        }
    };
    
    updateDashboardStats(mockStats);
    updateLeadsTable(mockLeads);
    updateAnalyticsCharts(mockAnalytics);
}

// Analytics Functions

async function fetchAnalytics() {
    try {
        const response = await fetch('/api/analytics/summary');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            dashboardState.analytics = data.data;
            return data.data;
        } else {
            throw new Error(data.error || 'Failed to fetch analytics');
        }
        
    } catch (error) {
        console.error('Error fetching analytics:', error);
        return null;
    }
}

function updateAnalyticsCharts(analyticsData) {
    if (!analyticsData) {
        console.warn('No analytics data available');
        return;
    }
    
    // Update last updated timestamp
    const lastUpdated = new Date(analyticsData.performance_metrics?.last_updated || new Date());
    document.getElementById('last-updated').textContent = lastUpdated.toLocaleString();
    
    // Initialize or update charts
    initializeTrendsChart(analyticsData.daily_trends);
    initializeCategoryChart(analyticsData.category_distribution);
    updateConversionForecast(analyticsData.conversion_forecast);
    
    // Update summary statistics
    updateAnalyticsSummary(analyticsData);
}

function initializeTrendsChart(trendsData) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (dashboardState.charts.trends) {
        dashboardState.charts.trends.destroy();
    }
    
    // Prepare data
    const labels = trendsData.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('id-ID', { weekday: 'short', day: 'numeric' });
    });
    
    const totalLeads = trendsData.map(item => item.total_leads);
    const hotLeads = trendsData.map(item => item.hot_leads);
    
    // Create new chart
    dashboardState.charts.trends = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Total Leads',
                    data: totalLeads,
                    borderColor: '#14b8a6',
                    backgroundColor: 'rgba(20, 184, 166, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Hot Leads',
                    data: hotLeads,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#9ca3af',
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#9ca3af',
                    borderColor: '#374151',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(55, 65, 81, 0.3)',
                        borderColor: '#374151'
                    },
                    ticks: {
                        color: '#9ca3af'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(55, 65, 81, 0.3)',
                        borderColor: '#374151'
                    },
                    ticks: {
                        color: '#9ca3af'
                    },
                    beginAtZero: true
                }
            }
        }
    });
    
    // Update summary
    const totalTrends = totalLeads.reduce((sum, val) => sum + val, 0);
    const avgTrends = (totalTrends / trendsData.length).toFixed(1);
    document.getElementById('total-trends').textContent = totalTrends;
    document.getElementById('avg-trends').textContent = avgTrends;
}

function initializeCategoryChart(categoryData) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (dashboardState.charts.category) {
        dashboardState.charts.category.destroy();
    }
    
    // Create new chart
    dashboardState.charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categoryData.labels,
            datasets: [{
                data: categoryData.data,
                backgroundColor: categoryData.colors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#9ca3af',
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#9ca3af',
                    borderColor: '#374151',
                    borderWidth: 1
                }
            }
        }
    });
    
    // Update summary
    const hotPercentage = categoryData.labels.find(label => label.includes('Hot'))?.match(/\((\d+)%\)/)?.[1] || '0';
    const conversionPotential = hotPercentage > 30 ? 'High' : hotPercentage > 20 ? 'Medium' : 'Low';
    document.getElementById('hot-percentage').textContent = hotPercentage + '%';
    document.getElementById('conversion-potential').textContent = conversionPotential;
}

function updateConversionForecast(forecastData) {
    document.getElementById('hot-leads-30d').textContent = forecastData.hot_leads_30d || 0;
    document.getElementById('conversion-rate-forecast').textContent = (forecastData.conversion_rate || 0) + '%';
    document.getElementById('estimated-conversions').textContent = forecastData.estimated_conversions || 0;
    
    // Format revenue
    const revenue = forecastData.forecast_revenue || 0;
    const formattedRevenue = revenue >= 1000000 
        ? 'Rp ' + (revenue / 1000000).toFixed(1) + 'M'
        : 'Rp ' + revenue.toLocaleString('id-ID');
    document.getElementById('forecast-revenue').textContent = formattedRevenue;
}

function updateAnalyticsSummary(analyticsData) {
    // Update top cards with analytics data
    const metrics = analyticsData.performance_metrics;
    
    if (metrics) {
        document.getElementById('total-leads').textContent = metrics.total_leads.toLocaleString();
        document.getElementById('hot-leads').textContent = metrics.by_status?.['New'] || 0;
        document.getElementById('conversion-rate').textContent = metrics.followup_rate + '%';
        
        // Calculate average score (mock for now)
        const avgScore = 75.3; // This would come from actual analytics
        document.getElementById('avg-score').textContent = avgScore.toFixed(1);
    }
}

// Edit Modal Functions

function openEditModal(leadId) {
    // Get lead data from current dashboard state
    const lead = dashboardState.leads.find(l => l.id === leadId);
    
    if (!lead) {
        console.error('Lead not found:', leadId);
        return;
    }
    
    // Populate form fields
    document.getElementById('editLeadId').value = lead.id;
    document.getElementById('editName').value = lead.nama || '';
    document.getElementById('editEmail').value = lead.email || '';
    document.getElementById('editScore').value = lead.skor_akhir || 0;
    document.getElementById('editCategory').value = lead.kategori || 'Cold';
    document.getElementById('editStatus').value = lead.status || 'New';
    document.getElementById('editSource').value = lead.sumber || '';
    document.getElementById('editNotes').value = lead.catatan || '';
    
    // Show modal
    document.getElementById('editModal').classList.remove('hidden');
    
    // Re-initialize Lucide icons in modal
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
    document.getElementById('editLeadForm').reset();
}

function saveLeadChanges() {
    const leadId = document.getElementById('editLeadId').value;
    
    const leadData = {
        id: leadId,
        nama: document.getElementById('editName').value,
        email: document.getElementById('editEmail').value,
        skor_akhir: parseFloat(document.getElementById('editScore').value),
        kategori: document.getElementById('editCategory').value,
        status: document.getElementById('editStatus').value,
        sumber: document.getElementById('editSource').value,
        catatan: document.getElementById('editNotes').value
    };
    
    // Send update request
    fetch(`/api/leads/update/${leadId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(leadData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showSuccessMessage('Lead data updated successfully!');
            
            // Close modal
            closeEditModal();
            
            // Refresh dashboard data
            loadDashboardData();
        } else {
            showErrorMessage('Failed to update lead: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error updating lead:', error);
        showErrorMessage('Error updating lead. Please try again.');
    });
}

function showSuccessMessage(message) {
    // Create success toast
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center space-x-2';
    toast.innerHTML = `
        <i data-lucide="check-circle" class="w-5 h-5"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function showErrorMessage(message) {
    // Create error toast
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center space-x-2';
    toast.innerHTML = `
        <i data-lucide="alert-circle" class="w-5 h-5"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Re-initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Update leads table with edit buttons
function updateLeadsTable(leads) {
    const tableBody = document.getElementById('leads-table-body');
    const noLeadsMessage = document.getElementById('no-leads-message');
    tableBody.innerHTML = ''; // Clear existing rows
    
    if (leads && leads.length > 0) {
        noLeadsMessage.style.display = 'none';
        leads.forEach(lead => {
            const row = tableBody.insertRow();
            row.className = 'border-b border-zinc-800 last:border-0 hover:bg-zinc-900 transition-colors';
            
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-white">${lead.nama}</td>
                <td class="px-6 py-4 whitespace-nowrap text-zinc-400">${lead.skor_akhir.toFixed(1)}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 rounded-full text-xs font-medium ${getCategoryClass(lead.kategori)}">
                        ${lead.kategori}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-zinc-400">${lead.status}</td>
                <td class="px-6 py-4 whitespace-nowrap text-zinc-400">${lead.sumber}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onclick="openEditModal(${lead.id})" class="text-amber-500 hover:text-amber-400 mr-3">
                        <i data-lucide="edit" class="w-4 h-4"></i>
                    </button>
                    <button onclick="viewLeadDetails(${lead.id})" class="text-teal-500 hover:text-teal-400">
                        <i data-lucide="eye" class="w-4 h-4"></i>
                    </button>
                </td>
            `;
        });
        
        // Re-initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } else {
        noLeadsMessage.style.display = 'block';
    }
}

// Interactive Functions

function viewLeadDetails(leadId) {
    console.log('Viewing lead details for:', leadId);
    // Implement lead details modal or navigation
    alert(`Lead details for: ${leadId}`);
}

function refreshDashboard() {
    console.log('Refreshing dashboard...');
    loadDashboardData();
}

// Export Functions for Global Access

window.LuminaDashboard = {
    refresh: refreshDashboard,
    getState: () => dashboardState,
    viewLead: viewLeadDetails
};
