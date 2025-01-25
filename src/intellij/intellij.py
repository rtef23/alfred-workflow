import os
import sys
import json
from pathlib import Path

USER_HOME = Path.home()
INTELLIJ_META_DIRECTORY = '.idea'
INTELLIJ_META_NAME_FILE = '.idea/.name'
ENCODING = 'utf-8'
PROJECT_ROOT_DIRECTORIES = [
    USER_HOME / 'projects',
]

def convert_to(query):
    return query.strip().lower()

query = convert_to(sys.argv[1] if len(sys.argv) > 1 else '')

def enumerate_project_directories():
    projects = []
    for root_directory in PROJECT_ROOT_DIRECTORIES:
        if not root_directory.exists():
            continue

        for item in root_directory.iterdir():
            if item.is_dir() and is_intellij_project(item):
                project_directory = str(item)
                project_name = get_project_name(item)
                projects.append({
                    "projectName": project_name,
                    "projectDirectory": project_directory
                })
    return projects

def is_intellij_project(project_path):
    return (project_path / INTELLIJ_META_DIRECTORY).exists()

def get_project_name(project_path):
    meta_name_file = project_path / INTELLIJ_META_NAME_FILE
    if meta_name_file.exists():
        return meta_name_file.read_text(encoding=ENCODING).strip()
    else:
        return project_path.name

projects = enumerate_project_directories()

# 검색어 필터 적용
filtered_projects = [
    {
        "uid": project["projectName"],
        "title": project["projectName"],
        "arg": project["projectDirectory"]
    }
    for project in projects
    if query in project["projectName"].lower()
]

# 검색 결과가 없으면 프로젝트 이름 기준 정렬 후 상위 5개 출력
if not filtered_projects:
    sorted_projects = sorted(projects, key=lambda p: p["projectName"].lower())[:5]
    filtered_projects = [
        {
            "uid": project["projectName"],
            "title": project["projectName"],
            "arg": project["projectDirectory"]
        }
        for project in sorted_projects
    ]

print(json.dumps({"items": filtered_projects}))
