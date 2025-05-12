import bcrypt
import random
import smtplib
import ssl
from getpass import getpass

# --- User database (in-memory for now) ---
users = {}

# --- Email OTP Sender ---
def send_otp(email, otp):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "your-email@gmail.com"  # Replace with your email
    password = "your-app-password"         # Use an app-specific password

    message = f"""\
    Subject: Your OTP Code

    Your OTP is: {otp}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)

# --- User signup ---
def signup():
    email = input("Email: ")
    password = getpass("Password: ")
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode(), salt)
    users[email] = hashed_pw
    print("✅ User registered!")

# --- Login flow ---
def login():
    email = input("Email: ")
    if email not in users:
        print("❌ No user found.")
        return

    password = getpass("Password: ")
    if not bcrypt.checkpw(password.encode(), users[email]):
        print("❌ Incorrect password.")
        return

    otp = str(random.randint(100000, 999999))
    print(f"Sending OTP to {email}... (mocked)")
    # send_otp(email, otp)  # Uncomment if you configure email
    print(f"[DEBUG] OTP: {otp}")
    user_otp = input("Enter the OTP: ")

    if user_otp == otp:
        print("✅ Login successful!")
    else:
        print("❌ Invalid OTP.")

# --- CLI Menu ---
while True:
    print("\n1. Signup\n2. Login\n3. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        signup()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("❌ Invalid choice.")
