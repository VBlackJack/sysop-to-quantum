#!/usr/bin/env python3
"""
Author: Julien Bombled
License: Apache License 2.0

This script scaffolds the directory structure and files for the SysOp to Quantum
documentation project using MkDocs.
"""

import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stdout
)

def create_directory(path: str) -> None:
    """Creates a directory if it does not exist."""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Failed to create directory {path}: {e}")
        sys.exit(1)

def write_file(path: str, content: str) -> None:
    """Writes content to a file, overwriting if it exists."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        logging.info(f"File created: {path}")
    except IOError as e:
        logging.error(f"Failed to write file {path}: {e}")

def main() -> None:
    """Main execution function."""
    base_dir = os.getcwd()
    logging.info(f"Starting scaffold in: {base_dir}")

    # Define file paths
    docs_dir = os.path.join(base_dir, "docs")
    infra_dir = os.path.join(docs_dir, "infra")
    github_workflows_dir = os.path.join(base_dir, ".github", "workflows")

    # Create directories
    create_directory(docs_dir)
    create_directory(infra_dir)
    create_directory(github_workflows_dir)

    # 1. mkdocs.yml
    mkdocs_content = """
site_name: De SysOp à l'Architecture Quantique
theme:
  name: material

nav:
  - Accueil: index.md
  - Fondations: []
  - Infrastructure:
    - Terraform: infra/terraform.md
  - Sécurité: []
  - Labs: []
  - Glossaire: glossaire.md
"""
    write_file(os.path.join(base_dir, "mkdocs.yml"), mkdocs_content)

    # 2. requirements.txt
    requirements_content = "mkdocs-material"
    write_file(os.path.join(base_dir, "requirements.txt"), requirements_content)

    # 3. .gitignore
    gitignore_content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
virtualenv/
.env

# MkDocs
site/
"""
    write_file(os.path.join(base_dir, ".gitignore"), gitignore_content)

    # 4. docs/index.md
    index_md_content = """
# De SysOp à l'Architecture Quantique

Bienvenue dans ce référentiel de documentation.

Ce projet a pour but de servir de veille technologique pour les équipes Ops.
Il explore l'hybridation entre le Cloud classique et l'informatique Quantique.

**Note :** L'approche se veut pragmatique et accessible, sans mathématiques complexes.
"""
    write_file(os.path.join(docs_dir, "index.md"), index_md_content)

    # 5. docs/glossaire.md
    glossaire_content = "# Glossaire"
    write_file(os.path.join(docs_dir, "glossaire.md"), glossaire_content)

    # 6. docs/infra/terraform.md
    terraform_content = "# Infrastructure Terraform"
    write_file(os.path.join(infra_dir, "terraform.md"), terraform_content)

    # 7. .github/workflows/publish.yml
    workflow_content = """
name: Publish Docs
on:
  push:
    branches:
      - main
      - master

permissions: 
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV
      - uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: .cache
          restore-keys: |
            mkdocs-material-
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
"""
    write_file(os.path.join(github_workflows_dir, "publish.yml"), workflow_content)

    logging.info("Scaffolding completed successfully.")

if __name__ == "__main__":
    main()
