#!/bin/bash

# USAGE:
#   ./run_directory_check.sh swift
#   ./run_directory_check.sh python
#   ./run_directory_check.sh cpp
#   ./run_directory_check.sh go

LANGUAGE=$(echo "$1" | tr '[:upper:]' '[:lower:]')

if [[ -z "$LANGUAGE" ]]; then
  echo "❌ Usage: $0 <language>"
  echo "Example: $0 cpp"
  exit 1
fi

# Extension map
case "$LANGUAGE" in
  cpp)    EXT="cpp" ;;
  python) EXT="py" ;;
  go)     EXT="go" ;;
  swift)  EXT="swift" ;;
  *) echo "❌ Unsupported language: $LANGUAGE"; exit 1 ;;
esac

# Define the test logs directory based on language
TEST_LOGS_DIR="test-file-logs"
if [[ "$LANGUAGE" == "go" ]]; then
  TEST_LOGS_DIR=".test-file-logs"
fi

ROOT_DIR="tmp.benchmarks/polyglot-benchmark/${LANGUAGE}/exercises/practice"
TOTAL=0
PASSED=0
FAILED=0

echo "🔍 Checking all exercises under: $ROOT_DIR"
echo "==========================================================================="

for exercise_path in "$ROOT_DIR"/*/; do
  ((TOTAL++))
  EXERCISE=$(basename "$exercise_path")
  STATUS="✅ $EXERCISE: PASS"

  # Set documentation filenames based on language
  DOCS_INSTRUCTIONS="instructions.md"
  DOCS_INTRODUCTION="introduction.md"

  # Dynamic example path detection
  EXAMPLE_FILE="${exercise_path}/.meta/example.${EXT}"
  STUB_FILE="${exercise_path}/${EXERCISE}.${EXT}"
  TEST_FILE="${exercise_path}/${EXERCISE}_test.${EXT}"
  TEST_FILE_UNDER_LOGS="${exercise_path}/${TEST_LOGS_DIR}/$(basename "$TEST_FILE")"

  # Construct the FILES array
  FILES=(
    "${exercise_path}/.docs/${DOCS_INSTRUCTIONS}"
    "${exercise_path}/.docs/${DOCS_INTRODUCTION}"
    "${exercise_path}/.meta/config.json"
    "$EXAMPLE_FILE"
    "$STUB_FILE"
    "$TEST_FILE"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test1.${EXT}"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test1_output.txt"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test2.${EXT}"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test2_output.txt"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test3.${EXT}"
    "${exercise_path}/${TEST_LOGS_DIR}/negative_test3_output.txt"
    "$TEST_FILE_UNDER_LOGS"
  )
  
  for file in "${FILES[@]}"; do
    if [[ ! -f "$file" ]]; then
      STATUS="❌ $EXERCISE: FAIL (Missing: $file)"
      ((FAILED++))
      break
    elif ! grep -q '[^[:space:]]' "$file"; then
      STATUS="❌ $EXERCISE: FAIL (Empty or whitespace-only: $file)"
      ((FAILED++))
      break
    fi
  done

  if [[ "$STATUS" == ✅* ]]; then
    ((PASSED++))
  fi

  echo "$STATUS"
done


GREEN="\033[0;32m"
RED="\033[1;31m"
BLACK="\033[1;30m"
BOLD="\033[1m"
RESET="\033[0m"

# Summary
echo -e "\n${BLACK}${BOLD}================================= SUMMARY =================================${RESET}"
echo -e "${BLACK}🧪 Total Exercises Checked: ${BOLD}${TOTAL}${RESET}"
echo -e "${GREEN}✅ Passed: ${BOLD}${PASSED}${RESET}"
echo -e "${RED}❌ Failed: ${BOLD}${FAILED}${RESET}"
echo -e "${BLACK}${BOLD}===========================================================================${RESET}\n"

if [[ "$FAILED" -gt 0 ]]; then
  exit 1
fi

exit 0