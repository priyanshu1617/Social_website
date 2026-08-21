# Bookmarks - Django Social Website

A fully-featured image bookmarking social platform built with Django.

## Features

- **Authentication System**: Custom login, registration, and password management along with Google OAuth2 integration.
- **User Profiles & Following**: Users can follow/unfollow each other and view follower counts and profiles.
- **Image Bookmarking (Bookmarklet)**: A custom JavaScript bookmarklet that users can drag to their browser toolbar to scrape and save images from any website directly into the platform.
- **Activity Stream**: A dynamic activity feed tracking user actions (likes, follows, bookmarks) powered by Django's Generic Relations.
- **Redis Caching**: Tracks image view counts and drives a "Top Images" ranking system, backed by Redis for high performance.
- **AJAX Interactions**: Seamless asynchronous likes, follows, and infinite scrolling on image feeds using vanilla JavaScript `fetch`.

## UI/UX Design

The platform features a modern, custom design system built from scratch without bulky CSS frameworks:
- Built with **Inter** typography and CSS custom properties for a consistent, premium feel.
- Fully responsive CSS Grid and Flexbox layouts.
- **Dynamic Dashboard**: Features a 2-column layout highlighting recent bookmarks in a beautiful image grid alongside a compact activity feed.
- **Polished Interactions**: Slide-in flash messages, subtle image zoom hover effects, CSS-styled file uploads, and smooth animated state toggles for like/follow buttons.
- Clean text-only interfaces for maximum professional aesthetic.

## Tech Stack

- **Backend**: Django
- **Database**: SQLite (default), Redis (for caching and rankings)
- **Frontend**: HTML5, Vanilla JavaScript, Custom CSS3
- **Libraries**: `social-auth-app-django`, `easy-thumbnails`

## How to Run Locally

1. Activate your virtual environment and install dependencies.
2. Ensure you have **Redis** running locally on port 6379.
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Navigate to `http://127.0.0.1:8000/` in your browser.
