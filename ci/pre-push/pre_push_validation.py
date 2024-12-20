import os
import sys
import requests
import subprocess

def get_in_progress_issues(github_token, repo_owner, repo_name):
    """
    Retrieves all issues in the 'in progress' state using the GitHub API.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {"Authorization": f"Bearer {github_token}"}
    params = {"state": "open", "labels": "in progress"}

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"\u274c Failed to fetch issues from GitHub. HTTP Status: {response.status_code}")
        sys.exit(1)

    issues = response.json()
    in_progress_prefixes = [f"{repo_name}-{issue['number']}" for issue in issues]
    return in_progress_prefixes


def get_commit_messages():
    """
    Retrieves the commit messages for the current push.
    """
    try:
        result = subprocess.check_output(
            ["git", "log", "origin/main..HEAD", "--pretty=format:%s"],
            universal_newlines=True
        ).strip()
        return result.split("\n") if result else []
    except subprocess.CalledProcessError as e:
        print(f"\u274c Error getting commit messages: {e}")
        sys.exit(1)

import sys

def validate_commit_messages(commit_messages, in_progress_prefixes):
    """
    Validates that each commit message starts with a prefix from the in-progress issues.
    """
    for message in commit_messages:
        if not any(message.startswith(prefix) for prefix in in_progress_prefixes):
            print(f"INFO: Commit message '{message}' does not match any in-progress issue prefixes.")
            sys.exit(1)
    print("SUCCESS: All commit messages match in-progress issue prefixes.")        


def main():
    """
    Main function to validate commit messages against in-progress issues.
    """
    # Configuration
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token from environment variable
    REPO_OWNER = "MarcosBorio"
    REPO_NAME = "weatherpipes"  # Replace with your repository name

    if not GITHUB_TOKEN:
        print("INFO: Missing GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Get commit messages
    commit_messages = get_commit_messages()
    if not commit_messages:
        print("INFO: No commits to validate.")
        sys.exit(0)

    # Get in-progress issues
    in_progress_prefixes = get_in_progress_issues(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
    if not in_progress_prefixes:
        print("INFO: No issues found with the 'in progress' label.")
        sys.exit(1)

    # Validate commit messages
    validate_commit_messages(commit_messages, in_progress_prefixes)

if __name__ == "__main__":
    main()