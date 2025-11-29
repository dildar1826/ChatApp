import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug (optional)
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: SUPABASE_URL or SUPABASE_KEY not loaded!")
    print("Make sure .env is in the same folder as app.py")
    exit()

# Create client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# AUTH FUNCTIONS
# ============================================================

def signup():
    print("\n--- SIGNUP ---")
    email = input("Enter email: ")
    password = input("Enter password: ")

    try:
        supabase.auth.sign_up({"email": email, "password": password})
        print("Signup successful! Check your email for verification.\n")
    except Exception as e:
        print("Signup failed:", e, "\n")


def login():
    print("\n--- LOGIN ---")
    email = input("Email: ")
    password = input("Password: ")

    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        print("Logged in successfully!\n")
        return result.user.id
    except Exception as e:
        print("Login failed:", e, "\n")
        return None


# ============================================================
# TODO FUNCTIONS
# ============================================================

def read_todos(user_id):
    print("\n--- YOUR TODOS ---")

    data = supabase.table("todos").select("*").eq("user_id", user_id).execute()

    if not data.data:
        print("No todos found.\n")
        return

    for todo in data.data:
        print(f"{todo['id']}. {todo['task']}")

    print("----------------------\n")


def add_todo(user_id):
    print("\n--- ADD TODO ---")
    task = input("Enter todo: ")

    if task.strip() == "":
        print("Todo cannot be empty.\n")
        return

    supabase.table("todos").insert({"user_id": user_id, "task": task}).execute()
    print("Todo added!\n")


def delete_todo(user_id):
    print("\n--- DELETE TODO ---")
    todo_id = input("Enter todo ID: ")

    supabase.table("todos") \
            .delete() \
            .eq("id", todo_id) \
            .eq("user_id", user_id) \
            .execute()

    print("Todo deleted!\n")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    print("Welcome to Terminal TODO App")
    print("1. Login")
    print("2. Signup")
    choice = input("> ")

    user_id = None

    if choice == "1":
        user_id = login()
    elif choice == "2":
        signup()
        return
    else:
        print("Invalid choice")
        return

    if not user_id:
        return

    # User logged in successfully
    while True:
        print("\n--- MENU ---")
        print("1. Read Todos")
        print("2. Add Todo")
        print("3. Delete Todo")
        print("4. Logout")

        choice = input("> ")

        if choice == "1":
            read_todos(user_id)
        elif choice == "2":
            add_todo(user_id)
        elif choice == "3":
            delete_todo(user_id)
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid option\n")


if __name__ == "__main__":
    main()
