#!/bin/bash

grep -vE '^$|#' extensions/molecule/resources/converge.yml | grep '\- role:' | awk -F '.' '{print $NF}' | while read -r r; do
  if ! grep -q "name: Verify ${r} role" extensions/molecule/resources/verify.yml; then
    echo -e "\n    - name: Verify ${r} role\n      ansible.builtin.import_tasks:\n        file: ../tests/verify_${r}.yml"
  fi
done
