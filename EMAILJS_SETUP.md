# EmailJS Setup Guide for BookMySeat

This guide will help you set up EmailJS to send booking confirmation emails to users after successful ticket bookings.

## Prerequisites

1. An EmailJS account (free at [emailjs.com](https://www.emailjs.com/))
2. A Gmail account (or other supported email service)

## Step 1: Create EmailJS Account

1. Go to [emailjs.com](https://www.emailjs.com/) and sign up for a free account
2. Verify your email address

## Step 2: Add Email Service

1. In your EmailJS dashboard, go to **Email Services**
2. Click **Add New Service**
3. Choose **Gmail** (or your preferred email provider)
4. Follow the setup instructions to connect your email account
5. Note down your **Service ID** (e.g., `service_xxxxxxx`)

## Step 3: Create Email Template

1. Go to **Email Templates** in your EmailJS dashboard
2. Click **Create New Template**
3. Use the following template for booking confirmations:

### Template Content

**Subject:** Booking Confirmation - {{movie_name}} / {{event_name}}

**Body:**
```
Dear {{to_name}},

Thank you for booking with BookMySeat!

BOOKING DETAILS:
================

{% if movie_name %}
Movie: {{movie_name}}
Theater: {{theater_name}}
Show Time: {{show_time}}
Seats: {{seat_numbers}}
{% endif %}

{% if event_name %}
Event: {{event_name}}
Date: {{event_date}}
Time: {{event_time}}
Venue: {{venue}}
Seats: {{seat_numbers}}
Total Amount: ₹{{total_amount}}
{% endif %}

Booking ID: {{booking_id}}
Booking Date: {{booking_date}}

IMPORTANT REMINDERS:
===================
- Please arrive 15 minutes before the show/event starts
- Bring a valid ID for verification
- Keep this email as your booking confirmation

Thank you for choosing BookMySeat!

Best regards,
The BookMySeat Team
```

4. Save the template and note down your **Template ID** (e.g., `template_xxxxxxx`)

## Step 4: Get Public Key

1. Go to **Account** → **General** in your EmailJS dashboard
2. Find your **Public Key** (e.g., `user_xxxxxxxxxxxxxxxx`)

## Step 5: Update Configuration

1. Open `static/js/emailjs-config.js`
2. Replace the placeholder values with your actual EmailJS credentials:

```javascript
const EMAILJS_CONFIG = {
    serviceId: 'service_your_service_id_here',        // Replace with your Service ID
    templateId: 'template_your_template_id_here',    // Replace with your Template ID
    publicKey: 'your_public_key_here'                // Replace with your Public Key
};
```

## Step 6: Test the Setup

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to your booking page and complete a test booking

3. Check if the confirmation email is sent successfully

## Troubleshooting

### Common Issues:

1. **"EmailJS is not defined" error**
   - Make sure the EmailJS SDK is loaded before your configuration script
   - Check browser console for any script loading errors

2. **"Service not found" error**
   - Verify your Service ID is correct
   - Ensure the service is active in your EmailJS dashboard

3. **"Template not found" error**
   - Verify your Template ID is correct
   - Ensure the template is published in your EmailJS dashboard

4. **"Invalid public key" error**
   - Double-check your Public Key
   - Make sure there are no extra spaces or characters

5. **Emails not being sent**
   - Check your email service connection in EmailJS dashboard
   - Verify your email account permissions
   - Check spam folder for test emails

### Testing Tips:

1. Use a real email address for testing
2. Check both inbox and spam folders
3. Test with different booking scenarios (movies vs events)
4. Verify all template variables are populated correctly

## Security Notes

- Never commit your actual EmailJS credentials to version control
- Consider using environment variables for production deployments
- The current setup uses client-side email sending, which is suitable for this use case
- For high-volume applications, consider server-side email solutions

## Production Considerations

1. **Rate Limiting**: EmailJS has rate limits on free accounts
2. **Monitoring**: Set up email delivery monitoring
3. **Backup**: Consider having a backup email service
4. **Analytics**: Track email open rates and delivery success

## Support

- EmailJS Documentation: [https://www.emailjs.com/docs/](https://www.emailjs.com/docs/)
- EmailJS Support: [https://www.emailjs.com/support/](https://www.emailjs.com/support/)

---

**Note**: This implementation automatically sends confirmation emails after successful bookings. Users will see a success message and can also manually trigger email sending if needed.
