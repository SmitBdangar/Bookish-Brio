# 📚 Bookish Brio

**Bookish Brio** is a modern, community-driven web application built with Django that empowers writers and readers to share stories, connect, and engage in meaningful conversations. With a clean, intuitive interface and robust features, it provides the perfect platform for creative expression and literary community building.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)

---

## ✨ Features

### 🔐 User Authentication & Management
- **Secure User Registration** - Create accounts with username, email, and password
- **Login/Logout System** - Protected authentication with session management
- **User Profiles** - Personalized profile pages displaying user information and activity
- **Password Validation** - Real-time password strength checking during registration
- **Form Validation** - Client-side and server-side validation for all user inputs

### 📝 Post Management
- **Create Posts** - Rich post creation with titles, content, and optional images
- **Cover Images** - Upload featured images for posts (single cover image)
- **Image Gallery** - Attach multiple gallery images (up to 8) to each post
- **Post Preview** - Automatic content truncation with "Read more" links
- **Full Post View** - Dedicated detail pages for reading complete posts
- **Delete Posts** - Authors can remove their own posts with confirmation
- **Drag & Drop Upload** - Intuitive image upload with preview functionality
- **Character Counter** - Real-time character count while composing

### 💬 Engagement Features
- **Like System** - Toggle likes on posts with visual feedback
- **Like Counter** - Display total likes for each post
- **Commenting** - Add comments to any post
- **Comment Management** - Delete your own comments
- **Comment Counter** - Track total comments per post
- **Author Identification** - Visual indicators for post authors
- **Engagement Metrics** - View likes and comments at a glance

### 🎨 User Interface & Experience
- **Modern Design** - Clean, professional interface with Inter font family
- **Responsive Layout** - Fully mobile-responsive design (desktop, tablet, mobile)
- **Color Scheme** - Vibrant orange primary color (#ff6b35) with elegant accents
- **Image Modal** - Click to view full-size images in modal overlay
- **Smooth Animations** - Transition effects and hover states throughout
- **Interactive Elements** - Dynamic dropdowns, buttons, and form controls
- **Loading States** - Visual feedback during form submissions
- **Empty States** - Helpful messages when no content is available

### 📱 Responsive Pages

#### Home Page (`index.html`)
- Paginated post feed
- Welcome banner for new visitors
- Post cards with previews
- Like and comment buttons
- Author and timestamp information
- Sidebar with trending topics and community stats

#### Post Detail Page (`post_detail.html`)
- Full post content display
- Featured image and gallery
- Complete engagement section
- Comment thread
- Add comment form (authenticated users)
- Author action menu (edit/delete)

#### Create Post Page (`add_post.html`)
- Rich text input for content
- Title input field
- Multiple image upload (up to 8)
- Drag-and-drop support
- Image preview with removal option
- Writing tips sidebar
- Community stats card
- Character counter

#### Profile Page (`profile.html`)
- User avatar with initials
- Account information display
- Member since badge
- Activity statistics (post count, active time)
- Recent posts list (5 most recent)
- Quick action buttons
- Account details grid

#### Authentication Pages
- **Login** (`login.html`) - Clean login form with features list
- **Signup** (`signup.html`) - Registration with real-time validation

### 🔧 Technical Features
- **Django 5.2** - Latest Django framework
- **SQLite Database** - Default development database
- **WhiteNoise** - Static file serving in production
- **Gunicorn** - Production WSGI server
- **Django Forms** - ModelForms for post and comment creation
- **Class-Based Views** - Efficient view handling
- **CSRF Protection** - Security tokens on all forms
- **Pagination** - Efficient content loading
- **Timezone Support** - UTC timezone handling
- **Message Framework** - Success/error notifications
- **Static Files Management** - Organized CSS, JS, and images

### 🛡️ Security Features
- **CSRF Protection** - Cross-Site Request Forgery prevention
- **Password Validation** - Django's built-in validators
- **Authentication Required** - Protected views for authenticated actions
- **Author Verification** - Users can only delete their own content
- **Secure Cookies** - Session and CSRF cookie security
- **XSS Protection** - Django template auto-escaping
- **SQL Injection Protection** - ORM query parameterization

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bookish-brio.git
   cd bookish-brio
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   # Create .env file
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open browser to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 📁 Project Structure

```
Bookish-Brio/
│
├── Brio/                      # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── home/                      # Main application
│   ├── models.py             # Post, Comment, PostImage models
│   ├── views.py              # View functions
│   ├── forms.py              # PostForm, CommentForm
│   ├── urls.py               # App URL patterns
│   ├── admin.py              # Admin configuration
│   │
│   ├── templates/home/       # HTML templates
│   │   ├── index.html        # Home page
│   │   ├── post_detail.html  # Post detail page
│   │   ├── add_post.html     # Create post page
│   │   ├── profile.html      # User profile page
│   │   ├── login.html        # Login page
│   │   └── signup.html       # Registration page
│   │
│   ├── static/               # Static files
│   │   └── img/              # Images (favicon, etc.)
│   │
│   └── migrations/           # Database migrations
│
├── staticfiles/              # Collected static files
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── runtime.txt               # Python version for deployment
├── Procfile                  # Production server configuration
└── README.md                 # This file

---

## 🗄️ Database Models

### Post Model
- `title` - Post title (CharField, max 200)
- `content` - Post content (TextField)
- `image` - Featured image (ImageField, optional)
- `author` - Foreign key to User
- `likes` - Many-to-many with User
- `created_at` - Timestamp (auto)

### Comment Model
- `post` - Foreign key to Post
- `author` - Foreign key to User
- `content` - Comment text (TextField)
- `created_at` - Timestamp (auto)

### PostImage Model
- `post` - Foreign key to Post
- `image` - Gallery image (ImageField)
- `created_at` - Timestamp (auto)

---

## 🚢 Deployment

### Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Set environment variables**
   - `DJANGO_SECRET_KEY`
   - `DEBUG=False`
   - Add your Railway domain to `ALLOWED_HOSTS`

### Environment Variables
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.railway.app,yourdomain.com
```

---

## 🛠️ Technologies Used

### Backend
- **Django 5.2** - Web framework
- **Python 3.13** - Programming language
- **SQLite** - Database (development)
- **Gunicorn** - WSGI HTTP server
- **WhiteNoise** - Static file serving

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling (custom, no frameworks)
- **JavaScript** - Interactivity
- **Font Awesome 6** - Icons
- **Google Fonts** - Inter font family

### Development
- **Django Debug Toolbar** - Debugging (optional)
- **Git** - Version control
- **Railway** - Deployment platform

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

---

## 🔮 Roadmap

### Planned Features
- [ ] User profile editing
- [ ] Follow/unfollow users
- [ ] Post categories and tags
- [ ] Search functionality
- [ ] Rich text editor
- [ ] Email notifications
- [ ] Social sharing buttons
- [ ] Reading time estimates
- [ ] Bookmarking posts
- [ ] Dark mode toggle
- [ ] User avatars upload
- [ ] Advanced post filtering
- [ ] API endpoints (REST/GraphQL)

---

## 📊 Project Statistics

- **Total Files**: 20+
- **Lines of Code**: 3000+
- **Templates**: 6 pages
- **Models**: 3 (Post, Comment, PostImage)
- **Views**: 10+ functions
- **URL Patterns**: 12 routes

---

<div align="center">

[⬆ Back to Top](#-bookish-brio)

</div>
