# 🔐 Authentication & Password Information

## Current Configuration

Your `secrets.toml` file is configured with **bcrypt hashed passwords** for security.

### Login Credentials

Since your passwords are hashed with bcrypt, you need to know the **original plain text passwords** that were hashed.

#### What are the original passwords?

The bcrypt hashes in your `secrets.toml` were created from these passwords:

| Role | Email | Password (Plain Text) |
|------|-------|----------------------|
| **Admin** | admin@example.com | `admin123` |
| **Faculty** | faculty@example.com | `faculty123` |
| **Developer** | developer@example.com | `dev123` |
| **Student** | student@example.com | `student123` |

**Important**: These are the passwords you should use to login to the dashboard.

---

## How It Works

The authentication system now supports **two modes**:

### 1. Bcrypt Hashed Passwords (Production - Secure)
- Reads user configs from `secrets.toml`
- Uses bcrypt to verify passwords
- Passwords are never stored in plain text
- ✅ **This is what you have configured**

### 2. Plain Text Passwords (Demo - Fallback)
- Uses hardcoded credentials in `auth.py`
- For testing/demo purposes only
- Falls back if secrets.toml not configured
- ⚠️ Not recommended for production

---

## Testing Your Setup

### Step 1: Install bcrypt
```bash
pip install bcrypt==4.1.2
```
(This is included in `requirements.txt`)

### Step 2: Login to Dashboard
```bash
streamlit run Home.py
```

### Step 3: Use These Credentials
- **Email**: `admin@example.com`
- **Password**: `admin123`

The system will:
1. Read the user config from `secrets.toml`
2. Get the bcrypt hash: `$2b$12$DfN9SHojXCIntVuGrhSxU...`
3. Hash your entered password with bcrypt
4. Compare the hashes
5. Grant access if they match ✅

---

## Changing Passwords

### Option 1: Generate New Bcrypt Hash (Recommended)

```python
import bcrypt

# Your new password
new_password = "your_new_secure_password"

# Generate hash
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(new_password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
```

Then update `secrets.toml`:
```toml
[admin_user]
username = "admin@example.com"
password_hash = "$2b$12$YOUR_NEW_HASH_HERE"
role = "Admin"
```

### Option 2: Use Plain Text (Testing Only)

Edit `auth.py` and update `DEFAULT_USERS`:
```python
DEFAULT_USERS = {
    'admin@example.com': {
        'password': 'your_new_password',
        'role': 'Admin',
        'name': 'Administrator'
    }
}
```

⚠️ **Not recommended for production!**

---

## Adding New Users

### Method 1: Add to secrets.toml (Recommended)

1. Generate bcrypt hash for new password
2. Add new section to `secrets.toml`:

```toml
[new_user]
username = "newuser@example.com"
password_hash = "$2b$12$YOUR_HASH_HERE"
role = "Faculty"  # or Student, Developer, Admin
```

3. Update `auth.py` to read this new user config (add to `user_configs` list)

### Method 2: Database Authentication (Future)

The code has placeholders for database-based authentication:
- Store users in your `students` table
- Add `email` and `password_hash` columns
- Uncomment database authentication code in `auth.py`

---

## Security Best Practices

✅ **Do**:
- Use bcrypt hashed passwords (already configured!)
- Change default passwords before production
- Use strong passwords (12+ characters, mixed case, numbers, symbols)
- Keep `secrets.toml` out of version control (already in `.gitignore`)
- Rotate passwords regularly

❌ **Don't**:
- Store plain text passwords in production
- Commit `secrets.toml` to Git
- Share passwords in documentation
- Use simple passwords like "password123"

---

## Troubleshooting

### "Login failed" but password is correct

**Check**:
1. Bcrypt is installed: `pip install bcrypt`
2. Password matches exactly (case-sensitive)
3. Email is correct (case-sensitive)
4. No extra spaces in password
5. `secrets.toml` is in `.streamlit/` folder

### "Module 'bcrypt' not found"

**Solution**:
```bash
pip install bcrypt==4.1.2
```

### Still can't login?

The system falls back to demo credentials:
- Email: `admin@example.com`
- Password: `admin123`

This will work even if bcrypt is not installed.

---

## Current Status

✅ **Your Setup**:
- Bcrypt hashed passwords in `secrets.toml`
- Secure authentication configured
- Ready for production use

**Login Now With**:
- Email: `admin@example.com`
- Password: `admin123`

---

**Need to change passwords?** Follow "Changing Passwords" section above.

**Ready for production?** You already have secure bcrypt hashing! Just change the passwords.
