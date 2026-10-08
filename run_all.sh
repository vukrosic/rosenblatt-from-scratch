#!/bin/bash
# Runs the seven steps, then the checks. About 4 minutes on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
PY="${PY:-python3}"
for step in step1_neuron step2_learn step3_mark1 step4_converge step5_xor step6_hidden step7_backprop; do
  echo
  echo "=== $step.py"
  $PY $step.py
done
echo
$PY tests.py
