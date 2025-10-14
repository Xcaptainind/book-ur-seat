// EmailJS Configuration
(function() {
    'use strict';
    
    // EmailJS configuration
    const EMAILJS_CONFIG = {
        serviceId: 'service_gku54f1', // Replace with your EmailJS service ID
        templateId: 'template_i3r6xzw', // Replace with your EmailJS template ID
        publicKey: 'BuezkjGJDvI4_J-LO' // Replace with your EmailJS public key
    };
    
    // Initialize EmailJS
    emailjs.init(EMAILJS_CONFIG.publicKey);
    
    // Email service object
    window.EmailService = {
        /**
         * Send booking confirmation email for movie tickets
         * @param {Object} bookingData - Booking information
         */
        sendMovieBookingConfirmation: function(bookingData) {
            const templateParams = {
                to_email: bookingData.userEmail,
                to_name: bookingData.userName,
                movie_name: bookingData.movieName,
                theater_name: bookingData.theaterName,
                show_time: bookingData.showTime,
                seat_numbers: bookingData.seatNumbers,
                booking_date: bookingData.bookingDate,
                booking_id: bookingData.bookingId,
                total_amount: bookingData.totalAmount || 'N/A'
            };
            
            // Debug logging
            console.log('Sending movie booking email with params:', templateParams);
            console.log('Using service ID:', EMAILJS_CONFIG.serviceId);
            console.log('Using template ID:', EMAILJS_CONFIG.templateId);
            
            return emailjs.send(
                EMAILJS_CONFIG.serviceId,
                EMAILJS_CONFIG.templateId,
                templateParams
            ).catch(function(error) {
                console.error('EmailJS Error Details:', error);
                console.error('Error Status:', error.status);
                console.error('Error Text:', error.text);
                throw error;
            });
        },
        
        /**
         * Send booking confirmation email for event tickets
         * @param {Object} bookingData - Event booking information
         */
        sendEventBookingConfirmation: function(bookingData) {
            const templateParams = {
                to_email: bookingData.userEmail,
                to_name: bookingData.userName,
                event_name: bookingData.eventName,
                event_date: bookingData.eventDate,
                event_time: bookingData.eventTime,
                venue: bookingData.venue,
                seat_numbers: bookingData.seatNumbers,
                booking_date: bookingData.bookingDate,
                booking_id: bookingData.bookingId,
                total_amount: bookingData.totalAmount
            };
            
            // Debug logging
            console.log('Sending event booking email with params:', templateParams);
            console.log('Using service ID:', EMAILJS_CONFIG.serviceId);
            console.log('Using template ID:', EMAILJS_CONFIG.templateId);
            
            return emailjs.send(
                EMAILJS_CONFIG.serviceId,
                EMAILJS_CONFIG.templateId,
                templateParams
            ).catch(function(error) {
                console.error('EmailJS Error Details:', error);
                console.error('Error Status:', error.status);
                console.error('Error Text:', error.text);
                throw error;
            });
        },
        
        /**
         * Show success/error messages
         * @param {boolean} success - Whether the email was sent successfully
         * @param {string} message - Message to display
         */
        showMessage: function(success, message) {
            const alertClass = success ? 'alert-success' : 'alert-danger';
            const icon = success ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
            
            const alertHtml = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    <i class="${icon} me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            
            // Insert alert at the top of the content
            const container = document.querySelector('.container');
            if (container) {
                container.insertAdjacentHTML('afterbegin', alertHtml);
                
                // Auto-dismiss after 5 seconds
                setTimeout(() => {
                    const alert = container.querySelector('.alert');
                    if (alert) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 5000);
            }
        }
    };
    
    // Utility function to format date
    window.formatDate = function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    
    // Utility function to format currency
    window.formatCurrency = function(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    };
    
})();
