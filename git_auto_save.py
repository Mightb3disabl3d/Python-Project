import os
import subprocess
import time

# Path to your Git repository
repo_path = r"C:\Users\Theep\Downloads\Python Project"  # <-- change this

# Commit message
commit_message = "Auto-save commit"

# Time interval between saves (seconds)
interval = 10  # every minute

def has_changes():
    """Check if there are changes to commit."""
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return bool(result.stdout.strip())

def git_auto_save():
    while True:
        try:
            os.chdir(repo_path)
            
            if has_changes():
                # Stage all changes
                subprocess.run(["git", "add", "."], check=True)

                # Commit changes
                subprocess.run(["git", "commit", "-m", commit_message], check=True)

                # Push to GitHub
                subprocess.run(["git", "push"], check=True)

                print("Changes auto-saved to GitHub!")

            else:
                print("No changes to commit.")

        except subprocess.CalledProcessError as e:
            print("Git error:", e)

        time.sleep(interval)

if __name__ == "__main__":
    git_auto_save()