# Quick Start Guide

Get your MIND Dashboard running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Database (2 minutes)

Edit `.streamlit/secrets.toml`:

```toml
[database]
host = "ep-cool-frog-12345678.us-east-2.aws.neon.tech"  # ← Your Neon host
database = "mind_database"                               # ← Your database name
user = "neondb_owner"                                    # ← Your username  
password = "npg_abc123xyz"                              # ← Your password
port = 5432
sslmode = "require"
```

**Where to find these:**
1. Go to your [Neon Console](https://console.neon.tech)
2. Select your project
3. Click "Connection Details"
4. Copy the values

## Step 3: Run the Dashboard (30 seconds)

```bash
streamlit run Home.py
```

The dashboard opens at: **http://localhost:8501**

## Step 4: Login (30 seconds)

Use these credentials:

**Admin:**
- Email: `admin@example.com`
- Password: `admin123`

## ✅ You're Done!

Navigate using the sidebar to explore different dashboards.

---

## 🐛 Not Working?

### "Unable to connect to database"
- Double-check your credentials in `secrets.toml`
- Ensure your Neon database is running
- Verify you're using the correct project

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Port 8501 already in use"
```bash
streamlit run Home.py --server.port 8502
```

---

## 📚 Next Steps

1. Read the full [README.md](README.md)
2. Explore each dashboard
3. Customize colors in `theme.py`
4. Add your logo to `assets/mind_logo.png`

---

Need help? Check the README or create an issue!
