### alfred workflow

#### usage
<details>
<summary>인텔리제이 workflow</summary>

#### keyword filter
```zsh
query=$1
node_directory=$(which node)
workflow_js=path-to-build-intellij-js

$node_directory $workflow_js $query
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