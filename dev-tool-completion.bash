# dev-tool bash completion
_dev-tool_complete() {
    local cur prev words cword
    _init_completion || return

    case "$prev" in
        dev-tool)
            COMPREPLY=( $(compgen -W "crp git config upgrade batch-crp help" -- "$cur") )
            return 0
            ;;
        crp)
            COMPREPLY=( $(compgen -W "pack projects topics instances branches test --name --topic --branch --help" -- "$cur") )
            return 0
            ;;
        git)
            COMPREPLY=( $(compgen -W "tag merge test lasttag --name --org --branch --tag --reviewer --help" -- "$cur") )
            return 0
            ;;
        config)
            COMPREPLY=( $(compgen -W "crp git" -- "$cur") )
            return 0
            ;;
    esac

    # 参数补全
    case "$cur" in
        -*)
            case "$prev" in
                crp)
                    COMPREPLY=( $(compgen -W "--name --topic --branch --help" -- "$cur") )
                    ;;
                git)
                    COMPREPLY=( $(compgen -W "--name --org --branch --tag --reviewer --help" -- "$cur") )
                    ;;
            esac
            ;;
    esac
}

complete -F _dev-tool_complete dev-tool
