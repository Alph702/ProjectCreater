import os
import subprocess
import argparse
import platform
import shutil

TEMPLATES = {
    "flask-react": [
        ("backend/app.py", 'from flask import Flask\napp = Flask(__name__)\n\n@app.route("/")\ndef home():\n    return {"message": "Hello, Flask!"}\n\nif __name__ == "__main__":\n    app.run(debug=True)'),
        ("backend/requirements.txt", ["flask"]),
        ("frontend/", None),
        ("frontend/src/", None),
        ("frontend/src/App.js", 'function App() { return <h1>Hello, React + Flask!</h1>; }\nexport default App;'),
        ("frontend/package.json", '{ "name": "frontend", "dependencies": { "react": "^18.0.0" } }'),
        ("README.md", "# Flask + React Full-Stack App"),
    ],
    "fastapi-react": [
        ("backend/main.py", 'from fastapi import FastAPI\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"message": "Hello, FastAPI!"}'),
        ("backend/requirements.txt", ["fastapi", "uvicorn"]),
        ("frontend/", None),
        ("frontend/src/", None),
        ("frontend/src/App.js", 'function App() { return <h1>Hello, React + FastAPI!</h1>; }\nexport default App;'),
        ("frontend/package.json", '{ "name": "frontend", "dependencies": { "react": "^18.0.0" } }'),
        ("README.md", "# FastAPI + React Full-Stack App"),
    ],
    "ai-ml-dl": [
        ("main.py", 'import torch\nimport tensorflow as tf\nprint("Deep Learning Ready!")'),
        ("requirements.txt", ["numpy", "pandas", "matplotlib", "scikit-learn", "tensorflow", "torch"]),
        ("README.md", "# AI/ML + Deep Learning Project"),
        ("data/", None),
        ("notebooks/", None),
    ],
    "bot": [
        ("bot.py", 'import telebot\nbot = telebot.TeleBot("YOUR_API_KEY")\n\n@bot.message_handler(commands=["start"])\ndef start(message):\n    bot.send_message(message.chat.id, "Hello! I am a bot.")\n\nbot.polling()'),
        ("requirements.txt", ["pyTelegramBotAPI"]),
        ("README.md", "# Telegram Bot Project"),
    ],
    "game": [
        ("game.py", 'import pygame\npygame.init()\nscreen = pygame.display.set_mode((800, 600))\nrunning = True\nwhile running:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            running = False\npygame.quit()'),
        ("requirements.txt", ["pygame"]),
        ("README.md", "# Game Development with Pygame"),
    ],
    "flask": [
        ("app.py", 'from flask import Flask\napp = Flask(__name__)\n\n@app.route("/")\ndef home():\n    return "Hello, Flask!"\n\nif __name__ == "__main__":\n    app.run(debug=True)'),
        ("requirements.txt", ["flask"]),
        ("README.md", "# Flask Project"),
        ("static/", None),
        ("templates/", None),
    ],
    "django": [
        ("manage.py", 'import os\nimport sys\n\nif __name__ == "__main__":\n    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")\n    try:\n        from django.core.management import execute_from_command_line\n    except ImportError as exc:\n        raise ImportError("Couldn\'t import Django. Are you sure it\'s installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc\n    execute_from_command_line(sys.argv)'),
        ("requirements.txt", ["django"]),
        ("README.md", "# Django Project"),
    ],
    "fastapi": [
        ("main.py", 'from fastapi import FastAPI\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"message": "Hello, FastAPI!"}'),
        ("requirements.txt", ["fastapi", "uvicorn"]),
        ("README.md", "# FastAPI Project"),
    ],
    "ai-ml": [
        ("main.py", 'import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nprint("AI/ML Project Ready!")'),
        ("requirements.txt", ["numpy", "pandas", "matplotlib", "scikit-learn"]),
        ("README.md", "# AI/ML Project"),
        ("data/", None),
        ("notebooks/", None),
    ],
    "cli": [
        ("main.py", 'import argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description="CLI Tool")\n    parser.add_argument("--name", help="Your name")\n    args = parser.parse_args()\n    print(f"Hello, {args.name}!")\n\nif __name__ == "__main__":\n    main()'),
        ("requirements.txt", []),  # Empty requirements file
        ("README.md", "# CLI Tool"),
    ],
    "automation": [
        ("script.py", 'import os\nprint("Automation script ready!")'),
        ("requirements.txt", []),  # Empty requirements file
        ("README.md", "# Automation Script"),
    ],
    "basic": [
        ("main.py", ""),
        ("requirements.txt", []),  # Empty requirements file
        ("README.md", ""),
    ],
}


def create_project(project_name, libraries, template = "basic"):
    """Creates a Python project folder with .venv and optional package installation."""
    
    # Check for required dependencies
    if shutil.which("git") is None:
        raise FileNotFoundError("⚠️ Git is not installed! Please install Git and retry.")
        
    
    # 1️⃣ Create the project folder
    os.makedirs(project_name, exist_ok=True)
    print(f"📁 Created project folder: {project_name}")

    # 2️⃣ Navigate into the project folder
    os.chdir(project_name)

    # 3️⃣ Create a virtual environment named `.venv`
    subprocess.run(["python", "-m", "venv", ".venv"])
    print("✅ Virtual environment created (.venv/)")

    # Create project files based on template
    for path, content in TEMPLATES.get(template, []):
        if path.endswith("/"):
            os.makedirs(path, exist_ok=True)
        else:
            with open(path, "w") as f:
                if isinstance(content, list):  
                    f.write("\n".join(content))  # Convert list to newline-separated string
                else:
                    f.write(content or "")  # Write content if not None


    # 5️⃣ Install dependencies if provided
    packages = libraries if libraries else []

    pip_path = os.path.join(".venv", "Scripts", "pip") if platform.system() == "Windows" else os.path.join(".venv", "bin", "pip")
    if packages:
        subprocess.run([pip_path, "install"] + packages, check=True)
        # Ensure requirements.txt is written correctly
        with open("requirements.txt", "w") as f:
            for package in (packages if isinstance(packages, list) else [packages]):
                f.write(package + "\n")

        print(f"📦 Installed packages: {', '.join(packages)}")
    else:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("📦 Installed packages from requirements.txt")

    # 6️⃣ Initialize Git repository
    subprocess.run(["git", "init"])
    print("🎯 Git repository initialized!")

    # 7️⃣ Open `main.py` in VS Code
    code_path = shutil.which("code")  # Get the full path of `code`
    if code_path:
        subprocess.run([code_path, "main.py"])
    else:
        print("⚠️ VS Code command not found! Please open main.py manually.")


    print("🚀 Project setup complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Python project setup with .venv & Git")
    parser.add_argument("project_name", type=str, help="Name of the project folder")
    parser.add_argument("-l", "--libraries", nargs="*", help="List of packages to install", default=[])
    parser.add_argument("-t", "--template", type=str, help="Template to use for project setup", default="basic")

    args = parser.parse_args()
    
    if args.template:
        template = args.template.lower()
        available_templates = {t.lower(): t for t in TEMPLATES}  # Map lowercase to original names

        if template not in available_templates:
            print(f"⚠️ Template '{args.template}' not found! Available templates:")
            print("\n".join(f"📋 {t}" for t in TEMPLATES.keys()))
            exit(1)  # Exit if an invalid template is provided
        else:
            template = available_templates[template]  # Convert back to original name

    create_project(args.project_name, args.libraries, template)
