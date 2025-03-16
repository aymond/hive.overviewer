// Custom JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    // Add 'active' class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
    
    // Set current year in footer
    const yearSpan = document.querySelector('.current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });

    // Game Server Status Check
    const checkStatusBtn = document.querySelector('.check-status-btn');
    if (checkStatusBtn) {
        checkStatusBtn.addEventListener('click', async function() {
            const serverId = this.dataset.serverId || this.dataset.hostId;  // Try server ID first, then host ID
            const isHost = this.dataset.hostId !== undefined;
            const endpoint = isHost ? `/hosts/${serverId}/check` : `/servers/${serverId}/check`;
            const originalText = this.innerHTML;
            
            // Show loading state
            this.disabled = true;
            this.innerHTML = '<i class="bi bi-arrow-repeat"></i> Checking...';
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Update status indicator
                    const statusIndicator = document.querySelector('.status-indicator');
                    if (statusIndicator) {
                        statusIndicator.className = `status-indicator status-${data.status}`;
                    }
                    
                    // Update status badge
                    const statusBadge = document.querySelector('.badge');
                    if (statusBadge) {
                        statusBadge.className = `badge bg-${data.status === 'running' ? 'success' : data.status === 'stopped' ? 'danger' : 'warning'}`;
                        statusBadge.textContent = data.status;
                    }
                    
                    // Update status message and data
                    const statusMessageContainer = document.querySelector('.mt-3');
                    if (data.status_message) {
                        if (!statusMessageContainer) {
                            const newContainer = document.createElement('div');
                            newContainer.className = 'mt-3';
                            document.querySelector('.card-body').appendChild(newContainer);
                        }
                        
                        const container = statusMessageContainer || document.querySelector('.mt-3');
                        container.innerHTML = `
                            <strong>Status Message:</strong>
                            <p class="mb-1">${data.status_message}</p>
                            ${data.status_data ? `
                                <div class="status-data">
                                    <strong>Status Details:</strong>
                                    <dl class="row mb-0">
                                        ${data.status_data.players !== undefined ? `
                                            <dt class="col-sm-4">Players Online:</dt>
                                            <dd class="col-sm-8">${data.status_data.players}/${data.status_data.max_players}</dd>
                                        ` : ''}
                                        ${data.status_data.version ? `
                                            <dt class="col-sm-4">Version:</dt>
                                            <dd class="col-sm-8">${data.status_data.version}</dd>
                                        ` : ''}
                                        ${data.status_data.description ? `
                                            <dt class="col-sm-4">Description:</dt>
                                            <dd class="col-sm-8">${data.status_data.description}</dd>
                                        ` : ''}
                                    </dl>
                                </div>
                            ` : ''}
                        `;
                    } else if (statusMessageContainer) {
                        statusMessageContainer.remove();
                    }
                    
                    // Show success message
                    showAlert('success', 'Status checked successfully');
                    
                    // Refresh the page if it's a host status check
                    if (isHost) {
                        location.reload();
                    }
                } else {
                    showAlert('danger', data.message || 'Failed to check status');
                }
            } catch (error) {
                showAlert('danger', 'An error occurred while checking status');
                console.error('Error:', error);
            } finally {
                // Restore button state
                this.disabled = false;
                this.innerHTML = originalText;
            }
        });
    }
});

// Show alert message
function showAlert(type, message) {
    const alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alert);
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
} 