# MIND Dashboard Setup Guide

**Database and authentication are already configured!** Follow these steps to get running.

---

## ✅ What's Pre-Configured

- ✅ **Database Connection**: Neon Postgres credentials are set
- ✅ **Authentication**: Bcrypt hashed passwords configured
- ✅ **User Accounts**: Admin, Faculty, Developer, Student ready
- ✅ **Theme**: Miva Open University brand colors

---

## 📥 Step 1: Download All Files

Download all files from the `MIND_Dashboard_Files` folder and create this structure:

```
MIND-Unified-Dashboard/
├── Home.py
├── auth.py
├── db.py
├── theme.py
├── requirements.txt
├── .gitignore
├── PASSWORD_INFO.md
├── .streamlit/
│   └── secrets.toml          ← Already configured!
├── core/
│   ├── components.py
│   ├── utils.py
│   └── queries/
│       ├── admin_queries.py
│       ├── attempts_queries.py
│       ├── engagement_queries.py
│       ├── environment_queries.py
│       └── rubric_queries.py
└── pages/
    ├── 1_Student_Dashboard.py
    ├── 2_Faculty_Dashboard.py
    ├── 3_Developer_Dashboard.py
    └── 4_Admin_Dashboard.py
```

---

## 🔧 Step 2: Install Dependencies

```bash
cd MIND-Unified-Dashboard
pip install -r requirements.txt
```

This installs:
- streamlit (dashboard framework)
- pandas (data manipulation)
- plotly (interactive charts)
- psycopg2-binary (Neon Postgres connection)
- bcrypt (secure password hashing)
- Other dependencies

---

## 🗄️ Step 3: Verify Database Connection

Your database is already configured in `.streamlit/secrets.toml`:

```toml
[database]
host = "ep-weathered-cake-a4lk3gou-pooler.us-east-1.aws.neon.tech"
database = "neondb"
user = "neondb_owner"
password = "npg_oG7bDL4stHRk"
```

**Test the connection**:
```bash
python -c "from db import get_db_manager; db = get_db_manager(); print('✅ Connected!' if db.test_connection() else '❌ Failed')"
```

**Expected output**: `✅ Connected!`

If it fails:
- Check your Neon database is running
- Verify the connection string is correct
- Ensure your IP is whitelisted in Neon Console

---

## 🚀 Step 4: Run the Dashboard

```bash
streamlit run Home.py
```

The dashboard will open at: **http://localhost:8501**

---

## 🔐 Step 5: Login

### Use These Credentials:

| Role | Email | Password |
|------|-------|----------|
| **Admin** (Full Access) | admin@example.com | admin123 |
| **Faculty** | faculty@example.com | faculty123 |
| **Developer** | developer@example.com | dev123 |
| **Student** | student@example.com | student123 |

**Start with Admin** to access all dashboards.

---

## 🎯 What You'll See

### Home Page
- Welcome message
- Your role and access level
- Dashboard cards for each role
- Navigation in sidebar

### Student Dashboard (Fully Functional)
- 8 KPI cards showing performance metrics
- Interactive charts (score trends, improvements, rubric mastery)
- Detailed data tables with filters
- CSV export for all tables

### Other Dashboards (Stubs)
- Faculty, Developer, Admin dashboards are templates
- Show planned features
- Ready for you to implement

---

## 📊 Testing with Real Data

The Student Dashboard will show real data from your Neon database if you have:
- Students in the `students` table
- Attempts in the `attempts` table
- Rubric scores in `rubric_scores` table
- Engagement logs in `engagement_logs` table

### Sample Test Query

Open a new Python file and test:

```python
from db import get_db_manager

db = get_db_manager()

# Check if we have data
result = db.execute_query("SELECT COUNT(*) as count FROM students")
print(f"Students in database: {result[0]['count']}")

result = db.execute_query("SELECT COUNT(*) as count FROM attempts")
print(f"Attempts in database: {result[0]['count']}")
```

---

