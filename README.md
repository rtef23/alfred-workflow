### alfred workflow

#### usage
<details>
<summary>인텔리제이 workflow</summary>

##### keyword filter
- keyword : ij
- with space check
- argument optional
- /usr/bin/python3
- with input as argv
```zsh
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

```

##### run script
- /bin/zsh
- with input as argv
```zsh
source ~/.zshrc

# 전달받은 프로젝트 경로를 변수에 저장
project_path="{query}"

echo 1

# 'which idea' 명령어로 IntelliJ IDEA의 실행 파일 경로 찾기
idea_path="/Users/nhn/Library/Application Support/JetBrains/Toolbox/scripts/idea"

echo $idea_path

# idea 명령어 경로가 존재하는지 확인
if [ -z "$idea_path" ]; then
    echo "IntelliJ IDEA의 'idea' 명령어를 찾을 수 없습니다. IntelliJ IDEA가 설치되어 있는지 확인하세요."
    exit 1
fi

# IntelliJ IDEA를 실행 (idea 명령어를 사용)
"$idea_path" "$project_path"
```
</details>

<details>
<summary>whale 북마크 workflow</summary>

#### keyword filter
- argument required
- /usr/bin/python3
- with input as argv
```zsh
import os
import sys
import json
from pathlib import Path

USER_HOME = Path.home()
WHALE_HOME_DIRECTORY = USER_HOME / 'Library' / 'Application Support' / 'Naver' / 'Whale'
WHALE_BOOKMARK_FILE = WHALE_HOME_DIRECTORY / 'Profile 1' / 'Bookmarks'

ENCODING = 'utf-8'
URL = 'url'
FOLDER = 'folder'

def convert_to(query):
    return query.strip().lower()

query = convert_to(sys.argv[1] if len(sys.argv) > 1 else '')

# 북마크 JSON 파일 로드
with open(WHALE_BOOKMARK_FILE, 'r', encoding=ENCODING) as file:
    bookmark_json = json.load(file)

bookmark_bar = bookmark_json.get('roots', {}).get('bookmark_bar', {})

def search(query, element):
    element_type = element.get('type')

    if element_type == URL:
        return search_url(query, element)
    elif element_type == FOLDER:
        return search_folder(query, element)
    else:
        return []

def search_folder(query, element):
    children = element.get('children', [])
    results = []
    for child in children:
        results.extend(search(query, child))
    return results

def search_url(query, element):
    url = element.get('url', '')
    name = element.get('name', '')
    
    is_search_target = not query or (query in url.lower() or query in name.lower())
    
    if is_search_target:
        return [{
            "uid": name,
            "title": name,
            "arg": url
        }]
    return []

filtered_items = search(query, bookmark_bar)

print(json.dumps({"items": filtered_items}, ensure_ascii=False))

```

#### open url
</details>

<details>
<summary>ssh copy workflow</summary>

```json
{
  "common_servers": {
    "common-server1": { "host": "common-server1", "ip": "12.34.56.78" },
    "common-server2": { "host": "common-server2", "ip": "12.34.56.78" }
  },
  "project-group-1": {
    "alpha": ["common-server1"],
    "beta": ["common-server2"],
    "real": {
      "each-server1": { "host": "each-server1", "ip": "12.34.56.789" },
      "each-server2": { "host": "each-server1", "ip": "12.34.56.789" }
    }
  },
  "project-group-2":{
    "dev": {
      "each-server3": { "host": "each-server3", "ip":  "12.34.56.79" },
      "each-server4": { "host": "each-server4", "ip":  "12.34.56.79" }
    },
    "alpha": ["common-server1"],
    "beta": ["common-server2"],
    "real": ["common-server2"]
  }
}
```

#### script filter
- keyword : ssh
- argument optional
- placeholder title : Select Group
- /bin/bash
- with input as {query}
```zsh
python3 /Users/nhn/projects/alfred-workflow/src/ssh/ssh.py ${path_to_json} list_groups {query}
```

#### script filter
- placeholder title : Select phase
- /bin/zsh --no-rcs
```zsh
python3 /Users/nhn/projects/alfred-workflow/src/ssh/ssh.py ${path_to_json} list_phases {query}

```

#### script filter
- placeholder title : Select Server
- /bin/zsh --no-rcs

```zsh
python3 /Users/nhn/projects/alfred-workflow/src/ssh/ssh.py ${path_to_json} list_servers {query}
```

#### run script
- /bin/bash
- with input as {query} 

```zsh
python3 /Users/nhn/projects/alfred-workflow/src/ssh/ssh.py ${path_to_json} connect {query}
```

</details>