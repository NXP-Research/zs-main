# Linux bash script that handles the installation of required
# packages and the setup of the development environment. Running
# this script is more or less the equivalent of manually performing
# the steps presented in [1] (Linux)
#
# [1]: https://docs.zephyrproject.org/latest/develop/getting_started/index.html

#!/bin/bash

# immediately exit on error
set -e

# for logging purposes
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
NONE="\e[0m"

WORK_DIR=$(dirname $(pwd))
CRT_DIR=$(pwd)

log() {
	printf "$@""\n"
}

log_err() {
	local msg="$1"

	log "$RED$msg$NONE"
}

run_command() {
	local cmd="$@"
	local log_file="_log.out"

	$cmd &> "$log_file" || {\
		log_err "failed to execute command: $cmd";
		log_err "dumping command output:"
		cat "$log_file" && rm -rf "$log_file";
		return 1;
	}

	rm -rf "$log_file"

	return 0
}

install_packages() {
	for pkg in "$@"; do
		log "installing $YELLOW$pkg$NONE..."

		if ! run_command "sudo apt-get install -y $pkg"; then
			log_err "failed to install $pkg"
			return 1
		fi
	done

	return 0
}

# list of packages to install
PACKAGES=(
	git cmake ninja-build
	gperf ccache dfu-util
	device-tree-compiler wget python3-dev
	python3-venv python3-tk xz-utils file
	make gcc gcc-multilib g++-multilib
	libsdl2-dev libmagic1 curl minicom
)

setup_west() {
	# set up the virtual environment
	if [ ! -d "$WORK_DIR/.venv" ]; then
		log "setting up virtual environment at $WORK_DIR/.venv..."

		if ! run_command "python3 -m venv $WORK_DIR/.venv"; then
			log_err "failed to set up virtual environment"
			exit 1
		fi
	fi

	# activate the virtual environment
	log "activating virtual environment at $YELLOW$WORK_DIR/.venv$NONE..."
	source "$WORK_DIR"/.venv/bin/activate

	# install west if need be
	log "installing west..."
	if ! pip3 show &> /dev/null; then
		if ! run_command "pip3 install west"; then
			log_err "failed to install west"
			exit 1
		fi
	fi

	# initialize west if need be
	if [ ! -d "$WORK_DIR/.west" ]; then
		log "initializing west at $WORK_DIR..."

		if ! (cd $WORK_DIR && run_command "west init -l $CRT_DIR"); then
			log_err "failed to initialize west"
			exit 1
		fi
	fi

	# update the repositories
	log "updating repositories..."
	run_command "west update" || { log_err "failed to update repositories"; exit 1; }

	# export the CMAKE package
	log "exporting cmake package..."
	run_command "west zephyr-export" || { log_err "failed to export cmake package"; exit 1; }

	# install python package used by west
	log "installing west packages..."
	run_command "west packages pip --install" || {\
		log_err "failed to install west packages";
		exit 1;
	}

	# install the toolchain
	log "installing the toolchain..."
	run_command "west sdk install --install-base $WORK_DIR -t arm-zephyr-eabi" || {\
		log_err "failed to install the toolchain";
		exit 1;
	}

	log "$GREEN""west environment ready""$NONE"
	log "activate virtual environment by sourcing $YELLOW$WORK_DIR/.venv/bin/activate$NONE"
}

main() {
	install_packages "${PACKAGES[@]}"
	setup_west
}

main
