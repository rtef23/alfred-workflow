### alfred workflow

#### usage
<details>
<summary>인텔리제이 workflow</summary>

#### keyword filter
- keyword : ij
- with space check
- argument optional
```zsh
import os
import sys
import subprocess

projects_directory = os.path.expanduser("~/Desktop/projects")  # 프로젝트 디렉토리 경로

# 프로젝트 목록을 가져오는 함수
def get_projects(directory):
    projects = []
    for root, dirs, files in os.walk(directory):
        if ".idea" in dirs:  # .idea 디렉토리가 있으면 IntelliJ 프로젝트로 간주
            projects.append(root)
    return projects

# Alfred용 항목 생성 함수
def generate_alfred_items(projects):
    items = []
    for project in projects:
        project_name = os.path.basename(project)
        items.append({
            'title': project_name,
            'subtitle': project,
            'arg': project  # 선택한 프로젝트 경로를 arg로 전달
        })
    return items

# Alfred가 입력한 query를 기반으로 프로젝트 목록을 필터링하고 결과 반환
def main(query):
    projects = get_projects(projects_directory)

    # 입력된 쿼리가 없으면 알파벳 순으로 정렬 후 상위 10개 프로젝트 선택
    if not query:
        # 알파벳 순으로 정렬하고 상위 10개 프로젝트를 가져옵니다
        projects = sorted(projects, key=lambda p: os.path.basename(p).lower())[:10]
    else:
        # 쿼리에 맞는 프로젝트 필터링
        projects = [p for p in projects if query.lower() in os.path.basename(p).lower()]

    # 결과를 알프레드에 반환
    items = generate_alfred_items(projects)
    print('{"items":' + str(items).replace("'", '"') + '}')

# 선택된 항목을 열기 위한 로직
if __name__ == "__main__":
    # Alfred가 'query' 값을 전달하면, 이를 처리하여 결과 반환
    if len(sys.argv) > 1:
        query = sys.argv[1]  # query 값은 사용자가 입력한 검색어
        main(query)
    else:
        # 'query'가 없다면 빈 문자열로 처리하여 알파벳 순으로 프로젝트 목록을 반환
        main("")

```

#### run script
```zsh
query=$1
intellij_cli_path=/usr/local/bin/idea

$intellij_cli_path $query
```
</details>

<details>
<summary>whale 북마크 workflow</summary>

#### keyword filter
```zsh
query=$1
node_directory=$(which node)
workflow_js=path-to-builded-whale-js

$node_directory $workflow_js $query
```

#### open url
</details>

<details>
<summary>kill workflow</summary>

#### keyword filter
```zsh
query=$1
node_directory=$(which node)
workflow_js=path-to-kill-js

$node_directory $workflow_js $query
```

#### terminal command
```zsh
kill -9 {query}
```
</details>