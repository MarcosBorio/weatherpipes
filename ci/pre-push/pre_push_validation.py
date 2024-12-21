import os
import sys
import requests
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Timestamp format
)

def get_in_progress_issues_via_project(token, repo_owner, repo_name, project_number, column_name="In progress"):
    """
    Retrieves all issues from a GitHub project that are in the specified column (e.g., "In progress").

    Parameters:
        token (str): GitHub personal access token for authentication.
        repo_owner (str): Owner of the repository.
        repo_name (str): Name of the repository.
        project_number (int): The project number within the repository.
        column_name (str): The name of the column to filter issues (default is "In progress").

    Returns:
        list: A list of prefixes corresponding to issues in the specified column.
    """
    try:
        # GitHub GraphQL API URL
        url = "https://api.github.com/graphql"

        # Set up the headers for authentication
        headers = {"Authorization": f"Bearer {token}"}

        # Define the GraphQL query
        query = """
        query($owner: String!, $repo: String!, $projectNumber: Int!) {
          repository(owner: $owner, name: $repo) {
            projectV2(number: $projectNumber) {
              items(first: 100) {
                nodes {
                  content {
                    ... on Issue {
                      number
                      title
                    }
                  }
                  fieldValues(first: 10) {
                    nodes {
                      __typename
                      ... on ProjectV2ItemFieldTextValue {
                        text
                      }
                      ... on ProjectV2ItemFieldSingleSelectValue {
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """

        # Define the variables for the GraphQL query
        variables = {
            "owner": repo_owner,
            "repo": repo_name,
            "projectNumber": project_number,
        }

        logging.info("Sending request to GitHub GraphQL API to fetch project issues...")

        # Make the POST request to the GitHub API
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

        # Handle errors in the API response
        if response.status_code != 200:
            logging.error(f"Error: Received status code {response.status_code}")
            logging.error(response.json())
            return []

        data = response.json()

        # Extract and filter issues based on the specified column name
        prefixes = []
        for item in data.get("data", {}).get("repository", {}).get("projectV2", {}).get("items", {}).get("nodes", []):
            field_values = item.get("fieldValues", {}).get("nodes", [])

            # Find the column name in field values
            column_name_value = next(
                (field.get("name") for field in field_values if field.get("__typename") == "ProjectV2ItemFieldSingleSelectValue" and field.get("name") == column_name),
                None
            )

            if column_name_value:
                content = item.get("content", {})
                if content:
                    prefix = f"{repo_name}-{content.get('number')}"
                    prefixes.append(prefix)

        logging.info(f"Found {len(prefixes)} prefixes in column '{column_name}'")
        return prefixes

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException occurred: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []

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
        logging.error(f"Error getting commit messages: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while retrieving commit messages: {e}")
        sys.exit(1)

def validate_commit_messages(commit_messages, in_progress_prefixes):
    """
    Validates that each commit message starts with a prefix from the in-progress issues.

    Parameters:
        commit_messages (list): A list of commit messages to validate.
        in_progress_prefixes (list): A list of prefixes corresponding to issues in "In Progress" status.

    Raises:
        SystemExit: If any commit message does not match the required prefix.

    Logs:
        Logs an error for any commit message that does not match.
        Logs a success message if all commit messages pass validation.
    """
    try:
        for message in commit_messages:
            if not any(message.startswith(prefix) for prefix in in_progress_prefixes):
                logging.error(f"Commit message '{message}' does not match any in-progress issue prefixes.")
                sys.exit(1)
        logging.info("All commit messages match in-progress issue prefixes.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during commit message validation: {e}")
        sys.exit(1)

def main():
    """
    Main function to validate commit messages against in-progress issues.
    """
    try:
        # Configuration
        from dotenv import load_dotenv
        load_dotenv()

        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token from environment variable
        REPO_OWNER = "MarcosBorio"
        REPO_NAME = "weatherpipes"  # Replace with your repository name
        PROJECT_NUMBER = 1

        if not GITHUB_TOKEN:
            logging.error("Missing GITHUB_TOKEN environment variable.")
            sys.exit(1)

        # Get commit messages
        commit_messages = get_commit_messages()
        if not commit_messages:
            logging.info("No commits to validate.")
            sys.exit(0)

        # Get in-progress issues
        in_progress_prefixes = get_in_progress_issues_via_project(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, PROJECT_NUMBER)
        if not in_progress_prefixes:
            logging.error("No issues found with the 'in progress' label.")
            sys.exit(1)

        # Validate commit messages
        validate_commit_messages(commit_messages, in_progress_prefixes)
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
