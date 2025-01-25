import json
import sys
import subprocess

# JSON 파일 경로
JSON_FILE_PATH = "/Users/nhn/projects/alfred-workflow/src/ssh/servers.json"

def load_data():
    with open(JSON_FILE_PATH, "r") as f:
        return json.load(f)

def list_groups(query=None):
    """1-depth 그룹 리스트 출력 (키워드 필터링 포함, 기본 10개 그룹 반환)"""
    data = load_data()
    groups = list(data.keys())

    # 키워드가 없는 경우, 최대 10개의 그룹만 반환
    if query is None:
        groups = groups[:10]

    results = [{"title": group, "arg": group} for group in groups if query is None or query.lower() in group.lower()]

    if not results:
        results.append({"title": "No matching groups found. query : " + query, "arg": ""})

    print(json.dumps({"items": results}, ensure_ascii=False, indent=2))

def list_phases(group_name):
    """선택한 그룹에 해당하는 phase 리스트 출력"""
    data = load_data()
    if group_name not in data:
        print(json.dumps({"items": [{"title": f"그룹 '{group_name}'이(가) 존재하지 않습니다.", "arg": ""}]}))
        return

    phases = ["alpha", "beta", "real"]
    results = [{"title": phase, "arg": f"{group_name} {phase}"} for phase in phases]
    print(json.dumps({"items": results}, ensure_ascii=False, indent=2))

def list_servers(group_name, phase, query=None):
    """선택한 그룹과 phase 내의 서버 리스트 출력 (키워드 필터링 포함)"""
    data = load_data()
    if group_name not in data or phase not in data[group_name]:
        print(json.dumps({"items": [{"title": f"그룹 '{group_name}'이나(가) '{phase}' phase가 존재하지 않습니다.", "arg": ""}]}))
        return

    servers = data[group_name][phase]
    results = []
    for server_name, details in servers.items():
        if query is None or query.lower() in server_name.lower():
            results.append({
                "title": f"{server_name} ({details['ip']})",
                "arg": f"{group_name} {phase} {server_name}"
            })
    print(json.dumps({"items": results}, ensure_ascii=False, indent=2))

def copy_ssh_command_to_clipboard(group_name, phase, server_name):
    """선택한 그룹, phase, 서버의 SSH 명령어를 클립보드에 복사"""
    data = load_data()
    if group_name not in data or phase not in data[group_name] or server_name not in data[group_name][phase]:
        print(f"'{group_name}' 그룹에서 '{phase}' phase의 '{server_name}' 서버를 찾을 수 없습니다.")
        return

    host = data[group_name][phase][server_name]['host']
    ssh_command = f"ssh irteam@{host}"

    # osascript를 사용해 클립보드에 SSH 명령어 복사
    applescript = f'''
    tell application "System Events"
        set the clipboard to "{ssh_command}"
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

    print(f"SSH 명령어가 클립보드에 복사되었습니다: {ssh_command}")

def main():
    if len(sys.argv) < 2:
        print("사용법: python script.py [list_groups|list_phases|list_servers|connect] ...")
        return

    command = sys.argv[1]

    if command == "list_groups":
        query = sys.argv[2] if len(sys.argv) > 2 else None
        list_groups(query)
    elif command == "list_phases":
        if len(sys.argv) < 3:
            print(json.dumps({"items": [{"title": "그룹 이름을 입력하세요.", "arg": ""}]}))
            return
        group_name = sys.argv[2]
        list_phases(group_name)
    elif command == "list_servers":
        if len(sys.argv) < 4:
            print(json.dumps({"items": [{"title": "그룹 이름과 phase를 입력하세요.", "arg": ""}]}))
            return
        group_name = sys.argv[2]
        phase = sys.argv[3]
        query = sys.argv[4] if len(sys.argv) > 4 else None
        list_servers(group_name, phase, query)
    elif command == "connect":
        if len(sys.argv) < 5:
            print("사용법: python script.py connect [group_name] [phase] [server_name]")
            return
        group_name = sys.argv[2]
        phase = sys.argv[3]
        server_name = sys.argv[4]
        copy_ssh_command_to_clipboard(group_name, phase, server_name)
    else:
        print(json.dumps({"items": [{"title": "알 수 없는 명령어입니다.", "arg": ""}]}))

if __name__ == "__main__":
    main()
