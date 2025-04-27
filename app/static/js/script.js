// Toast notification system
document.addEventListener('DOMContentLoaded', function() {
    window.showToast = function(message, type = 'info', duration = 5000) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container fixed bottom-4 right-4 z-50';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toast = document.createElement('div');
        toast.setAttribute('x-data', '{ show: true }');
        toast.setAttribute('x-show', 'show');
        toast.setAttribute('x-init', `setTimeout(() => show = false, ${duration})`);
        
        // Set toast styling based on type
        let bgColor, textColor, borderColor, iconSvg;
        switch(type) {
            case 'success':
                bgColor = 'bg-green-50';
                textColor = 'text-green-800';
                borderColor = 'border-green-100';
                iconSvg = '<svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>';
                break;
            case 'error':
                bgColor = 'bg-red-50';
                textColor = 'text-red-800';
                borderColor = 'border-red-100';
                iconSvg = '<svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" /></svg>';
                break;
            case 'warning':
                bgColor = 'bg-yellow-50';
                textColor = 'text-yellow-800';
                borderColor = 'border-yellow-100';
                iconSvg = '<svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>';
                break;
            default:
                bgColor = 'bg-blue-50';
                textColor = 'text-blue-800';
                borderColor = 'border-blue-100';
                iconSvg = '<svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>';
        }
        
        // Set toast HTML
        toast.className = `mb-2 p-4 rounded-md shadow-md ${bgColor} ${textColor} border ${borderColor} transform transition-all duration-300 ease-in-out`;
        toast.innerHTML = `
            <div class="flex">
                <div class="flex-shrink-0">
                    ${iconSvg}
                </div>
                <div class="ml-3">
                    <p class="text-sm">${message}</p>
                </div>
                <div class="ml-auto pl-3">
                    <div class="-mx-1.5 -my-1.5">
                        <button @click="show = false" class="inline-flex rounded-md p-1.5 ${textColor} hover:${bgColor} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-${type === 'success' ? 'green' : type === 'error' ? 'red' : type === 'warning' ? 'yellow' : 'blue'}-500">
                            <span class="sr-only">Dismiss</span>
                            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add to container
        toastContainer.appendChild(toast);
        
        // Initialize Alpine on the new element
        if (window.Alpine) {
            window.Alpine.initTree(toast);
        }
        
        // Remove toast after animation completes
        setTimeout(() => {
            toast.addEventListener('x-collapse:after', () => {
                toast.remove();
            });
        }, duration);
    };

    // Helper functions for common toast types
    window.showSuccessToast = (message, duration = 5000) => window.showToast(message, 'success', duration);
    window.showErrorToast = (message, duration = 5000) => window.showToast(message, 'error', duration);
    window.showWarningToast = (message, duration = 5000) => window.showToast(message, 'warning', duration);
    window.showInfoToast = (message, duration = 5000) => window.showToast(message, 'info', duration);

    // Check for toast headers - this handles toast notifications after redirects or API responses
    const checkToastHeaders = () => {
        // Check for meta tags with toast information
        const message = document.head.querySelector('meta[name="x-toast-message"]')?.getAttribute('content');
        const type = document.head.querySelector('meta[name="x-toast-type"]')?.getAttribute('content') || 'info';
        const duration = document.head.querySelector('meta[name="x-toast-duration"]')?.getAttribute('content') || 5000;

        if (message) {
            window.showToast(message, type, parseInt(duration, 10));
        }
    };

    // Initialize AJAX handlers for toast headers
    const initAjaxToastHandler = () => {
        // Store the original fetch function
        const originalFetch = window.fetch;
        
        // Override the fetch function
        window.fetch = async function(...args) {
            // Call the original fetch function
            const response = await originalFetch(...args);
            
            // Check for toast headers in the response
            const toastMessage = response.headers.get('X-Toast-Message');
            if (toastMessage) {
                const toastType = response.headers.get('X-Toast-Type') || 'info';
                const toastDuration = response.headers.get('X-Toast-Duration') || 5000;
                
                // Show the toast
                window.showToast(toastMessage, toastType, parseInt(toastDuration, 10));
            }
            
            // Return the original response
            return response;
        };

        // Handle XMLHttpRequest for libraries that don't use fetch
        const originalXhrOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function() {
            const xhr = this;
            const originalOnReadyStateChange = xhr.onreadystatechange;
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    const toastMessage = xhr.getResponseHeader('X-Toast-Message');
                    if (toastMessage) {
                        const toastType = xhr.getResponseHeader('X-Toast-Type') || 'info';
                        const toastDuration = xhr.getResponseHeader('X-Toast-Duration') || 5000;
                        
                        // Show the toast
                        window.showToast(toastMessage, toastType, parseInt(toastDuration, 10));
                    }
                }
                
                if (originalOnReadyStateChange) {
                    originalOnReadyStateChange.apply(this, arguments);
                }
            };
            
            originalXhrOpen.apply(this, arguments);
        };
    };

    // Check for toast headers on page load
    checkToastHeaders();
    
    // Initialize AJAX handlers
    initAjaxToastHandler();
});

// Score Resume modal functions
function scoreResume(resumeId) {
    // Set the current resume ID to score
    window.currentResumeId = resumeId;
    
    // Reset the job description field and hide any previous results
    document.getElementById('job-description').value = '';
    
    // Show the modal
    Alpine.store('app').showScoreModal = true;
}

function cancelScoreModal() {
    Alpine.store('app').showScoreModal = false;
    window.currentResumeId = null;
}

async function submitScoreResume() {
    const jobDescription = document.getElementById('job-description').value.trim();
    
    if (!jobDescription) {
        window.showWarningToast('Please enter a job description to score your resume against.');
        return;
    }
    
    if (!window.currentResumeId) {
        window.showErrorToast('No resume selected. Please try again.');
        return;
    }
    
    try {
        // Show loading state
        Alpine.store('app').isScoring = true;
        
        // Call the API to score the resume
        const response = await fetch(`/api/resume/${window.currentResumeId}/score`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_description: jobDescription
            })
        });
        
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        
        // Parse the response
        const result = await response.json();
        
        // Update the score results in Alpine store
        Alpine.store('app').scoreResults = {
            ats_score: result.ats_score,
            matching_skills: result.matching_skills || [],
            missing_skills: result.missing_skills || [],
            recommendation: result.recommendation || 'No specific recommendations available.'
        };
        
        // Hide score modal and show results modal
        Alpine.store('app').showScoreModal = false;
        Alpine.store('app').showScoreResultsModal = true;
        
    } catch (error) {
        console.error('Error scoring resume:', error);
        window.showErrorToast('There was a problem scoring your resume. Please try again.');
    } finally {
        Alpine.store('app').isScoring = false;
    }
}

function closeScoreResultsModal() {
    Alpine.store('app').showScoreResultsModal = false;
    window.currentResumeId = null;
}

function optimizeResumeFromScore() {
    if (!window.currentResumeId) {
        window.showErrorToast('Resume ID not found. Please try again.');
        return;
    }
    
    // Close the current modal
    Alpine.store('app').showScoreResultsModal = false;
    
    // Redirect to the optimize page with the resume ID
    window.location.href = `/resume/${window.currentResumeId}/optimize`;
}

// Add Alpine store for managing global state
document.addEventListener('alpine:init', () => {
    Alpine.store('app', {
        // Score modal state
        showScoreModal: false,
        isScoring: false,
        
        // Score results modal state
        showScoreResultsModal: false,
        scoreResults: {
            ats_score: 0,
            matching_skills: [],
            missing_skills: [],
            recommendation: ''
        }
    });
});
