# ProjectCreater

ProjectCreater is a command-line tool that automates the setup of new Python (and full-stack) project folders. With a single command, you can scaffold a new project with best practices, install dependencies, set up version control, and even push to GitHub—all tailored to your needs.

## Features

- **Multiple Templates:** Choose from templates like basic Python, AI/ML, Flask, Django, FastAPI, CLI apps, automation scripts, bots, games, and even a FastAPI + React full-stack app.
- **Virtual Environment:** Automatically creates a `.venv` for isolated Python development.
- **Dependency Management:** Installs libraries you specify and common dev tools (black, flake8, pytest, pre-commit).
- **Docker Support:** Optionally adds Docker and docker-compose files.
- **Git & GitHub Integration:** Initializes a git repo, creates a `.gitignore`, and can create/push to a new GitHub repository (public or private).
- **License Selection:** Adds a license file (MIT, Apache, GPL, BSD, CC0) of your choice.
- **Interactive or CLI Use:** Configure everything interactively or via command-line arguments.
- **VS Code Integration:** Optionally opens your main script in VS Code and activates the virtual environment.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Alph702/ProjectCreater.git
cd ProjectCreater
```

### 2. (Optional/Windows) Use the installer

For Windows users, run:

```bash
install.bat
```

This copies the tool to your Python programs directory and adds it to your PATH.

### 3. Set up environment variables

Create an `env.py` file with your GitHub token and SSH URL:

```python
GITHUB_TOKEN = "your_github_token"
GITHUB_SSH_URL = "git@github.com:your_github_username"
```

## Usage

### Basic CLI Usage

```bash
python main.py <project_name> [options]
```

#### Example

```bash
python main.py my_new_project -l numpy pandas -t flask --github --private --docker -a -d -lic mit
```

### Interactive Mode

```bash
python main.py <project_name> --interactive
```

You'll be prompted to select templates, dev tools, licenses, and more.

### Options

- `project_name`                Name of the new project folder (required)
- `-l, --libraries`             Space-separated list of extra packages to install
- `-t, --template`              Project template (basic, ai-ml, ai-ml-dl, flask, django, fastapi, bot, game, cli, automation, fastapi-react)
- `-lic, --license`             License type (mit, apache, gpl, bsd, cc0)
- `-a, --activate`              Automatically activate the virtual environment
- `-d, --dev`                   Install common dev tools (black, flake8, pytest, pre-commit)
- `--docker`                    Add Docker and docker-compose files
- `--github`                    Create and push to a GitHub repo
- `--private`                   Make the GitHub repo private
- `--interactive`               Run interactive setup

## Example: Creating a Flask Project

```bash
python main.py my-flask-app -t flask --docker --github -l flask_sqlalchemy
```

This creates a Flask project, adds Docker support, initializes and pushes to GitHub, and installs Flask-SQLAlchemy.

## Templates

Supported templates include:

- **basic**: Empty Python project
- **ai-ml**: Data science/ML starter (numpy, pandas, matplotlib, scikit-learn)
- **ai-ml-dl**: Deep learning starter (adds tensorflow, torch)
- **flask**: Flask web app
- **django**: Django web app
- **fastapi**: FastAPI backend
- **bot**: Telegram bot example
- **game**: Pygame starter
- **cli**: Command-line tool starter
- **automation**: Automation script
- **fastapi-react**: Full-stack FastAPI + React

## Contributing

Contributions are welcome! Open an issue or submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for details.
