"""
Project templates for different project types.
Each template includes a structure definition, description, and default name.
"""

# ==================== Project Templates ====================
PROJECT_TEMPLATES = {
    "🔬 Research / Data Science": {
        "description": "For scientific research, data analysis, and experiments",
        "structure": """# Research / Data Science Project
README.md
.gitignore
requirements.txt
src/
  main.py
  utils/
  analysis/
data/
  raw/
  processed/
  external/
results/
  figures/
  tables/
  models/
notebooks/
docs/
tests/
notes.md
""",
        "default_name": "research_project"
    },
    
    "🤖 Machine Learning": {
        "description": "For ML/AI projects with model training pipelines",
        "structure": """# Machine Learning Project
README.md
.gitignore
requirements.txt
pyproject.toml
src/
  __init__.py
  data/
    __init__.py
    dataset.py
    preprocessing.py
  models/
    __init__.py
    model.py
    layers.py
  training/
    __init__.py
    trainer.py
    callbacks.py
  evaluation/
    __init__.py
    metrics.py
  utils/
    __init__.py
    config.py
    logger.py
data/
  raw/
  processed/
  external/
models/
  checkpoints/
  exported/
experiments/
  configs/
  logs/
notebooks/
  exploration/
  experiments/
tests/
  test_models.py
  test_data.py
scripts/
  train.py
  evaluate.py
  inference.py
docs/
configs/
  config.yaml
""",
        "default_name": "ml_project"
    },
    
    "🌐 Web Application": {
        "description": "For full-stack web applications",
        "structure": """# Web Application
README.md
.gitignore
.env.example
package.json
docker-compose.yml
frontend/
  src/
    components/
    pages/
    hooks/
    utils/
    styles/
    assets/
  public/
  package.json
  tsconfig.json
backend/
  src/
    routes/
    controllers/
    models/
    middleware/
    services/
    utils/
  tests/
  package.json
shared/
  types/
  constants/
database/
  migrations/
  seeds/
docs/
  api/
scripts/
nginx/
""",
        "default_name": "web_app"
    },
    
    "📱 Mobile App": {
        "description": "For React Native or Flutter mobile applications",
        "structure": """# Mobile Application
README.md
.gitignore
.env.example
app.json
package.json
src/
  screens/
    Home/
    Profile/
    Settings/
  components/
    common/
    forms/
    navigation/
  hooks/
  services/
    api/
    storage/
  utils/
  constants/
  types/
  assets/
    images/
    fonts/
    icons/
  navigation/
  store/
    slices/
tests/
  __mocks__/
  screens/
  components/
ios/
android/
docs/
scripts/
""",
        "default_name": "mobile_app"
    },
    
    "📦 Python Package": {
        "description": "For distributable Python libraries/packages",
        "structure": """# Python Package
README.md
LICENSE
.gitignore
pyproject.toml
setup.py
MANIFEST.in
CHANGELOG.md
src/
  package_name/
    __init__.py
    core.py
    utils.py
    exceptions.py
    types.py
    cli.py
tests/
  __init__.py
  conftest.py
  test_core.py
  test_utils.py
docs/
  index.md
  api/
  guides/
  conf.py
  Makefile
examples/
  basic_usage.py
  advanced_usage.py
.github/
  workflows/
    ci.yml
    publish.yml
""",
        "default_name": "my_package"
    },
    
    "⚡ API Service": {
        "description": "For REST/GraphQL API backends",
        "structure": """# API Service
README.md
.gitignore
.env.example
requirements.txt
pyproject.toml
Dockerfile
docker-compose.yml
src/
  __init__.py
  main.py
  config.py
  api/
    __init__.py
    routes/
      __init__.py
      health.py
      users.py
    dependencies.py
  core/
    __init__.py
    security.py
    exceptions.py
  models/
    __init__.py
    user.py
    base.py
  schemas/
    __init__.py
    user.py
  services/
    __init__.py
    user_service.py
  db/
    __init__.py
    session.py
    migrations/
tests/
  __init__.py
  conftest.py
  api/
  services/
scripts/
  start.sh
  migrate.sh
docs/
  api/
alembic/
  versions/
  env.py
""",
        "default_name": "api_service"
    },
    
    "🔧 CLI Tool": {
        "description": "For command-line interface tools",
        "structure": """# CLI Tool
README.md
LICENSE
.gitignore
pyproject.toml
setup.py
src/
  cli_name/
    __init__.py
    __main__.py
    cli.py
    commands/
      __init__.py
      init.py
      run.py
      config.py
    core/
      __init__.py
      engine.py
    utils/
      __init__.py
      console.py
      config.py
    templates/
tests/
  __init__.py
  conftest.py
  test_cli.py
  test_commands/
docs/
  index.md
  commands/
  configuration.md
examples/
.github/
  workflows/
    ci.yml
""",
        "default_name": "my_cli"
    },
    
    "🎮 Game Project": {
        "description": "For game development projects",
        "structure": """# Game Project
README.md
.gitignore
requirements.txt
main.py
src/
  __init__.py
  game/
    __init__.py
    engine.py
    scenes/
      __init__.py
      menu.py
      gameplay.py
    entities/
      __init__.py
      player.py
      enemies.py
    systems/
      __init__.py
      physics.py
      audio.py
      input.py
    ui/
      __init__.py
      hud.py
      menu.py
  utils/
    __init__.py
    math.py
    helpers.py
assets/
  sprites/
    characters/
    environment/
    ui/
  audio/
    music/
    sfx/
  fonts/
  maps/
    levels/
data/
  configs/
  saves/
tests/
docs/
  design/
  art/
""",
        "default_name": "my_game"
    },
    
    "📊 Dashboard / Analytics": {
        "description": "For data dashboards and analytics platforms",
        "structure": """# Dashboard / Analytics
README.md
.gitignore
.env.example
requirements.txt
pyproject.toml
docker-compose.yml
app/
  __init__.py
  main.py
  config.py
  pages/
    __init__.py
    home.py
    analytics.py
    reports.py
  components/
    __init__.py
    charts.py
    tables.py
    filters.py
  data/
    __init__.py
    connectors/
    processors/
    cache/
  utils/
    __init__.py
assets/
  css/
  images/
data/
  raw/
  processed/
  exports/
notebooks/
  analysis/
  reports/
tests/
scripts/
  etl/
  reports/
docs/
configs/
""",
        "default_name": "analytics_dashboard"
    },
    
    "📝 Custom (Empty)": {
        "description": "Start with a blank template",
        "structure": """# Custom Project Structure
# Add your folders and files below
# Use 2-space indentation for nesting
README.md
.gitignore
src/
docs/
""",
        "default_name": "my_project"
    }
}

# Default template
DEFAULT_TEMPLATE_NAME = "🔬 Research / Data Science"
DEFAULT_STRUCTURE = PROJECT_TEMPLATES[DEFAULT_TEMPLATE_NAME]["structure"]


def get_template(name: str) -> dict:
    """Get a template by name, or return the default template if not found."""
    return PROJECT_TEMPLATES.get(name, PROJECT_TEMPLATES[DEFAULT_TEMPLATE_NAME])


def get_template_names() -> list:
    """Get a list of all available template names."""
    return list(PROJECT_TEMPLATES.keys())


def get_default_names() -> list:
    """Get a list of all default project names from templates."""
    return [t["default_name"] for t in PROJECT_TEMPLATES.values()]
