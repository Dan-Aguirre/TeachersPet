import os
import sys
import subprocess

def check_and_install_deps():
    try:
        import flask
        import customtkinter
        import requests
        print("Dependencies found.")
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def setup_db():
    db_path = os.path.join("Backend", "game.db")
    if not os.path.exists(db_path):
        print("Database not found. Running setup and importing questions...")
        subprocess.check_call([sys.executable, "setup_db.py"], cwd="Backend")
        subprocess.check_call([sys.executable, "import_questions.py"], cwd="Backend")
    else:
        print("Database found. Skipping import.")

def run_app():
    print("Starting backend server...")
    backend_process = subprocess.Popen([sys.executable, "backend.py"], cwd="Backend")
    
    print("Starting frontend interface...")
    frontend_dir = os.path.join("frontend", "src", "pages")
    
    try:
        # Run frontend and wait for it to close
        subprocess.run([sys.executable, "loginpage.py"], cwd=frontend_dir)
    finally:
        # Make sure backend shuts down when the frontend closes/crashes
        print("Shutting down backend...")
        backend_process.terminate()

if __name__ == "__main__":
    check_and_install_deps()
    setup_db()
    run_app()