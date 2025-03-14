import os
import subprocess
import platform
import argparse
import shutil
import requests
import inquirer
from env import *
from template.config import *


# 📦 Function to Install Packages
def install_packages(packages):
    """Installs a list of packages inside the virtual environment."""
    if not packages:
        return
    pip_path = os.path.join(".venv", "Scripts", "pip") if platform.system() == "Windows" else ".venv/bin/pip"
    subprocess.run([pip_path, "install"] + packages, check=True)
    print(f"📦 Installed packages: {', '.join(packages)}")

# 🛠 Function to Detect OS and Activate Virtual Environment
def activate_virtual_env():
    """Automatically activates the virtual environment based on OS."""
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
        shell_cmd = ["cmd.exe", "/k", activate_cmd]  # Opens new command prompt
    else:
        activate_cmd = "source .venv/bin/activate"
        shell_cmd = ["bash", "-c", f"{activate_cmd} && exec bash"]  # Opens new terminal session

    try:
        subprocess.run(shell_cmd)
        print("⚡ Virtual environment activated!")
    except Exception:
        print(f"⚠️ Unable to auto-activate! Run manually:\n   {activate_cmd}")

# 🚀 Function to Create GitHub Repository
def create_github_repo(project_name, is_public):
    """Creates a GitHub repository and pushes the project via SSH."""

    # 🛠️ 1️⃣ Ask user for public/private repo choice
    repo_visibility = "public" if is_public else "private"
    print(f"🔹 Creating a {repo_visibility} GitHub repository...")

    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": project_name, "private": not is_public}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"✅ {repo_visibility.capitalize()} repository created successfully!")
    elif response.status_code == 422:
        print("⚠️ Repository already exists on GitHub.")
    else:
        print(f"❌ Failed to create repository: {response.json()}")
        return

    # 🛠️ 2️⃣ Initialize Git & Add Remote Repository
    print("🎯 Initializing Git repository...")
    subprocess.run(["git", "init"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Initial commit"])

    ssh_repo_url = f"{GITHUB_SSH_URL}/{project_name}.git"
    subprocess.run(["git", "remote", "add", "origin", ssh_repo_url])

    print(f"🔗 Remote repository added: {ssh_repo_url}")

    # 🛠️ 3️⃣ Push Code to GitHub
    print("🚀 Pushing project to GitHub...")
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

    print("✅ Project pushed successfully!")

def create_project(project_name, libraries, template, license_type, activate, install_dev_tools, docker, github, Is_private = False):
    """Creates a Python project folder with .venv, Git, .gitignore, and LICENSE."""
    
    # 1️⃣ Create the project folder
    os.makedirs(project_name, exist_ok=True)
    print(f"📁 Created project folder: {project_name}")

    # 2️⃣ Navigate into the project folder
    os.chdir(project_name)

    # 3️⃣ Create a virtual environment
    subprocess.run(["python", "-m", "venv", ".venv"])
    print("✅ Virtual environment created (.venv/)")

    # 4️⃣ Create project files based on template
    for path, content in TEMPLATES.get(template, []):
        if path.endswith("/"):
            os.makedirs(path, exist_ok=True)
        else:
            with open(path, "w") as f:
                if isinstance(content, list):  
                    f.write("\n".join(content))  # Convert list to newline-separated string
                else:
                    f.write(content or "")

    # 5️⃣ Install dependencies
    pip_path = os.path.join(".venv", "Scripts", "pip")
    if libraries:
        subprocess.run([pip_path, "install"] + libraries, check=True)
        with open("requirements.txt", "a") as f:
            for package in libraries:
                f.write(package + "\n")
        print(f"📦 Installed additional packages: {', '.join(libraries)}")

    if install_dev_tools:
        install_packages(DEV_TOOLS)
        with open(".pre-commit-config.yaml", "w") as f:
            f.write(PRE_COMMIT_CONFIG)
            print("✅ Created .pre-commit-config.yaml")
        subprocess.run([".venv/Scripts/pre-commit", "install"], check=True)
        print("🔗 Pre-commit hooks installed!")

    # Install from template `requirements.txt`
    if template != "basic" and os.path.exists("requirements.txt"):
            subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
            print("📦 Installed packages from requirements.txt")
    
    # 6️⃣ Create Docker files (if requested)
    if docker:
        with open("Dockerfile", "w") as f:
            f.write(DOCKERFILE)

        with open("docker-compose.yml", "w") as f:
            f.write(DOCKER_COMPOSE)

        print("🐳 Docker setup added!")

    # 7️⃣ Initialize Git repository
    subprocess.run(["git", "init"])
    print("🎯 Git repository initialized!")

    # 8️⃣ Create `.gitignore` file
    with open(".gitignore", "w") as f:
        f.write(GITIGNORE_CONTENT)
    print("📜 Created `.gitignore` file.")

    if github:
        create_github_repo(project_name, Is_private)
        

    # 9️⃣ Create `LICENSE` file
    if license_type in LICENSES:
        with open("LICENSE", "w") as f:
            f.write(LICENSES[license_type])
        print(f"📜 Added {license_type.upper()} License.")

    # 🔟 Open `main.py` in VS Code
    code_path = shutil.which("code") or r"C:\Users\Amanat\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    if os.path.exists(code_path):
        subprocess.run([code_path, "main.py"])
        print("🚀 Opened main.py in VS Code!")
    else:
        print("⚠️ VS Code not found! Please open main.py manually.")

    # 1️⃣1️⃣ Activate Virtual Environment
    if activate:
        activate_virtual_env()
        

    print("🚀 Project setup complete!")

def interactive_setup(project_name):
    """Runs an interactive prompt for project setup."""
    questions = [
        inquirer.List("template", message="Choose a project type", choices=list(TEMPLATES.keys())),
        inquirer.Confirm("github", message="Initialize Git repository?", default=True),
        inquirer.List("license_type", message="Select a license", choices=["MIT", "Apache-2.0", "GPL-3.0"], default="MIT"),
        inquirer.Confirm("docker", message="Include Docker support?", default=False),
        inquirer.Confirm("activate", message="Activate virtual environment after setup?", default=True),
        inquirer.Confirm("install_dev_tools", message="Install common dev tools (black, flake8, pytest, pre-commit)?", default=True),
        inquirer.Confirm("Is_private", message="Make the GitHub repository private?", default=False),
        inquirer.Text("libraries", message="Enter additional packages to install (space-separated)", default=""),
    ]
    answers = inquirer.prompt(questions)
    create_project(project_name=project_name,**answers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Python project setup with .venv & Git")
    parser.add_argument("project_name", type=str, help="Name of the project folder")
    parser.add_argument("-l", "--libraries", nargs="*", help="List of packages to install", default=[])
    parser.add_argument("-t", "--template", type=str, help="Template to use for project setup")
    parser.add_argument("-lic", "--license", type=str, choices=LICENSES.keys(), help="License type (e.g., mit, apache, gpl)", default="mit")
    parser.add_argument("-a", "--activate", action="store_true", help="Automatically activate virtual environment")
    parser.add_argument("-d", "--dev", action="store_true", help="Install common dev tools (black, flake8, pytest, pre-commit)")
    parser.add_argument("--docker", action="store_true", help="Add Docker support")
    parser.add_argument("--github", action="store_true", help="Create and push to GitHub repo")
    parser.add_argument("--private", action="store_true", help="Make the GitHub repository private")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    # Convert template input to lowercase & validate
    template_input = args.template.lower() if args.template else "basic"
    available_templates = {t.lower(): t for t in TEMPLATES}  

    if template_input not in available_templates:
        print(f"⚠️ Template '{args.template}' not found! Available templates:")
        print("\n".join(f"📋 {t}" for t in TEMPLATES.keys()))
        exit(1)
    else:
        template = available_templates[template_input]  


    if args.interactive:
        interactive_setup(project_name=args.project_name)
    elif args.project_name:
        create_project(args.project_name, args.libraries, template, args.license, args.activate, args.dev, args.docker, args.github, args.private)
    else:
        print("❌ Please provide a project name or use `--interactive` mode.")
