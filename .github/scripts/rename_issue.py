import os
import sys
import requests

# Retrieve environment variables provided by the workflow
repo_name = str.split(os.getenv("REPO_NAME"), '/')[1]
print(repo_name)
issue_number = os.getenv("ISSUE_NUMBER")
original_title = os.getenv("ORIGINAL_TITLE")
github_token = os.getenv("GITHUB_TOKEN")

# Validate that all required variables are defined
if not all([repo_name, issue_number, original_title, github_token]):
    print("❌ Missing required environment variables.")
    sys.exit(1)

# Construct the new issue title
new_title = f"{repo_name}-{issue_number}: {original_title}"
print(f"🔧 Renaming issue to: {new_title}")

# GitHub API URL to update the issue
api_url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}"

# Make a PATCH request to the GitHub API to update the issue title
response = requests.patch(
    api_url,
    headers={
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    },
    json={"title": new_title},
)

# Verify the API response
if response.status_code == 200:
    print("✅ Issue title updated successfully!")
else:
    print(f"❌ Failed to update issue. HTTP {response.status_code}")
    print(response.json())
    sys.exit(1)
