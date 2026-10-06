import os
import subprocess
import random
from datetime import datetime, timedelta

# --- STRICT TIMELINE CONFIGURATION ---
START_DATE = datetime(2026, 3, 25, 9, 0, 0)
END_DATE = datetime(2026, 5, 30, 23, 59, 59)
TEMP_BRANCH = "temp-dataset-timeline"

def run_cmd(cmd, env=None):
    """Executes a shell command and returns the output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running: {cmd}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()

def generate_timeline(total_commits):
    """Generates the scattered timeline, ignoring the 1 AM to 7 AM sleep window."""
    total_seconds = int((END_DATE - START_DATE).total_seconds())
    timestamps = []
    
    while len(timestamps) < total_commits:
        random_seconds = random.randint(0, total_seconds)
        dt = START_DATE + timedelta(seconds=random_seconds)
        
        # Skip the sleep window
        if 1 <= dt.hour <= 7:
            continue
            
        timestamps.append(dt)
        
    timestamps.sort()
    return timestamps

def main():
    print("[*] Reading your current Git history...")
    
    current_branch = run_cmd("git branch --show-current")
    if not current_branch:
        print("Error: You are in a detached HEAD state. Please checkout a branch first.")
        return

    log_output = run_cmd("git log --reverse --format='%H'")
    hashes = log_output.split("\n")
    
    if not hashes or not hashes[0]:
        print("No commits found in this repository.")
        return

    total_commits = len(hashes)
    print(f"[*] Found {total_commits} commits on branch '{current_branch}'. Generating timeline...")
    
    timestamps = generate_timeline(total_commits)
    
    print("[*] Rewriting history safely in the background...")
    
    run_cmd(f"git checkout {hashes[0]} --quiet")
    run_cmd(f"git checkout -b {TEMP_BRANCH} --quiet")
    
    # 3. Amend the first commit's date (ADDED --date FLAG)
    env = os.environ.copy()
    first_date = timestamps[0].strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_COMMITTER_DATE"] = first_date
    run_cmd(f'git commit --amend --no-edit --date="{first_date}"', env=env)

    # 4. Cherry-pick the remaining commits one by one (ADDED --date FLAG)
    for i, commit_hash in enumerate(hashes[1:], start=2):
        run_cmd(f"git cherry-pick {commit_hash}")
        
        git_date = timestamps[i-1].strftime("%Y-%m-%dT%H:%M:%S")
        env["GIT_COMMITTER_DATE"] = git_date
        run_cmd(f'git commit --amend --no-edit --date="{git_date}"', env=env)
        
    print(f"\n[*] History successfully rewritten. Overwriting '{current_branch}'...")

    run_cmd(f"git branch -M {TEMP_BRANCH} {current_branch}")

    print(f"\n[+] Success! Your timeline has been completely rewritten on the '{current_branch}' branch.")

if __name__ == "__main__":
    main()