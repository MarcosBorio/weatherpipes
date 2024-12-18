import os
import re
import sys
import json

# Get commit messages
complete_repo_name = os.getenv("REPO_NAME")
repo_name = str.split(complete_repo_name, '/')[1]
commit_messages = json.loads(os.getenv("COMMIT_MESSAGES"))

# Validate each commit message
for message in commit_messages:
    if not re.match(rf"{repo_name}-\d+: .+", message):
        print(f"❌ Invalid commit message: '{message}'. Expected format: '{repo_name}-<number>: Description'.")
        sys.exit(1)

print("✅ All commit messages are valid.")