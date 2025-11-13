<h1 align="center">Bookish Brio</h1>

<p align="center">
A clean, modern blogging platform for writers and readers to share stories and connect.
</p>

<p align="center">
  <img src="mDEAL/home.png" width="700" alt="Home Page">
</p>

<h1 align="center">Features</h1>
<div align="center">

- **Create & Share**: Write posts with rich text and images  
- **Engage**: Like posts and comment on stories  
- **Connect**: Build a community of writers and readers  
- **User Profiles**: Track your posts and activity  

</div>

<h1 align="center">Create Posts</h1>

<p align="center">
Write and publish your stories with an intuitive editor. Add images to make your posts more engaging.
</p>


<p align="center">
  <img src="mDEAL/CreatePost.png" width="700" alt="Create Post">
</p>

<h1 align="center">User Profile</h1>
<p align="center">
View your posts, track your activity, and manage your account in one place.
</p>

<p align="center">
  <img src="mDEAL/Profile.png" width="700" alt="User Profile">
</p>

<h1 align="center">Tech Stack</h1>
<div align="center">
- Django 5.2.6
- SQLite database
- Whitenoise for static files
- Gunicorn for deployment
</div>
<h1 align="center">Quick Start</h1>

```bash
git clone https://github.com/SmitBdangar/Bookish-Brio.git
cd Bookish-Brio

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
