# Project Scaffold Builder

A modern cross-platform desktop app for macOS, Windows, and Linux that helps you quickly create consistent project folder structures with beautiful UI.

![Version](https://img.shields.io/badge/version-2.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

### 🎯 10 Built-in Project Templates
Choose from various project types with pre-configured folder structures:

| Template | Description |
|----------|-------------|
| 🔬 Research / Data Science | Scientific research, data analysis, experiments |
| 🤖 Machine Learning | ML/AI projects with training pipelines |
| 🌐 Web Application | Full-stack web applications |
| 📱 Mobile App | React Native / Flutter mobile apps |
| 📦 Python Package | Distributable Python libraries |
| ⚡ API Service | REST/GraphQL backend services |
| 🔧 CLI Tool | Command-line interface tools |
| 🎮 Game Project | Game development projects |
| 📊 Dashboard / Analytics | Data dashboards and analytics |
| 📝 Custom (Empty) | Start from scratch |

### 🎨 Modern UI Design
- Built with **CustomTkinter** for a sleek, modern appearance
- **Dark/Light theme** toggle
- Responsive layout with smooth scrolling
- Real-time structure preview with validation

### ⚡ Quick Actions
- One-click project creation
- Optional Git repository initialization
- Auto-open folder after creation
- Save/Load custom templates as JSON

## Installation

### Requirements
- Python 3.8+
- CustomTkinter (auto-installed on first run)

### Run
```bash
python app.py
```

On first run, `customtkinter` will be automatically installed if not present.

## Usage

1. **Select Project Type** - Choose a template from the dropdown
2. **Set Location** - Browse to select the base directory
3. **Name Your Project** - Enter your project name
4. **Customize Structure** - Edit the folder/file structure as needed
5. **Configure Options** - Toggle Git init, README content, etc.
6. **Create** - Click "✨ Create Project"

### Structure Syntax
- One item per line
- Use **2 spaces** for nesting levels
- Folder names can end with `/` (optional)
- Lines starting with `#` are comments

```text
README.md
.gitignore
src/
  main.py
  utils/
    helpers.py
data/
  raw/
  processed/
tests/
```

### Saving Templates
Click "Save" to export your current structure and settings as a JSON file for reuse.

## Screenshots

The app features a clean two-panel layout:
- **Left panel**: Project settings, template selection, and options
- **Right panel**: Editable structure editor and live preview

## Development

### Project Structure
```
Folder creator/
├── app.py          # Main application
└── README.md       # This file
```

### Tech Stack
- **CustomTkinter** - Modern UI framework
- **tkinter** - Native dialogs (file browser, etc.)
- **pathlib** - Cross-platform path handling

## License

MIT License - Feel free to use and modify.

## Contributing

Contributions are welcome! Feel free to:
- Add new project templates
- Improve UI/UX
- Add new features
- Report bugs
