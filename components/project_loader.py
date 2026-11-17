import os
import json
import streamlit as st


def load_all_projects():
    """Scans the projects directory and loads metadata and content for each project."""
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)
        return []

    projects = []
    for folder_name in os.listdir(projects_dir):
        folder_path = os.path.join(projects_dir, folder_name)
        if os.path.isdir(folder_path):
            meta_path = os.path.join(folder_path, "metadata.json")
            content_path = os.path.join(folder_path, "content.md")

            # Load metadata if it exists
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            else:
                metadata = {"title": folder_name, "summary": "No metadata found."}

            # Load markdown content if it exists
            content = ""
            if os.path.exists(content_path):
                with open(content_path, "r", encoding="utf-8") as f:
                    content = f.read()

            projects.append({
                "id": folder_name,
                "metadata": metadata,
                "content": content,
                "path": folder_path
            })
    return projects