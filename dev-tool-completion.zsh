#compdef dev-tool
#autoload

local curcontext="$curcontext" state line
typeset -A opt_args

_dev-tool() {
    _arguments -C \
        '1: :->command' \
        '*: :->args'

    case $state in
        (command)
            local -a commands
            commands=(
                'crp:Manage CRP packages'
                'git:Manage git tags' 
                'batch-git:Batch process git tags'
                'config:Edit configuration'
                'upgrade:Upgrade dev-tool'
                'batch-crp:Batch process CRP packages'
                'help:Show help'
            )
            _describe 'command' commands
            ;;
        (args)
            case $words[2] in
                (crp)
                    _arguments -C \
                        '1: :->crp_command' \
                        '*: :->crp_args'
                    
                    case $state in
                        (crp_command)
                            local -a crp_commands
                            crp_commands=(
                                'list:List CRP packages'
                                'create:Create new CRP package'
                                'update:Update CRP package'
                            )
                            _describe 'crp command' crp_commands
                            ;;
                        (crp_args)
                            _arguments \
                                '--name[Package name]' \
                                '--topic[Topic name]' \
                                '--branch[Branch name]' \
                                '--help[Show help]'
                            ;;
                    esac
                    ;;
                (git)
                    _arguments -C \
                        '1: :->git_command' \
                        '*: :->git_args'
                    
                    case $state in
                        (git_command)
                            local -a git_commands
                            git_commands=(
                                'tag:Manage git tags'
                                'push:Push changes'
                                'create:Create new branch'
                            )
                            _describe 'git command' git_commands
                            ;;
                        (git_args)
                            _arguments \
                                '--name[Project name]' \
                                '--org[Organization]' \
                                '--branch[Branch name]' \
                                '--tag[Tag name]' \
                                '--reviewer[Reviewer]' \
                                '--help[Show help]'
                            ;;
                    esac
                    ;;
                (config)
                    _arguments \
                        '1: :(crp git batch-git)'
                    ;;
                (batch-git)
                    _arguments -C \
                        '1: :->batch_git_command' \
                        '*: :->batch_git_args'
                    
                    case $state in
                        (batch_git_command)
                            local -a batch_git_commands
                            batch_git_commands=(
                                'tag:Create batch git tags'
                                'merge:Merge batch git PRs'
                                'test:Test batch git tags'
                                'lasttag:Show last batch git tags'
                            )
                            _describe 'batch-git command' batch_git_commands
                            ;;
                        (batch_git_args)
                            _arguments \
                                '--config[Config file]' \
                                '--org[Organization]' \
                                '--branch[Branch name]' \
                                '--tag[Tag name]' \
                                '--reviewer[Reviewer]' \
                                '--help[Show help]'
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
}

compdef _dev-tool dev-tool
