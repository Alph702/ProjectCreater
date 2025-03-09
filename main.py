import os
import subprocess
import argparse
import platform
import shutil

def create_project(project_name, packages):
    """Creates a Python project folder with .venv and optional package installation."""
    
    # 1️⃣ Create the project folder
    os.makedirs(project_name, exist_ok=True)
    print(f"📁 Created project folder: {project_name}")

    # 2️⃣ Navigate into the project folder
    os.chdir(project_name)

    # 3️⃣ Create a virtual environment named `.venv`
    subprocess.run(["python", "-m", "venv", ".venv"])
    print("✅ Virtual environment created (.venv/)")

    # 4️⃣ Create basic empty project files
    open("main.py", "w").close()
    open("requirements.txt", "w").close()
    open("README.md", "w").close()
    open(".gitignore", "w").close()
    
    print("📝 Created files: main.py, requirements.txt, README.md, and .gitignore")

    # 5️⃣ Install dependencies if provided
    if packages:
        pip_path = ".venv/Scripts/pip" if platform.system() == "Windows" else ".venv/bin/pip"
        subprocess.run([pip_path, "install"] + packages)
        
        with open("requirements.txt", "w") as f:
            f.write("\n".join(packages))
        
        print(f"📦 Installed packages: {', '.join(packages)}")

    # 6️⃣ Initialize Git repository
    subprocess.run(["git", "init"])
    print("🎯 Git repository initialized!")

    # 7️⃣ Open `main.py` in VS Code
    code_path = shutil.which("code")  # Get the full path of `code`
    if code_path:
        subprocess.run([code_path, "main.py"])
        print("🚀 Opened main.py in VS Code!")
    else:
        print("⚠️ VS Code command not found! Please open main.py manually.")


    print("🚀 Project setup complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Python project setup with .venv & Git")
    parser.add_argument("project_name", type=str, help="Name of the project folder")
    parser.add_argument("-l", "--libraries", nargs="*", help="List of packages to install", default=[])
    parser.add_argument("-t", "--template", type=str, help="Template to use for project setup i.e ()", default="basic")

    args = parser.parse_args()
    create_project(args.project_name, args.libraries)
