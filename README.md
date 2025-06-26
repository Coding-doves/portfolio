---

# 📸 My Portfolio API

This is a backend portfolio API built with **FastAPI** for a photographer and videographer. It powers a personal portfolio site, showcasing projects, testimonials, skills, education, and blog posts.

---

## 🛠️ Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **Alembic**
- **Pydantic**
- **Uvicorn**
- **Docker** 
- **Render** (for deployment)

---

## 📁 Directory Structure

```
app/
├── app_tools/
│   ├── routers/           # API endpoints
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── core/              # DB config, auth, utils
│   ├── dependencies/      # Shared helper functions
├── media/                 # Uploaded files (images, videos)
├── main.py                # FastAPI app entrypoint
````

---

## 🔧 Setup

### 1. Clone the repo

```
git clone https://github.com/Coding-doves/portfolio.git
cd portfolio
```

### 2. Create a virtual environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file and add:

```
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
```

### 5. Run migrations

```
alembic upgrade head
```

### 6. Start the server

```
uvicorn main:app --reload
```

Visit the docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📬 Contact

For collaboration, contact me at **[obenedicta4@gmail.com](mailto:obenedicta4@gmail.com)**.

---

```
**[frontend repo](...)**
**[Backend repo](...)**
```
