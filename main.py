import os
import subprocess
import argparse
import shutil

# 📌 Project Templates
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


# 📜 License Templates
LICENSES = {
    "mit": """MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.
""",

    "apache": """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.
"License" shall mean the terms and conditions for use, reproduction, and 
distribution as defined by Sections 1 through 9 of this document.

"Licensor" shall mean the copyright owner or entity authorized by the 
copyright owner that is granting the License.

"Legal Entity" shall mean the union of the acting entity and all other 
entities that control, are controlled by, or are under common control with 
that entity.

(Full Apache License Text at: http://www.apache.org/licenses/LICENSE-2.0)

END OF TERMS AND CONDITIONS
""",

    "gpl": """GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc.
Everyone is permitted to copy and distribute verbatim copies of this 
license document, but changing it is not allowed.

Preamble:
The GNU General Public License is a free, copyleft license for software and 
other kinds of works.

The licenses for most software are designed to take away your freedom to 
share and change it. By contrast, the GNU General Public License is intended 
to guarantee your freedom to share and change all versions of a program--to 
make sure it remains free software for all its users.

(Full GPL License Text at: https://www.gnu.org/licenses/gpl-3.0.txt)
""",

    "bsd": """BSD 3-Clause License

Copyright (c) 2025, [Your Name]
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
   this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions, and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its 
   contributors may be used to endorse or promote products derived from 
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.

(Full BSD 3-Clause License at: https://opensource.org/licenses/BSD-3-Clause)
""",

    "cc0": """Creative Commons Legal Code
CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

The person who associated a work with this deed has dedicated the work to 
the public domain by waiving all of his or her rights to the work worldwide 
under copyright law, including all related and neighboring rights, to the 
extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial 
purposes, all without asking permission.

(Full CC0 License Text at: https://creativecommons.org/publicdomain/zero/1.0/legalcode)
"""
}


# 📜 Default `.gitignore` for Python projects
GITIGNORE_CONTENT = """# Ignore virtual environments
.venv/
env/
__pycache__/
*.pyc
*.pyo
.DS_Store
.idea/
.vscode/
"""

def create_project(project_name, libraries, template, license_type):
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

    # Install from template `requirements.txt`
    if os.path.exists("requirements.txt"):
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("📦 Installed packages from requirements.txt")

    # 6️⃣ Initialize Git repository
    subprocess.run(["git", "init"])
    print("🎯 Git repository initialized!")

    # 7️⃣ Create `.gitignore` file
    with open(".gitignore", "w") as f:
        f.write(GITIGNORE_CONTENT)
    print("📜 Created `.gitignore` file.")

    # 8️⃣ Create `LICENSE` file
    if license_type in LICENSES:
        with open("LICENSE", "w") as f:
            f.write(LICENSES[license_type])
        print(f"📜 Added {license_type.upper()} License.")

    # 9️⃣ Open `main.py` in VS Code
    code_path = shutil.which("code") or r"C:\Users\Amanat\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    if os.path.exists(code_path):
        subprocess.run([code_path, "main.py"])
        print("🚀 Opened main.py in VS Code!")
    else:
        print("⚠️ VS Code not found! Please open main.py manually.")

    print("🚀 Project setup complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Python project setup with .venv & Git")
    parser.add_argument("project_name", type=str, help="Name of the project folder")
    parser.add_argument("-l", "--libraries", nargs="*", help="List of packages to install", default=[])
    parser.add_argument("-t", "--template", type=str, help="Template to use for project setup")
    parser.add_argument("-L", "--license", type=str, choices=LICENSES.keys(), help="License type (e.g., mit, apache, gpl)", default="mit")

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

    create_project(args.project_name, args.libraries, template, args.license)
