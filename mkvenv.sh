#!/bin/bash
set -e
mkdir -p "${HOME}/.local/venv/"
virtualenv -p /usr/bin/python3.9 "${HOME}/.local/venv/urna_eletronica"
source "${HOME}/.local/venv/urna_eletronica/bin/activate"
pip install -U pip
pip install -U -r "${PWD}/requirements.txt"
exit 0
