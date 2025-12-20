# MIND Unified Dashboard

Production-quality Streamlit multi-page dashboard with Google BigQuery backend, role-based access control (RBAC), and full dark mode support.

## 🌟 Features

- **Multi-page Dashboard**: Home, Student, Faculty, Developer, and Admin dashboards
- **Role-Based Access Control (RBAC)**: Secure authentication with bcrypt password hashing
- **BigQuery Integration**: Read-only access to MIND analytics database
- **Dark Mode Support**: Full dark mode with theme-aware logos and styling
- **Professional UI**: Clean, responsive design with interactive visualizations
- **Comprehensive Analytics**: 
  - Student performance tracking
  - Faculty cohort insights
  - Developer system monitoring
  - Admin organization metrics

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account
- BigQuery dataset configured
- Service account with appropriate permissions

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd mind-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure secrets**
```bash
# Copy the example secrets file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml with your actual credentials
```

4. **Add your logos** (optional but recommended)
```bash
# Place in assets/ folder:
# - miva_logo_light.png (for light mode - dark/colored logo)
# - miva_logo_dark.png (for dark mode - white/light logo)
```

5. **Run the application**
```bash
streamlit run app.py
# OR use the quick start script
./start.sh
```

6. **Access the dashboard**
Open your browser to `http://localhost:8501`

---

## 🔐 Authentication & Users

### Default Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| faculty | faculty123 | Faculty |
| developer | dev123 | Developer |
| student | student123 | Student |

⚠️ **IMPORTANT**: Change these passwords before deploying to production!

### Setting Up Custom Users

1. **Generate a bcrypt password hash:**
```python
import bcrypt
password = "your_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print(hashed)

# OR use the helper script:
python generate_password_hash.py your_password
```

2. **Add to `.streamlit/secrets.toml`:**
```toml
[users.username]
role = "Admin"  # or Faculty, Developer, Student
password_hash = "your_bcrypt_hash_here"
```

### Dashboard Access by Role

| Role | Access |
|------|--------|
| **Student** | Personal learning analytics, performance metrics, case study attempts |
| **Faculty** | Cohort performance, at-risk detection, rubric distributions |
| **Developer** | System monitoring, data freshness, error tracking |
| **Admin** | Full access to all dashboards + organization-wide KPIs |

---

## 🌙 Dark Mode

The dashboard includes full dark mode support with automatic logo switching.

### Using Dark Mode

1. **Toggle Theme**: Click the 🌙 (moon) or ☀️ (sun) button in the sidebar
2. **Theme persists** during your session
3. **Logo switches automatically** based on active theme

### Logo Setup

Place **two versions** of your logo in the `assets/` folder:

**Required Files:**
- `miva_logo_light.png` - Dark/colored logo for light backgrounds
- `miva_logo_dark.png` - White/light logo for dark backgrounds
- `miva_logo.png` - Optional fallback if theme-specific logos are missing

**Logo Specifications:**
- **Format**: PNG with transparency (recommended)
- **Width**: 200-300px
- **Height**: Proportional to width
- **Max Size**: 500KB for best performance

