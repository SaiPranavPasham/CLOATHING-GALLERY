# CLOATHING-GALLERY

CLOATHING-GALLERY is a Django-based fashion gallery web app where users can create an account, upload outfit photos, organize favorite looks, and maintain a personal wishlist. The project is designed as a simple personal fashion dashboard with a modern UI and an interactive image carousel.

## Features

- User registration and login
- Personal dashboard for each user
- Upload outfit images with title and description
- Mark uploaded outfits as favorites
- Delete outfits from the gallery
- Create and manage a wishlist with product links, notes, and optional images
- Responsive interface for desktop and mobile
- Custom gallery carousel for showcasing uploaded looks

## Tech Stack

- Python
- Django 5
- SQLite
- HTML
- CSS
- JavaScript
- Pillow

## Project Structure

- `accounts/`  
  Handles models, views, authentication, and user-related features.

- `templates/`  
  Contains the frontend HTML files such as login, register, dashboard, favorites, wishlist, and upload pages.

- `dashboard_project/`  
  Main Django project configuration including settings and URLs.

- `media/`  
  Stores uploaded user images.

## Main Modules

### Authentication
Users can:
- Register with username, email, and password
- Log in with credentials
- Log out securely

### Outfit Gallery
Users can:
- Upload outfit photos
- Add titles and descriptions
- View their personal gallery
- Mark outfits as favorites
- Delete outfits

### Wishlist
Users can:
- Save wishlist items
- Add product links
- Add notes
- Upload an optional image for the wishlist item

## Database Models

### Outfit
Stores:
- user
- title
- description
- image
- favorite status
- created date

### WishlistItem
Stores:
- user
- title
- product link
- notes
- image
- created date

## Local Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Run migrations
5. Start the local server

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