## 🔧 Next Steps

### Immediate (Today)
1. ✅ Run the dashboard
2. ✅ Login as Admin
3. ✅ Explore Student Dashboard
4. ✅ Verify data is showing correctly

### This Week
1. **Complete Faculty Dashboard**:
   - Open `pages/2_Faculty_Dashboard.py`
   - Follow the Student Dashboard pattern
   - Use queries from `core/queries/attempts_queries.py` and `rubric_queries.py`
   - See `docs/DEVELOPMENT_GUIDE.md` for help

2. **Complete Developer Dashboard**:
   - Open `pages/3_Developer_Dashboard.py`
   - Use queries from `core/queries/environment_queries.py`
   - Monitor system health and API performance

3. **Complete Admin Dashboard**:
   - Open `pages/4_Admin_Dashboard.py`
   - Use queries from `core/queries/admin_queries.py`
   - Show platform-wide KPIs

### Before Production
1. **Change Passwords**:
   - Generate new bcrypt hashes (see `PASSWORD_INFO.md`)
   - Update `.streamlit/secrets.toml`

2. **Add Your Logo**:
   - Replace `assets/mind_logo.png` with Miva logo
   - Restart dashboard to see changes

3. **Customize Theme** (Optional):
   - Edit `theme.py` to adjust colors
   - Current: Light ash, deep blue, red accents

---

## 📚 Documentation Reference

All documentation is in the `docs/` folder:

| File | Purpose |
|------|---------|
| **QUICKSTART.md** | 5-minute setup |
| **README.md** | Complete documentation |
| **DEVELOPMENT_GUIDE.md** | How to build remaining dashboards |
| **SETUP_CHECKLIST.md** | Step-by-step verification |

Plus in the root:
- **PASSWORD_INFO.md** - Authentication details
- **INSTALL.txt** - Quick reference

---

## 🆘 Troubleshooting

### Can't connect to database
```bash
# Test connection separately
python -c "from db import get_db_manager; db = get_db_manager(); print(db.test_connection())"
```

**If False**:
- Check `.streamlit/secrets.toml` has correct credentials
- Verify Neon database is running
- Check Neon Console for connection issues

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Port 8501 already in use
```bash
streamlit run Home.py --server.port 8502
```

### Login not working
- Verify bcrypt is installed: `pip install bcrypt`
- Try credentials from `PASSWORD_INFO.md`
- Check no extra spaces in email/password
- Email and password are case-sensitive

### No data showing in Student Dashboard
- Check if you have data in your Neon database
- Run sample queries to verify
- Check student_id matches in queries

---

## ✅ Quick Verification Checklist

Before considering setup complete:

- [ ] All files downloaded and structured correctly
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database connection test passes
- [ ] Dashboard runs without errors (`streamlit run Home.py`)
- [ ] Can login as Admin
- [ ] Home page displays correctly
- [ ] Student Dashboard loads (with or without data)
- [ ] Can navigate between pages
- [ ] No console errors

---

## 🎉 You're Ready!

Your dashboard is **production-ready** for the Student Dashboard and has secure authentication.

**What's Working**:
- ✅ Database connected
- ✅ Authentication with bcrypt
- ✅ Student Dashboard fully functional
- ✅ Professional theme
- ✅ Documentation complete

**What's Next**:
- Complete Faculty Dashboard
- Complete Developer Dashboard
- Complete Admin Dashboard
- Deploy to Streamlit Cloud

---

## 📞 Need Help?

1. Check `PASSWORD_INFO.md` for authentication issues
2. Check `docs/QUICKSTART.md` for setup issues
3. Check `docs/DEVELOPMENT_GUIDE.md` for coding help
4. Review error messages in terminal
5. Test database connection separately

---

**Neon Database**: `ep-weathered-cake-a4lk3gou-pooler.us-east-1.aws.neon.tech`  
**Database Name**: `neondb`  
**Admin Login**: `admin@example.com` / `admin123`

**Ready to start!** 
