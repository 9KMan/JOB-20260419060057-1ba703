# Specification: Music/Booking SaaS — Finish & Launch

## 1. Project Overview

**Project:** Music/Booking SaaS — Finish & Launch
**Type:** Full-stack SaaS (B2B / marketplace-adjacent)
**Core Functionality:** Booking and scheduling platform for music industry — managing venue bookings, performer scheduling, AI-driven automation for booking workflows, and communication
**Target Users:** Music venues, booking agents, performers, and event managers
**Current Status:** ~70% built. Existing codebase needs completion, stabilization, and launch.

---

## 2. Technical Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js (App Router), React 18, TypeScript, Tailwind CSS |
| **Backend** | Node.js (Express or similar) |
| **Database** | PostgreSQL (confirm with client) |
| **Auth** | NextAuth.js or similar (role-based: admin, performer, venue) |
| **AI** | OpenAI API + Claude API for LLM features (parsing, automation, summaries) |
| **Scheduling** | Custom calendar engine or Cal.com API integration |
| **Email** | SendGrid or Resend for transactional + notification emails |
| **Deployment** | Vercel (frontend) + Railway/Render (backend) |

---

## 3. Core Features to Complete

### 3.1 User Authentication & Authorization
- Sign-up, login, email verification
- Role-based access: admin, venue manager, performer, booking agent
- JWT session management (httpOnly cookies)
- Password reset flow

### 3.2 Booking Management
- Create, approve, reject, and manage booking requests
- Calendar view for availability (performer and venue)
- Conflict detection for double-booking
- Status tracking: pending → approved → rejected → completed → cancelled
- Booking notes and internal comments
- Attachments support (contract uploads, rider documents)

### 3.3 Scheduling System
- Time slot management (blocked times, available times)
- Calendar integration: display bookings on calendar view
- Conflict alerts when scheduling overlapping events
- Automated reminder notifications (email/SMS) before events
- Recurring booking support (weekly/monthly slots)

### 3.4 AI Features (LLM Integration)
- **Booking Inquiry Parser:** Parse natural language booking requests into structured data (extract date, venue, performer, budget)
- **Automated Routing:** Route booking requests to correct venue/performer based on genre, location, availability
- **Auto-Confirmation Workflow:** AI-generated confirmation messages; auto-reply to booking inquiries
- **Availability Suggestions:** AI suggests optimal time slots based on historical booking patterns
- **Conflict Alerts:** AI-generated alerts for scheduling conflicts, availability gaps
- **Summary Reports:** AI-generated daily/weekly booking summaries for admins

### 3.5 Communication Workflow
- In-app messaging between venues and performers
- Notification system for booking status updates
- Email notifications via SendGrid/Resend
- Status change webhook notifications (Phase 2)

### 3.6 Payment Integration (Phase 2 — post-launch)
- Stripe for booking deposits
- Invoice generation
- Payment status tracking

---

## 4. Existing Codebase Assessment Required

Before building, OpenCode agent MUST:
1. Read and understand all existing code in the repository
2. Identify: which features from the spec are already built, partially built, or missing
3. Identify: tech stack decisions already made (ORM, auth library, component patterns)
4. Create a gap analysis: what remains → this becomes the build spec

**Gap analysis is mandatory before writing new code.**

---

## 5. Data Model (Draft — confirm with existing codebase)

```
Users:         id, email, password_hash, name, role (ENUM: admin, venue, performer, agent), phone, created_at
Venues:        id, name, address, capacity, genre_focus, contact_email, created_at
Performers:    id, user_id, name, genre, bio, availability_notes, created_at
Bookings:      id, venue_id, performer_id, requested_date, start_time, end_time, status (ENUM: pending, approved, rejected, completed, cancelled), notes, created_at, updated_at
Messages:      id, booking_id, sender_id, body, sent_at
Notifications: id, user_id, type, message, read (BOOLEAN), created_at
```

---

## 6. File Structure (Standard Next.js Full-Stack)

```
music-booking-saas/
├── SPEC.md
├── README.md
├── package.json
├── tsconfig.json
├── .env.example
├── prisma/
│   └── schema.prisma              # or existing schema
├── src/
│   ├── app/
│   │   ├── (auth)/               # auth routes (login, register, reset)
│   │   ├── (dashboard)/          # protected routes
│   │   │   ├── bookings/          # booking management
│   │   │   ├── calendar/          # calendar/scheduling view
│   │   │   ├── performers/        # performer profiles
│   │   │   ├── venues/            # venue management
│   │   │   └── admin/            # admin analytics
│   │   └── api/
│   │       ├── auth/
│   │       ├── bookings/
│   │       ├── calendar/
│   │       ├── ai/               # OpenAI/Claude endpoints
│   │       └── webhooks/
│   ├── components/
│   │   ├── ui/                   # shadcn/ui primitives
│   │   ├── booking/              # booking-specific components
│   │   └── calendar/             # calendar components
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── db.ts                 # Prisma client
│   │   ├── openai.ts             # OpenAI client
│   │   └── claude.ts             # Claude client
│   └── services/
│       ├── bookingService.ts
│       ├── aiService.ts
│       └── notificationService.ts
└── tests/
    ├── booking.test.ts
    └── ai.test.ts
```

---

## 7. Out of Scope

- Mobile app (web only for MVP)
- Payment processing (Phase 2 post-launch)
- Social features / reviews
- Analytics dashboard (Phase 2)
- Multi-language support

---

## 8. Delivery Checklist

- [ ] GitHub repo assessed — gap analysis documented in README
- [ ] Missing features from spec completed
- [ ] AI features (LLM parsing, automation) functional
- [ ] Calendar/scheduling working without conflicts
- [ ] Auth + RBAC verified
- [ ] Email notifications working
- [ ] Production-ready deployment (Vercel + Railway)
- [ ] No hardcoded secrets
- [ ] README with setup + gap analysis documented
