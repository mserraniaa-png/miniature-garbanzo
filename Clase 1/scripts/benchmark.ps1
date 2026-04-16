# Rigorous Benchmark Suite for CSV Parsing (Windows Version)
# Author: Antigravity for Dr. Fuentes
# OS: Windows

$ScriptsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptsDir

# Colors
$Blue = "`e[94m"
$Green = "`e[92m"
$Red = "`e[91m"
$Yellow = "`e[93m"
$NC = "`e[0m"

Write-Host "${Blue}=== Industrial Benchmark Suite (Windows) ===${NC}"
Write-Host "Date: $(Get-Date)"
Write-Host "-------------------------------------"

# 1. Compilation
Write-Host "${Yellow}[System] Starting compilation phase...${NC}"

# Compiling C
Write-Host -NoNewline "  > Compiling C... "
if (Get-Command gcc -ErrorAction SilentlyContinue) {
    Set-Location "$RootDir\src\c"
    # Clean and Compile
    if (Test-Path .\csv_parser.exe) { Remove-Item .\csv_parser.exe }
    $compileResult = gcc -Wall -Wextra -O3 main.c -o csv_parser.exe 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Host "${Green}DONE${NC}" } else { Write-Host "${Red}FAILED${NC}" }
} else {
    Write-Host "${Red}MISSING GCC${NC}"
}

# Compiling Go
Write-Host -NoNewline "  > Compiling Go... "
if (Get-Command go -ErrorAction SilentlyContinue) {
    Set-Location "$RootDir\src\go"
    $compileResult = go build -o parser.exe main.go 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Host "${Green}DONE${NC}" } else { Write-Host "${Red}FAILED${NC}" }
} else {
    Write-Host "${Red}MISSING GO${NC}"
}

# Python Environment
Write-Host -NoNewline "  > Python Environment... "
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Set-Location "$RootDir\src\python"
    $envResult = uv sync 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Host "${Green}READY${NC}" } else { Write-Host "${Red}FAILED${NC}" }
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "${Yellow}READY (System Python)${NC}"
} else {
    Write-Host "${Red}MISSING PYTHON${NC}"
}

# 2. Execution logic
function Run-Benchmark($dir, $bin, $label) {
    Write-Host "`n${Blue}--- [AUDIT] $label ---${NC}"
    
    if (-not (Test-Path $dir)) {
        Write-Host "${Red}Directory not found: $dir${NC}"
        return
    }

    Set-Location $dir
    
    # Split bin into command and arguments
    $parts = $bin -split " "
    $cmd = $parts[0]
    $args = $parts[1..($parts.Length-1)]

    # Measure time and memory
    try {
        $startTime = Get-Date
        $process = Start-Process -FilePath $cmd -ArgumentList $args -NoNewWindow -PassThru -Wait -ErrorAction Stop
        $endTime = Get-Date
        
        $duration = ($endTime - $startTime).TotalSeconds
        # Peak Working Set is a decent proxy for Max RSS on Windows
        $maxRssMiB = [Math]::Round($process.PeakWorkingSet64 / 1MB, 2)
        
        Write-Host "`n${Yellow}Performance Metrics [$label]:${NC}"
        Write-Host "  - Time: $($duration.ToString("F3"))s | RAM: $maxRssMiB MiB"
    } catch {
        Write-Host "${Red}Error running $label : $($_.Exception.Message)${NC}"
    }
}

# Run implementations
Run-Benchmark "$RootDir\src\python" "python main.py" "Python (Native)"
if (Test-Path "$RootDir\src\c\csv_parser.exe") {
    Run-Benchmark "$RootDir\src\c" ".\csv_parser.exe" "C (Native)"
}
if (Test-Path "$RootDir\src\go\parser.exe") {
    Run-Benchmark "$RootDir\src\go" ".\parser.exe" "Go (Binary)"
}

Write-Host "`n${Blue}-------------------------------------${NC}"
Write-Host "${Blue}Benchmark Audit Completed.${NC}"
