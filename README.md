# Project Scaffold Builder

A small cross-platform desktop app for macOS and Windows that helps you create a clean project folder structure before you start coding.

## What it does
- Choose where to store a new project
- Set the project name
- Edit the default folder/file structure before creation
- Keep most defaults while renaming only the parts you want
- Optionally initialize a Git repository
- Optionally open the folder after creation
- Save and reload custom templates as JSON

## Why this fits your workflow
This is designed for a research + AI coding workflow where you often have many small projects and want a consistent structure without manually creating folders every time.

## Run it
Python 3 is enough. It uses the built-in Tkinter GUI toolkit.

```bash
python app.py
```

## Suggested default use
- Put active projects under `Research_Code/01_active_projects/`
- Put practice/demo work under `Research_Code/02_learning_and_demos/`
- Save a few templates, such as:
  - `research_project_template.json`
  - `demo_project_template.json`
  - `paper_figure_template.json`

## Structure syntax
Edit the structure in the big text box:
- One item per line
- Use 2 spaces for nesting
- Folder names can end with `/`
- File names usually do not end with `/`

Example:

```text
README.md
.gitignore
src/
  main.py
  utils/
data/
  raw/
  processed/
results/
```

## Good next improvements
Possible upgrades for a later version:
- Preset templates for Python / MATLAB / simulation / paper figures
- One-click `git init`, first commit, and GitHub remote setup
- Export as a standalone app bundle
- Duplicate detection and template validation
- A visual tree editor instead of text-based editing
