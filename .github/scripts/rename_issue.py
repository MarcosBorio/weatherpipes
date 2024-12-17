import os
import sys
import requests

# Obtener variables de entorno proporcionadas por el workflow
repo_name = os.getenv("REPO_NAME")
issue_number = os.getenv("ISSUE_NUMBER")
original_title = os.getenv("ORIGINAL_TITLE")
github_token = os.getenv("GITHUB_TOKEN")
project_name = os.getenv("PROJECT_NAME", "WeatherProject")

# Validar que todas las variables estén definidas
if not all([repo_name, issue_number, original_title, github_token]):
    print("❌ Missing required environment variables.")
    sys.exit(1)

# Construir el nuevo título
new_title = f"{project_name}-{issue_number}: {original_title}"
print(f"🔧 Renaming issue to: {new_title}")

# URL de la API de GitHub
api_url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}"

# Llamada a la API de GitHub para actualizar el título
response = requests.patch(
    api_url,
    headers={
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    },
    json={"title": new_title},
)

# Verificar el resultado
if response.status_code == 200:
    print("✅ Issue title updated successfully!")
else:
    print(f"❌ Failed to update issue. HTTP {response.status_code}")
    print(response.json())
    sys.exit(1)
