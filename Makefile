all: submodules #worktrees

submodules:
	@git submodule foreach 'git fetch -t origin'
	@git submodule update --init
	git submodule status
