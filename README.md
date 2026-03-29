# SattvaFlow - AI-Powered Yoga Training Platform

A full-stack yoga management platform where Admin, Trainers, and Clients interact in a secure, privacy-focused environment.

## Features

### Authentication
- Google Based Authentication

### User Roles
- **Admin**: Full system control, manage trainers, clients, assignments, reviews, and queries
- **Trainer**: Manage assigned clients, create sessions and plans, track progress
- **Client**: View assigned trainer, access sessions and plans, submit queries and reviews

### Key Features
- WhatsApp and Email notifications
- Query management system
- Review system with admin moderation
- Session scheduling
- Yoga plan management
- Progress tracking
- Privacy-first design (users only see their own data)

## Tech Stack

### Backend
- Flask (Python)
- MongoDB
- JWT Authentication
- Twilio (WhatsApp API)
- SMTP (Email)

### Frontend
- Vue.js 3
- Vue Router
- Pinia (State Management)
- Vite

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- Twilio Account (for WhatsApp)
- SMTP Email Account

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
pip install -r requirements.txt
cd frontend
npm install vite
npm install





API Endpoints
Authentication
POST /api/auth/send-otp - Send OTP to WhatsApp/Email

POST /api/auth/verify-otp - Verify OTP and login

GET /api/auth/me - Get current user

Admin
GET /api/admin/trainers - Get all trainers

PUT /api/admin/trainers/:id/approve - Approve trainer

PUT /api/admin/trainers/:id/reject - Reject trainer

GET /api/admin/clients - Get all clients

POST /api/admin/assignments - Assign client to trainer

GET /api/admin/queries - Get all queries

POST /api/admin/queries/:id/respond - Respond to query

GET /api/admin/reviews - Get all reviews

GET /api/admin/stats - Get platform statistics

Trainer
GET /api/trainer/clients - Get assigned clients

GET /api/trainer/sessions - Get sessions

POST /api/trainer/sessions - Create session

GET /api/trainer/plans - Get plans

POST /api/trainer/plans - Create plan

PUT /api/trainer/plans/:id/progress - Update plan progress

GET /api/trainer/reviews - Get trainer reviews

Client
GET /api/client/trainer - Get assigned trainer

GET /api/client/sessions - Get sessions

GET /api/client/plans - Get plans

GET /api/client/queries - Get queries

POST /api/client/queries - Create query

GET /api/client/reviews - Get reviews

POST /api/client/reviews - Create review

Notifications
GET /api/notifications - Get notifications

PUT /api/notifications/:id/read - Mark notification read

PUT /api/notifications/read-all - Mark all read

Public
GET /api/public/trainers - Get featured trainers

GET /api/public/reviews - Get public reviews