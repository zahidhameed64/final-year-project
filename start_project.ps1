# Check for dataset
if (-not (Test-Path "Global YouTube Statistics.csv")) {
    Write-Host "Error: 'Global YouTube Statistics.csv' not found in the root directory." -ForegroundColor Red
    Write-Host "Please place the dataset file in the root directory before running this script."
    exit 1
}

# --- PORT CLEANUP ---
# Function to kill process by port
function Kill-PortOwner {
    param([int]$Port)
    $tcp = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($tcp) {
        Write-Host "Port $Port is in use. Attempting to stop owning process..." -ForegroundColor Yellow
        foreach ($conn in $tcp) {
            try {
                $proc = Get-Process -Id $conn.OwningProcess -ErrorAction Stop
                Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
                Write-Host "Stopped process $($proc.ProcessName) (PID: $($conn.OwningProcess))." -ForegroundColor Green
            } catch {
                # Process might have already closed or access denied
            }
        }
        Start-Sleep -Seconds 2
    }
}

Write-Host "Cleaning up ports 3000 (Frontend) and 5000 (Backend)..." -ForegroundColor Cyan
Kill-PortOwner 3000
Kill-PortOwner 5000

Write-Host "Starting Project Setup..." -ForegroundColor Green

# --- DETECT PYTHON EXECUTABLE ---
$pythonPath = "python" # Default
# Check if python is in PATH
try {
    $null = Get-Command "python" -ErrorAction Stop
    $pythonPath = "python"
    Write-Host "Found Python in PATH." -ForegroundColor Cyan
}
catch {
    # If not in PATH, try the known Anaconda path from user logs
    $anacondaPath = "C:\Users\A C\anaconda3\python.exe"
    if (Test-Path $anacondaPath) {
        $pythonPath = $anacondaPath
        Write-Host "Found Python at: $anacondaPath" -ForegroundColor Cyan
    }
    else {
        Write-Host "Error: Python not found in PATH and Anaconda path '$anacondaPath' does not exist." -ForegroundColor Red
        Write-Host "Please ensure Python is installed and added to your PATH, or update this script with the correct path." 
        exit 1
    }
}

# 1. Install Backend Dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
if (-not (Test-Path "backend/requirements.txt")) {
    Write-Host "Error: backend/requirements.txt not found." -ForegroundColor Red
    exit 1
}

# Use python -m pip to ensure we use the pip associated with the found python
& $pythonPath -m pip install -r backend/requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Python dependencies." -ForegroundColor Red
    exit 1
}

# 2. Install Frontend Dependencies
Write-Host "Installing Frontend dependencies..." -ForegroundColor Cyan
Push-Location frontend
if (-not (Test-Path "package.json")) {
    Write-Host "Error: frontend/package.json not found." -ForegroundColor Red
    Pop-Location
    exit 1
}
# Check for npm
try {
    $null = Get-Command "npm" -ErrorAction Stop
}
catch {
    Write-Host "Error: 'npm' is not recognized. Please install Node.js." -ForegroundColor Red
    Pop-Location
    exit 1
}

npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Node dependencies." -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# 3. Start Backend
Write-Host "Starting Flask Backend on Port 5000..." -ForegroundColor Green
# Start in a new window to keep running
$backendProcess = Start-Process $pythonPath -ArgumentList "backend/app.py" -PassThru

# Wait a bit for backend to initialize
Start-Sleep -Seconds 5

# 4. Start Frontend
Write-Host "Starting Next.js Frontend on Port 3000..." -ForegroundColor Green
Push-Location frontend
# Start in the CURRENT window so the user can see frontend logs/errors directly
npm run dev
Pop-Location

