from supabase import create_client, Client
import time
import os

SUPABASE_URL = "https://xtmankqkoyvisyolkdua.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh0bWFua3Frb3l2aXN5b2xrZHVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ0MjI4MDQsImV4cCI6MjA3OTk5ODgwNH0.0_7DNv_jRtD4wmvYKtKFUS6tFlGzy8dtzaaUd8AVO1k"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------
# AUTH FUNCTIONS
# ------------------------

def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    try:
        supabase.table("users").insert({
            "username": username,
            "password": password
        }).execute()

        print("\nUser created successfully!\n")
    except Exception as e:
        print("Signup error:", e)


def login():
    username = input("Username: ")
    password = input("Password: ")

    result = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()

    if result.data:
        print(f"\nLogged in as {username}\n")
        return result.data[0]  # return user data
    else:
        print("Invalid login!")
        return None


# ------------------------
# CHAT FUNCTIONS
# ------------------------

def send_message(user):
    msg = input("Enter your message: ")

    supabase.table("messages").insert({
        "user_id": user["id"],
        "username": user["username"],
        "content": msg
    }).execute()

    print("Message sent!\n")


def view_messages():
    msgs = supabase.table("messages").select("*").order("created_at").execute()

    print("\n--- CHAT ROOM ---")
    for m in msgs.data:
        print(f"[{m['created_at']}] {m['username']}: {m['content']}")
    print("-----------------\n")


# ------------------------
# MAIN LOOP
# ------------------------

def main():
    print("=== WELCOME TO TERMINAL CHAT ===")

    user = None
    while not user:
        print("\n1. Login")
        print("2. Signup")
        choice = input("Choose: ")

        if choice == "1":
            user = login()
        elif choice == "2":
            signup()
        else:
            print("Invalid choice")

    while True:
        print("\n1. Send Message")
        print("2. View Messages")
        print("3. Refresh Chat")
        print("4. Exit")
        option = input("Choose: ")

        if option == "1":
            send_message(user)
        elif option == "2":
            view_messages()
        elif option == "3":
            os.system("cls" if os.name == "nt" else "clear")
            view_messages()
        elif option == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
