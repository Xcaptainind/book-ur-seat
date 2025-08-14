# 🎬 Book Ur Seat - Movie Booking System

A comprehensive Django-based movie booking system with advanced features including payment gateways, seat reservations, and admin analytics.

## ✨ Features

### 🎭 Core Features
- **Movie Management**: Add, edit, and manage movies with detailed information
- **Theater Management**: Multiple theaters with different show timings
- **Seat Booking**: Interactive seat selection with real-time availability
- **User Authentication**: Secure user registration and login system

### 🔍 Enhanced Features
1. **Genre and Language Filters**
   - Filter movies by genre (Action, Comedy, Drama, Horror, etc.)
   - Filter by language (Hindi, English, Tamil, Telugu, etc.)
   - Search functionality for movie titles and descriptions

2. **Ticket Email Confirmation**
   - Automated email confirmations after successful bookings
   - HTML and plain text email templates
   - Reminder emails for upcoming shows

3. **Movie Trailers**
   - YouTube trailer integration for each movie
   - Embedded video players on movie detail pages

4. **Payment Gateway Integration**
   - **Stripe**: Credit/Debit card payments
   - **Razorpay**: UPI, Net Banking, and wallet payments
   - Secure payment processing with webhook verification
   - Success/failure handling

5. **Seat Reservation Timeout**
   - Temporary seat reservations (5 minutes)
   - Automatic seat release after timeout
   - Background task processing with Celery

6. **Admin Dashboard with Analytics**
   - Revenue analytics and reporting
   - Popular movies and theater performance
   - User behavior analytics
   - Seat utilization metrics
   - Interactive charts and graphs

## 🛠️ Technology Stack

- **Backend**: Django 3.2.19
- **Database**: SQLite (development) / PostgreSQL (production)
- **Payment**: Stripe + Razorpay
- **Background Tasks**: Celery + Redis
- **Email**: SMTP (Gmail)
- **Frontend**: Bootstrap 5 + Chart.js
- **Forms**: Django Crispy Forms

## 📋 Prerequisites

- Python 3.8+
- pip
- Redis (for Celery)
- Stripe and Razorpay accounts (for payments)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-ur-seat
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the project root:
   ```env
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # Email Configuration
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Stripe Configuration
   STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-key
   STRIPE_SECRET_KEY=sk_test_your-stripe-secret
   STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
   
   # Razorpay Configuration
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-secret-key
   RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Redis Server**
   ```bash
   # On Windows (using WSL or Docker)
   redis-server
   
   # On macOS
   brew services start redis
   
   # On Linux
   sudo systemctl start redis
   ```

8. **Start Celery Worker**
   ```bash
   celery -A book_ur_seat worker --loglevel=info
   ```

9. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Payment Gateways

#### Stripe
1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from the dashboard
3. Set up webhook endpoint: `https://yourdomain.com/webhook/stripe/`
4. Add webhook secret to environment variables

#### Razorpay
1. Create a Razorpay account at [razorpay.com](https://razorpay.com)
2. Get your API keys from the dashboard
3. Set up webhook endpoint: `https://yourdomain.com/webhook/razorpay/`
4. Add webhook secret to environment variables

### Email Configuration
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Update environment variables with your email and app password

## 📱 Usage

### For Users
1. **Browse Movies**: View available movies with filters
2. **Select Theater**: Choose from available theaters and show times
3. **Select Seats**: Interactive seat selection interface
4. **Make Payment**: Choose payment method and complete transaction
5. **Get Confirmation**: Receive email confirmation with booking details

### For Administrators
1. **Dashboard**: Access analytics at `/admin/dashboard/`
2. **Revenue Reports**: Detailed financial reports at `/admin/revenue-report/`
3. **User Analytics**: User behavior insights at `/admin/user-analytics/`
4. **Django Admin**: Full CRUD operations at `/admin/`

## 🔒 Security Features

- CSRF protection on all forms
- Secure payment processing
- User authentication and authorization
- Admin-only access to sensitive data
- Webhook signature verification

## 📊 Admin Analytics

The admin dashboard provides:
- **Revenue Metrics**: Total and monthly revenue
- **Booking Analytics**: Total, completed, and pending bookings
- **Popular Content**: Most booked movies and performing theaters
- **User Insights**: Active users and engagement metrics
- **Seat Utilization**: Real-time seat occupancy statistics
- **Interactive Charts**: Revenue trends and genre distribution

## 🚨 Troubleshooting

### Common Issues

1. **Celery not working**
   - Ensure Redis is running
   - Check Celery worker is started
   - Verify Redis connection in settings

2. **Payment failures**
   - Check API keys in environment variables
   - Verify webhook endpoints are accessible
   - Check payment gateway dashboard for errors

3. **Email not sending**
   - Verify SMTP credentials
   - Check Gmail app password is correct
   - Ensure 2FA is enabled on Gmail

4. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database connection settings
   - Verify models are properly defined

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Updates

### Version 2.0 Features Added:
- ✅ Genre and Language filtering
- ✅ Email confirmation system
- ✅ YouTube trailer integration
- ✅ Stripe and Razorpay payment gateways
- ✅ Seat reservation timeout system
- ✅ Comprehensive admin dashboard
- ✅ Background task processing
- ✅ Enhanced user experience

---

**Made with ❤️ for movie lovers everywhere!**
