import os
import re
import sys
import json
import requests

# Retrieve environment variables
commit_messages = json.loads(os.getenv("COMMIT_MESSAGES"))
github_token = os.getenv("GITHUB_TOKEN")
complete_repo_name = os.getenv("REPO_NAME")
repo_name = str.split(complete_repo_name, '/')[1]

# Validate that all required variables exist
if not all([commit_messages, github_token, repo_name, complete_repo_name]):
    print("❌ Missing required environment variables.")
    sys.exit(1)

# Initialize a variable to track the issue number
first_issue_number = None

# Validate each commit message
for message in commit_messages:
    # Check if the commit follows the format ProjectName-IssueNumber: Description
    match = re.match(rf"{repo_name}-(\d+): .+", message)
    if not match:
        print(f"❌ Invalid commit message: '{message}'. Expected format: '{repo_name}-<number>: Description'.")
        sys.exit(1)

    # Extract the issue number from the commit message
    issue_number = match.group(1)

    # Ensure all commits are linked to the same issue
    if first_issue_number is None:
        first_issue_number = issue_number  # Set the first issue number
    elif issue_number != first_issue_number:
        print(f"❌ Inconsistent issue numbers in commits. Expected all commits to link to issue {repo_name}-{first_issue_number}, but found {repo_name}-{issue_number}.")
        sys.exit(1)

    print(f"🔍 Validating issue {repo_name}-{issue_number} for commit message: '{message}'")

# Validate the linked issue using the GitHub API
api_url = f"https://api.github.com/repos/{complete_repo_name}/issues/{first_issue_number}"
response = requests.get(
    api_url,
    headers={"Authorization": f"Bearer {github_token}"}
)

if response.status_code != 200:
    print(f"❌ Issue {repo_name}-{first_issue_number} does not exist.")
    sys.exit(1)

issue_data = response.json()
labels = [label["name"].lower() for label in issue_data.get("labels", [])]

# Check if the issue is in progress
if "in progress" not in labels:
    print(f"❌ Issue {repo_name}-{first_issue_number} is not 'in progress'. Current labels: {labels}")
    sys.exit(1)

print(f"✅ All commits are valid and linked to issue {repo_name}-{first_issue_number} in progress.")
