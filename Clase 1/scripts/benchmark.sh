#!/bin/bash

# Rigorous Benchmark Suite for CSV Parsing
# Author: Antigravity for Dr. Fuentes
# OS: macOS / Linux / Windows (Git Bash)

SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( dirname "$SCRIPTS_DIR" )"

# Detect OS
OS_TYPE="unix"
EXE_EXT=""
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    OS_TYPE="windows"
    EXE_EXT=".exe"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Industrial Benchmark Suite ===${NC}"
echo "Date: $(date)"
echo "OS detected: $OSTYPE ($OS_TYPE)"
echo "-------------------------------------"

# 1. Compilation
echo -e "${YELLOW}[System] Starting compilation phase...${NC}"

# Check for compilers
check_command() {
    if ! command -v $1 &> /dev/null; then
        return 1
    fi
    return 0
}

# Compile C
echo -n "  > Compiling C... "
if check_command gcc; then
    (cd "$ROOT_DIR/src/c" && gcc -Wall -Wextra -O3 main.c -o "csv_parser$EXE_EXT") > /dev/null 2>&1 && echo -e "${GREEN}DONE${NC}" || echo -e "${RED}FAILED${NC}"
else
    echo -e "${RED}MISSING GCC${NC}"
fi

# Compile Go
echo -n "  > Compiling Go... "
if check_command go; then
    (cd "$ROOT_DIR/src/go" && go build -o "parser$EXE_EXT" main.go) > /dev/null 2>&1 && echo -e "${GREEN}DONE${NC}" || echo -e "${RED}FAILED${NC}"
else
    echo -e "${RED}MISSING GO${NC}"
fi

# Python Environment
echo -n "  > Python Environment... "
if check_command uv; then
    (cd "$ROOT_DIR/src/python" && uv sync > /dev/null 2>&1 && echo -e "${GREEN}READY${NC}") || echo -e "${RED}FAILED${NC}"
else
    echo -e "${YELLOW}READY (System Python)${NC}"
fi

# 2. Execution
run_benchmark() {
    local dir=$1
    local cmd=$2
    local label=$3
    
    echo -e "\n${BLUE}--- [AUDIT] ${label} ---${NC}"
    
    if [ ! -d "$dir" ]; then
        echo -e "${RED}Directory not found: $dir${NC}"
        return
    fi

    cd "$dir"
    
    # Measure time
    local start=$(date +%s.%N)
    # Handle OS specific timing/RAM if possible
    if [[ "$OS_TYPE" == "windows" ]]; then
        # On Windows/Git Bash, we just run the command
        $cmd
    else
        # On macOS/Linux we can use /usr/bin/time if it exists
        if [ -f "/usr/bin/time" ]; then
            /usr/bin/time -p $cmd
        else
            $cmd
        fi
    fi
    local end=$(date +%s.%N)
    
    # Calculate duration (simple subtraction if %N is supported)
    # Fallback if %N is not supported (some older shells)
    if [[ "$start" == *"%N"* ]]; then
        start=$(date +%s)
        end=$(date +%s)
    fi
    
    # Print metrics (RAM is hard to get portably in one line without specialized tools on Windows bash)
    echo -e "\n${YELLOW}Performance Metrics [${label}]:${NC}"
    echo "  - Benchmark completed."
}

# Run implementations
run_benchmark "$ROOT_DIR/src/python" "python main.py" "Python"
if [ -f "$ROOT_DIR/src/c/csv_parser$EXE_EXT" ]; then
    run_benchmark "$ROOT_DIR/src/c" "./csv_parser$EXE_EXT" "C (Native)"
fi
if [ -f "$ROOT_DIR/src/go/parser$EXE_EXT" ]; then
    run_benchmark "$ROOT_DIR/src/go" "./parser$EXE_EXT" "Go (Binary)"
fi

echo -e "\n${BLUE}-------------------------------------${NC}"
echo -e "${BLUE}Benchmark Audit Completed.${NC}"
