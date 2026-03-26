#!/bin/bash

set -euo pipefail

VIRTUAL_ENV="$(uv run python -c "import sys; print(sys.prefix)")"
PYTHON_LIB_PATH="$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"

export VIRTUAL_ENV

echo "ANSIBLE_FILTER_PLUGINS: ${PYTHON_LIB_PATH}/molecule/provisioner/ansible/plugins/filter:${HOME}/.ansible/plugins/filter:/usr/share/ansible/plugins/filter
ANSIBLE_LIBRARY: ${PYTHON_LIB_PATH}/molecule/provisioner/ansible/plugins/modules:${PYTHON_LIB_PATH}/molecule_plugins/vagrant/modules:${HOME}/.ansible/plugins/modules:/usr/share/ansible/plugins/modules"
