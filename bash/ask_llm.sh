# Binds Ctrl+k to get a command from AI

get_cmd_from_ai() {
    local query cmd ROOT_PROJECT_DIR
    ROOT_PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."

    query=$(fzf --print-query --prompt="> " --phony --height=5% --no-info < /dev/null)
    if [[ -z "$query" ]]; then
        return 1
    fi

    cmd=$($ROOT_PROJECT_DIR/.venv/bin/python $ROOT_PROJECT_DIR/src/main_llm.py "$query" "$PWD")

    READLINE_LINE="$cmd"
    READLINE_POINT=${#READLINE_LINE}
}

bind -x '"\C-k":get_cmd_from_ai'