**Design Guidelines:**
- **Light Mode Logo**: Use dark or saturated colors that work on white (#FFFFFF) backgrounds
- **Dark Mode Logo**: Use white or very light colors that work on black (#0E1117) backgrounds

### Color Palette

**Light Mode:**
| Element | Color | Hex |
|---------|-------|-----|
| Background | White | `#FFFFFF` |
| Secondary BG | Light Gray | `#F0F2F6` |
| Text | Dark Gray | `#262730` |
| Primary Accent | MIVA Red | `#E31837` |

**Dark Mode:**
| Element | Color | Hex |
|---------|-------|-----|
| Background | Deep Black | `#0E1117` |
| Secondary BG | Dark Gray | `#262730` |
| Text | Very Light Gray | `#FAFAFA` |
| Primary Accent | MIVA Red | `#E31837` |

**Semantic Colors** (work in both modes):
- **Success**: Green `#2ca02c`
- **Warning**: Amber `#ffbb00`
- **Danger**: MIVA Red `#E31837`
- **Info**: Cyan `#17becf`

---

## ☁️ Deployment to Streamlit Cloud

### Prerequisites
- GitHub repository containing the code
- Google Cloud service account JSON key
- Streamlit Cloud account

### Step-by-Step Deployment

**1. Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit: MIND Dashboard"
git remote add origin https://github.com/YOUR-USERNAME/mind-dashboard.git
git push -u origin main
```

**2. Deploy on Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app"
- **Repository**: Select your `mind-dashboard` repo
- **Branch**: `main`
- **Main file**: `app.py`
- **App URL**: Choose a custom name (e.g., `mind-dashboard`)

**3. Configure Secrets**
- Before or after deploying, click "Advanced settings"
- In the "Secrets" section, paste your entire `.streamlit/secrets.toml` content
- Click "Save"

**4. Verify Deployment**
- App will be at: `https://your-app-name.streamlit.app`
- Test login and all dashboards
- Verify BigQuery connection works

### Updating Your Deployed App

```bash
# Make changes locally
git add .
git commit -m "Update dashboard"
git push origin main

# Streamlit Cloud auto-deploys on push!
```

---

## 🔧 BigQuery Configuration

### Project Details
- **Project ID**: `gen-lang-client-0625543859`
- **Dataset**: `mind_analytics`
- **Location**: `EU`

### Creating Service Account

**1. Navigate to GCP Console**
```
GCP Console → IAM & Admin → Service Accounts
```

**2. Create Service Account**
```bash
gcloud iam service-accounts create mind-dashboard-reader \
  --display-name="MIND Dashboard Reader" \
  --project=gen-lang-client-0625543859
```

**3. Grant BigQuery Permissions**
```bash
# Data Viewer role
gcloud projects add-iam-policy-binding gen-lang-client-0625543859 \
  --member="serviceAccount:mind-dashboard-reader@gen-lang-client-0625543859.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

# Job User role
gcloud projects add-iam-policy-binding gen-lang-client-0625543859 \
  --member="serviceAccount:mind-dashboard-reader@gen-lang-client-0625543859.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"
```

**4. Create and Download Key**
```bash
gcloud iam service-accounts keys create ~/mind-dashboard-key.json \
  --iam-account=mind-dashboard-reader@gen-lang-client-0625543859.iam.gserviceaccount.com

# View the key
cat ~/mind-dashboard-key.json
```

**5. Add to Secrets**
- Copy the **entire JSON content**
- Paste into `.streamlit/secrets.toml` under `[gcp_service_account]`
- For Streamlit Cloud: paste in the Secrets UI

### Required IAM Roles
Your service account needs these **minimum** permissions:
- `roles/bigquery.dataViewer` - View data in BigQuery
- `roles/bigquery.jobUser` - Run queries

**⚠️ Security Note**: Only grant read-only access. Never use admin or editor roles.

---

## 📁 Project Structure

```
mind-dashboard/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This comprehensive guide
├── .gitignore                  # Git ignore rules
├── start.sh                    # Quick start script
├── generate_password_hash.py   # Password utility
│
├── .streamlit/
│   ├── config.toml            # Streamlit theme configuration
│   └── secrets.toml.example   # Example secrets template
│
├── assets/
│   ├── README.md              # Logo placement instructions
│   ├── miva_logo_light.png    # Light mode logo (you add this)
│   └── miva_logo_dark.png     # Dark mode logo (you add this)
│
├── core/                       # Core modules
│   ├── __init__.py            # Package exports
│   ├── auth.py                # Authentication (bcrypt)
│   ├── db.py                  # BigQuery connection
│   ├── rbac.py                # Role-based access control
│   ├── theme.py               # Dark mode & theme management
│   └── settings.py            # Configuration & colors
│
├── pages/                      # Dashboard pages
│   ├── __init__.py
│   ├── home.py                # Home dashboard
│   ├── student.py             # Student analytics
│   ├── faculty.py             # Faculty insights
│   ├── developer.py           # System monitoring
│   └── admin.py               # Admin overview
│
├── components/                 # Reusable UI components
│   ├── __init__.py
│   └── ui.py                  # Charts, tables, KPIs
│
└── sql/                        # SQL reference
    └── example_queries.md     # Query examples
```

---

## 🛠️ Customization

### Changing Theme Colors

**Edit `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#E31837"          # Your accent color
backgroundColor = "#FFFFFF"        # Light mode background
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[theme.dark]
primaryColor = "#E31837"          # Accent (same as light)
backgroundColor = "#0E1117"        # Dark mode background
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
```

**Edit `core/settings.py` COLORS:**
```python
COLORS = {
    'primary': '#E31837',       # MIVA Red
    'secondary': '#262730',     # Dark gray
    'success': '#2ca02c',       # Green
    'warning': '#ffbb00',       # Amber
    'danger': '#E31837',        # MIVA Red
    'info': '#17becf'           # Cyan
}
```

### Adding New Pages

1. **Create** `pages/newpage.py`:
```python
import streamlit as st
from core.db import get_bigquery_client, run_query
from core.settings import get_table_ref

def render():
    st.title("New Page")
    # Your page code here
```

2. **Update** `core/rbac.py`:
```python
ROLE_PERMISSIONS = {
    'Student': ['Home', 'Student'],
    'Faculty': ['Home', 'Faculty', 'NewPage'],  # Add here
    # ...
}
```

3. **Update** `app.py` sidebar navigation:
```python
if 'NewPage' in accessible_pages:
    if st.button("📄 New Page", use_container_width=True):
        st.session_state.current_page = 'NewPage'
        st.rerun()
```

4. **Add routing** in `app.py`:
```python
elif current_page == 'NewPage':
    from pages import newpage
    newpage.render()
```

### Adding Custom Queries

```python
from core.settings import get_table_ref
from core.db import run_query, get_bigquery_client

# Get client
client = get_bigquery_client()

# Build query with proper table references
query = f"""
SELECT 
    u.name,
    COUNT(g.grade_id) as attempts,
    AVG(g.final_score) as avg_score
FROM {get_table_ref('grades')} g
LEFT JOIN {get_table_ref('user')} u ON g.user_id = u.user_id
GROUP BY u.name
ORDER BY avg_score DESC
LIMIT 10
"""

# Execute query with caching
result = run_query(query, client)

# Use result
if result is not None and not result.empty:
    st.dataframe(result)
```

---

## 🐛 Troubleshooting

### BigQuery Connection Issues

**Problem**: "Failed to initialize BigQuery client"

**Solutions**:
1. Verify service account JSON is complete and correctly formatted
2. Check `project_id` matches: `gen-lang-client-0625543859`
3. Ensure service account has `bigquery.dataViewer` + `bigquery.jobUser` roles
4. Test connection manually:
```python
from google.cloud import bigquery
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('path/to/key.json')
client = bigquery.Client(credentials=credentials, project='gen-lang-client-0625543859')
print(list(client.list_datasets()))
```

### Authentication Issues

**Problem**: "Invalid username or password"

**Solutions**:
1. Verify password hash was generated correctly with bcrypt
2. Check username exists in `secrets.toml` under `[users.username]`
3. Ensure `secrets.toml` is in `.streamlit/` directory
4. Try regenerating the hash:
```bash
python generate_password_hash.py your_password
```

### Table/Data Issues

**Problem**: "Table not found" or "No data available"

**Solutions**:
1. Verify dataset exists: `mind_analytics`
2. Check table names in BigQuery console
3. Ensure service account has access to dataset
4. Test query in BigQuery console first
5. Check table reference format: `` `project.dataset.table` ``

### Logo Display Issues

**Problem**: Logo not showing

**Solutions**:
1. Check exact file names:
   - `miva_logo_light.png` (not Logo_Light.png or .jpg)
   - `miva_logo_dark.png`
2. Verify files are in `assets/` folder
3. Check file permissions (should be readable)
4. Try refreshing browser (Ctrl + Shift + R)
5. Check browser console for errors (F12)

### Dark Mode Issues

**Problem**: Theme not switching or styles not applying

**Solutions**:
1. Clear browser cache completely
2. Hard refresh: Ctrl + Shift + R (Windows/Linux) or Cmd + Shift + R (Mac)
3. Try incognito/private browsing mode
4. Check `st.session_state` is working (view in browser console)
5. Verify `core/theme.py` is imported in `app.py`

### Deployment Issues

**Problem**: App won't start on Streamlit Cloud

**Solutions**:
1. Check logs in Streamlit Cloud UI
2. Verify `requirements.txt` includes all dependencies
3. Ensure `app.py` is at repository root
4. Check secrets are properly formatted (valid TOML syntax)
5. Remove any absolute file paths

---

## 📊 Example SQL Queries

### Student Performance
```sql
-- Get individual student performance
SELECT 
    u.name,
    c.title as case_study,
    AVG(g.final_score) as avg_score,
    COUNT(g.grade_id) as total_attempts,
    MAX(g.final_score) as best_score
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.user` u 
    ON g.user_id = u.user_id
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.casestudy` c
    ON g.case_study_id = c.case_study_id
WHERE u.user_id = 'USER_ID_HERE'
GROUP BY u.name, c.title
ORDER BY avg_score DESC
```

### Cohort Analytics
```sql
-- Cohort performance comparison
SELECT 
    u.cohort,
    COUNT(DISTINCT u.user_id) as total_students,
    COUNT(DISTINCT g.grade_id) as total_attempts,
    AVG(g.final_score) as avg_score,
    AVG(g.communication) as avg_communication,
    AVG(g.comprehension) as avg_comprehension,
    AVG(g.critical_thinking) as avg_critical_thinking
FROM `gen-lang-client-0625543859.mind_analytics.user` u
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
    ON u.user_id = g.user_id
WHERE u.cohort IS NOT NULL
GROUP BY u.cohort
ORDER BY avg_score DESC
```

### At-Risk Students
```sql
-- Identify students needing support
WITH student_stats AS (
    SELECT 
        u.user_id,
        u.name,
        u.student_email,
        COUNT(g.grade_id) as attempts,
        AVG(g.final_score) as avg_score,
        MAX(c.timestamp) as last_activity
    FROM `gen-lang-client-0625543859.mind_analytics.user` u
    LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
        ON u.user_id = g.user_id
    LEFT JOIN `gen-lang-client-0625543859.mind_analytics.conversation` c
        ON u.user_id = c.user_id
    GROUP BY u.user_id, u.name, u.student_email
)
SELECT *,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_activity, DAY) as days_inactive
FROM student_stats
WHERE avg_score < 70 OR attempts < 3 OR days_inactive > 30
ORDER BY avg_score ASC, days_inactive DESC
```

**More examples**: See `sql/example_queries.md`

---

## 📈 Performance Tips

1. **Query Optimization**
   - Use `LIMIT` clauses for large datasets
   - Add appropriate `WHERE` filters
   - Use aggregations in SQL rather than in Pandas
   - Avoid `SELECT *`, specify columns needed

2. **Caching**
   - Queries auto-cache for 5 minutes (`@st.cache_data`)
   - BigQuery client cached per session (`@st.cache_resource`)
   - Adjust TTL in function decorators if needed

3. **UI Performance**
   - Load critical data first
   - Use pagination for large tables
   - Lazy-load charts on demand
   - Keep dataframes under 10,000 rows when possible

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Use strong, unique passwords (12+ characters)
- [ ] Verify service account is read-only
- [ ] Remove any test/dummy data
- [ ] Add `.streamlit/secrets.toml` to `.gitignore`
- [ ] Never commit service account keys to Git
- [ ] Enable 2FA on GCP account
- [ ] Review IAM permissions regularly
- [ ] Set up BigQuery audit logging
- [ ] Use environment-specific credentials
- [ ] Implement password rotation policy
- [ ] Review user access quarterly

---

## 🧪 Testing Checklist

- [ ] **Local**: App starts without errors
- [ ] **Auth**: All 4 roles can login successfully
- [ ] **Pages**: All 5 dashboards load and display data
- [ ] **Charts**: Bar, line, pie, heatmap charts render
- [ ] **Tables**: Data tables display and export works
- [ ] **Filters**: Date filters and dropdowns function
- [ ] **Dark Mode**: Theme toggle switches properly
- [ ] **Logos**: Both light and dark logos display
- [ ] **BigQuery**: Queries execute successfully
- [ ] **Logout**: Logout clears session properly
- [ ] **Mobile**: UI is responsive on mobile devices
- [ ] **Browsers**: Works in Chrome, Firefox, Safari

---

## 📞 Support & Resources

### Documentation
- **Streamlit**: [docs.streamlit.io](https://docs.streamlit.io)
- **BigQuery**: [cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs)
- **Plotly**: [plotly.com/python](https://plotly.com/python/)

### Getting Help
1. Check this README's troubleshooting section
2. Review code comments in relevant files
3. Check Streamlit Community forum
4. Open GitHub issue with error details

### Contact
- **GitHub**: [repository-url]/issues
- **Email**: support@example.com

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Google Cloud BigQuery](https://cloud.google.com/bigquery) - Data warehouse
- [Plotly](https://plotly.com/) - Interactive charts
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [bcrypt](https://github.com/pyca/bcrypt/) - Password hashing

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Maintained by**: MIVA Team  
**License**: [Your License]
