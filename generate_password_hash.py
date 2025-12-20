#!/usr/bin/env python3
"""
Password Hash Generator for MIND Dashboard
Generates bcrypt password hashes for user authentication
"""

import bcrypt
import sys

def generate_hash(password):
    """Generate bcrypt hash for a password"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def main():
    print("=" * 60)
    print("MIND Dashboard - Password Hash Generator")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        # Password provided as argument
        password = sys.argv[1]
        print(f"Generating hash for provided password...")
    else:
        # Interactive mode
        password = input("Enter password to hash: ")
    
    if not password:
        print("Error: Password cannot be empty")
        sys.exit(1)
    
    print("\nGenerating hash...")
    hash_result = generate_hash(password)
    
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(f"\nPassword: {password}")
    print(f"Hash:     {hash_result}")
    
    print("\n" + "=" * 60)
    print("Add to secrets.toml:")
    print("=" * 60)
    print(f"""
[users.username]
role = "Admin"  # or Faculty, Developer, Student
password_hash = "{hash_result}"
    """)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
