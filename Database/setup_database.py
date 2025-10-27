import sqlite3
from werkzeug.security import generate_password_hash

# --- Configuration: Define users with their roles ---
USERS_TO_ADD = [
    # (username, password, role)
    ("Aneel", "Aneel@22", "admin"),
    ("jejjari26", "Vinay@26", "admin"),
    ("Harsha", "Harsha123", "employee"),
    ("Durga", "Durga123", "employee"),
    ("Vinay", "Vinay123", "employee")
      # Example for a 'vinay' employee user
]
# This path points from hr_database up one level, then into the correct backend folder
DATABASE_FILE = "../Backend/Daily Aprovels/users.db"
# --- End Configuration ---


print("Setting up the user database with roles...")
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Drop existing tables for a clean setup
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS login_history")
print("🧹 Old tables dropped for a clean setup.")

# Create the users table with the new 'role' column
try:
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    print("✅ 'users' table with 'role' column created successfully.")
except Exception as e:
    print(f"❌ Error with 'users' table: {e}")

# Create the login_history table
try:
    cursor.execute("""
    CREATE TABLE login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        login_timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    print("✅ 'login_history' table created successfully.")
except Exception as e:
    print(f"❌ Error with 'login_history' table: {e}")

# Add the users to the table
for username, password, role in USERS_TO_ADD:
    password_hash = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    print(f"✅ User '{username}' with role '{role}' added successfully.")

conn.commit()
conn.close()


print("\nDatabase setup complete.")
