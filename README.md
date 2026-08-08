# Blog App
 
A simple blog application with user authentication, authorization, and full CRUD functionality for blog posts. Users can register, log in, and create, read, update, and delete their own blog posts.
 
## Features
 
- **Authentication** — user registration and login using hashed passwords and JWT tokens
- **Authorization** — protected routes; only a post's author (or an admin) can update/delete it
- **CRUD** — create, read, update, and delete blog posts
- **Validation** — request validation on user and blog input
## Tech Stack
 
- **Framework:** Flask
- **Database:** PostgreSQL with SQLAlchemy (Flask-SQLAlchemy)
- **Migrations:** Flask-Migrate (Alembic)
- **Auth:** JSON Web Tokens (Flask-JWT-Extended) + Werkzeug/bcrypt for password hashing
## Data Schema
 
### User
 
| Field        | Type         | Required | Description                                  |
|--------------|--------------|----------|-----------------------------------------------|
| `id`         | Integer (PK) | auto     | Unique user identifier                        |
| `username`   | String       | Yes      | Unique display name                           |
| `email`      | String       | Yes      | Unique, used for login                        |
| `password`   | String       | Yes      | Hashed password (never returned in responses) |
| `role`       | String       | No       | `"user"` or `"admin"` (default: `"user"`)     |
| `avatar`     | String       | No       | URL to profile image                          |
| `bio`        | Text         | No       | Short user bio                                |
| `created_at` | DateTime     | auto     | Account creation timestamp                    |
| `updated_at` | DateTime     | auto     | Last update timestamp                         |
 
### Blog Post
 
| Field         | Type          | Required | Description                                        |
|---------------|---------------|----------|------------------------------------------------------|
| `id`          | Integer (PK)  | auto     | Unique post identifier                              |
| `author`      | Integer (FK)  | Yes      | References `users.id` — the post's creator          |
| `title`       | String        | Yes      | Post title                                           |
| `content`     | Text          | Yes      | Post body (markdown or HTML)                         |
| `tags`        | ARRAY(String) | No       | Categorization tags (Postgres array, or a join table)|
| `cover_image` | String        | No       | URL to a cover image                                 |
| `created_at`  | DateTime      | auto     | Creation timestamp                                   |
| `updated_at`  | DateTime      | auto     | Last update timestamp                                |
 
## API Routes
 
### Auth Routes (`/api/auth`)
 
| Method | Route         | Access  | Description                          |
|--------|---------------|---------|----------------------------------------|
| POST   | `/register`   | Public  | Create a new user account            |
| POST   | `/login`      | Public  | Log in, returns a JWT                |
| POST   | `/logout`     | Private | Invalidate current session/token     |
| GET    | `/me`         | Private | Get the logged-in user's profile     |
 
### User Routes (`/api/users`)
 
| Method | Route         | Access  | Description                          |
|--------|---------------|---------|----------------------------------------|
| GET    | `/<id>`       | Public  | Get a user's public profile          |
| PUT    | `/<id>`       | Private (owner) | Update own profile             |
| DELETE | `/<id>`       | Private (owner/admin) | Delete a user account    |
 
### Blog Routes (`/api/blogs`)
 
| Method | Route         | Access                  | Description                        |
|--------|---------------|--------------------------|-------------------------------------|
| GET    | `/`           | Public                  | Get all published blog posts (supports pagination/filters) |
| GET    | `/<id>`       | Public                  | Get a single blog post by ID        |
| POST   | `/`           | Private                 | Create a new blog post              |
| PUT    | `/<id>`       | Private (author only)   | Update an existing blog post        |
| DELETE | `/<id>`       | Private (author/admin)  | Delete a blog post                  |
| GET    | `/user/<user_id>` | Public              | Get all posts by a specific user    |
 
## Authorization Rules
 
- Routes marked **Private** require a valid JWT in the `Authorization: Bearer <token>` header.
- **Owner-only** routes verify that the requesting user's ID matches the resource's `author`/user ID (or that the user has an `admin` role).
- Passwords are hashed before storage and are never included in API responses.
## Environment Variables
 
Create a `.env` file in the project root:
 
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost:5432/blog_app
JWT_SECRET_KEY=your_jwt_secret
JWT_ACCESS_TOKEN_EXPIRES=604800
```
 
## Installation
 
```bash
# Clone the repo
git clone https://github.com/your-username/blog-app.git
cd blog-app
 
# Install dependencies (uv creates/manages the virtual environment for you)
uv sync
 
# Set up the database
uv run flask db upgrade
 
# Run in development
uv run flask run
```
 
## Project Structure
 
```
blog-app/
├── app/
│   ├── __init__.py      # App factory, extension setup
│   ├── models.py        # SQLAlchemy models (User, Blog)
│   ├── auth/             # Auth blueprint (register, login, logout, me)
│   │   └── routes.py
│   ├── users/             # User blueprint
│   │   └── routes.py
│   ├── blogs/             # Blog blueprint (CRUD)
│   │   └── routes.py
│   └── utils/             # Auth/authorization decorators, helpers
├── migrations/            # Alembic migration files (Flask-Migrate)
├── config.py               # Config classes (dev/prod/test)
├── .env
├── pyproject.toml
├── uv.lock
└── run.py
```
 
## License
 
MIT
 
