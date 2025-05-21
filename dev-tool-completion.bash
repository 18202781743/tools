# bash completion for dev-tool

_dev-tool() {
    local cur prev words cword
    _init_completion || return

    case $prev in
        dev-tool)
            COMPREPLY=( $(compgen -W "crp git batch-git config upgrade help" -- "$cur") )
            return 0
            ;;
        crp)
            COMPREPLY=( $(compgen -W "pack test projects topics instances branches" -- "$cur") )
            return 0
            ;;
        git)
            COMPREPLY=( $(compgen -W "tag merge test lasttag" -- "$cur") )
            return 0
            ;;
        batch-git)
            COMPREPLY=( $(compgen -W "tag merge test lasttag" -- "$cur") )
            return 0
            ;;
    esac

    case ${words[1]} in
        crp)
            _dev-tool_crp
            ;;
        git)
            _dev-tool_git
            ;;
        batch-git)
            _dev-tool_batch_git
            ;;
    esac
}

_dev-tool_crp() {
    local cur prev words cword
    _init_completion || return

    case $prev in
        --name|--topic|--branch|--tag)
            return 0
            ;;
    esac

    if [[ $cur == -* ]]; then
        COMPREPLY=( $(compgen -W "--name --topic --branch --tag --help" -- "$cur") )
    fi
}

_dev-tool_git() {
    local cur prev words cword
    _init_completion || return

    case $prev in
        --name|--org|--branch|--tag|--reviewer)
            return 0
            ;;
    esac

    if [[ $cur == -* ]]; then
        COMPREPLY=( $(compgen -W "--name --org --branch --tag --reviewer --help" -- "$cur") )
    fi
}

_dev-tool_batch_git() {
    local cur prev words cword
    _init_completion || return

    case $prev in
        --config|--org|--branch|--tag|--reviewer)
            return 0
            ;;
    esac

    if [[ $cur == -* ]]; then
        COMPREPLY=( $(compgen -W "--config --org --branch --tag --reviewer --help" -- "$cur") )
    fi
}

complete -F _dev-tool dev-tool
