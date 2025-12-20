# MIND Unified Dashboard

Production-quality Streamlit multi-page dashboard with Google BigQuery backend and role-based access control (RBAC).

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

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the dashboard**
Open your browser to `http://localhost:8501`

## 🔐 Authentication

### Default Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| faculty | faculty123 | Faculty |
| developer | dev123 | Developer |
| student | student123 | Student |

### Setting Up Custom Users

1. Generate a bcrypt password hash:
```python
import bcrypt
password = "your_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print(hashed)
```

2. Add to `.streamlit/secrets.toml`:
```toml
[users.username]
role = "Admin"  # or Faculty, Developer, Student
password_hash = "your_bcrypt_hash"
```

## 📊 Dashboard Access by Role

### Student
- Personal learning analytics
- Performance metrics
- Case study attempts and scores

### Faculty
- Cohort performance overview
- At-risk student detection
- Rubric score distributions

### Developer
- System monitoring
- Data freshness checks
- Error tracking and anomaly detection

### Admin
- Full access to all dashboards
- Organization-wide KPIs
- User adoption metrics

## ☁️ Deployment to Streamlit Cloud

### Prerequisites
- GitHub repository containing the code
- Google Cloud service account JSON key
- Streamlit Cloud account

### Deployment Steps

1. **Push code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

3. **Configure secrets in Streamlit Cloud**
   - In your app settings, go to "Secrets"
   - Paste the contents of your `.streamlit/secrets.toml` file
   - Click "Save"

4. **Verify deployment**
   - Your app should be accessible at `https://your-app-name.streamlit.app`

## 🔧 BigQuery Configuration

### Service Account Permissions

Your GCP service account needs the following IAM roles:

**Minimum Required (Read-Only):**
- `roles/bigquery.dataViewer` - View data in BigQuery
- `roles/bigquery.jobUser` - Run queries

**Project Level:**
```bash
gcloud projects add-iam-policy-binding gen-lang-client-0625543859 \
  --member="serviceAccount:your-sa@project.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding gen-lang-client-0625543859 \
  --member="serviceAccount:your-sa@project.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"
```

**Dataset Level (Alternative):**
```bash
bq show --format=prettyjson gen-lang-client-0625543859:mind_analytics > dataset.json
# Edit dataset.json to add service account with READER role
bq update --source dataset.json gen-lang-client-0625543859:mind_analytics
```

### Creating a Service Account

1. **Navigate to GCP Console**
   - Go to IAM & Admin > Service Accounts

2. **Create Service Account**
   - Click "Create Service Account"
   - Name: `mind-dashboard-reader`
   - Description: "Read-only access for MIND Dashboard"

3. **Grant Permissions**
   - Add roles: `BigQuery Data Viewer` and `BigQuery Job User`

4. **Create Key**
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select JSON format
   - Download the key file

5. **Add to Secrets**
   - Copy the entire JSON content
   - Paste into `.streamlit/secrets.toml` under `[gcp_service_account]`

## 📁 Project Structure

```
mind-dashboard/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Example secrets template
│
├── assets/
│   └── README.md              # Logo and branding assets (place miva_logo.png here)
│
├── core/
│   ├── __init__.py
│   ├── auth.py                # Authentication logic
│   ├── db.py                  # BigQuery connection & queries
│   ├── rbac.py                # Role-based access control
│   └── settings.py            # Configuration & table mappings
│
├── pages/
│   ├── __init__.py
│   ├── home.py                # Home dashboard
│   ├── student.py             # Student dashboard
│   ├── faculty.py             # Faculty dashboard
│   ├── developer.py           # Developer dashboard
│   └── admin.py               # Admin dashboard
│
└── components/
    ├── __init__.py
    └── ui.py                  # Reusable UI components
```

## 🔒 Security Best Practices

1. **Never commit secrets**: Add `.streamlit/secrets.toml` to `.gitignore`
2. **Use read-only access**: Service account should only have viewer permissions
3. **Rotate credentials regularly**: Update service account keys periodically
4. **Use environment-specific secrets**: Different credentials for dev/staging/prod
5. **Monitor access logs**: Review BigQuery audit logs regularly

## 🐛 Troubleshooting

### Common Issues

**Issue: "Failed to initialize BigQuery client"**
- Verify service account JSON is correctly formatted in secrets
- Check that service account has required permissions
- Ensure project_id matches your GCP project

**Issue: "Invalid username or password"**
- Verify password hash is correctly generated
- Check that username exists in secrets.toml
- Ensure secrets.toml is in the correct location

**Issue: "Table not found"**
- Verify dataset name is correct: `mind_analytics`
- Check that tables exist in BigQuery
- Ensure service account has access to the dataset

**Issue: "Query execution error"**
- Check BigQuery quotas and limits
- Verify SQL syntax is compatible with BigQuery
- Review error details in the expanded error message

## 📈 Performance Optimization

- **Query Caching**: All queries are cached with `@st.cache_data` (5-minute TTL)
- **BigQuery Client**: Cached with `@st.cache_resource`
- **Efficient Queries**: Use aggregations and filters to minimize data transfer
- **Progressive Loading**: Load critical data first, secondary data later

## 🛠️ Customization

### Using Dark Mode

The dashboard includes a built-in dark mode toggle:

1. **Switch Themes**: Click the theme toggle button (🌙/☀️) in the sidebar
2. **Logo Support**: Place both light and dark versions of your logo in `assets/`:
   - `miva_logo_light.png` - For light mode
   - `miva_logo_dark.png` - For dark mode
3. **Theme Colors**: Configure in `.streamlit/config.toml`

**Dark Mode Colors:**
- Background: `#0E1117` (deep black)
- Secondary: `#262730` (dark gray)
- Text: `#FAFAFA` (very light gray)
- Accent: `#E31837` (MIVA red)

### Adding New Pages

1. Create a new file in `pages/` directory (e.g., `pages/custom.py`)
2. Implement a `render()` function
3. Add page to `core/rbac.py` role permissions
4. Add navigation button in `app.py`

### Adding New Queries

1. Create SQL query using `get_table_ref()` for table references
2. Use `run_query()` from `core/db.py`
3. Process results with pandas
4. Visualize with components from `components/ui.py`

### Modifying Styles

Edit the CSS in `app.py`:
```python
st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
""", unsafe_allow_html=True)
```

## 📝 License

[Your License Here]

## 🤝 Contributing

[Contribution Guidelines]

## 📧 Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@example.com

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
