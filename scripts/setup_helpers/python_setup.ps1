$requiredPythonVersion = [version]"3.14"

$isPythonInstalled = [bool](Get-Command python -ErrorAction SilentlyContinue)

if ($isPythonInstalled) {
    $pythonVersionOutput = python --version 2>&1
    $pythonVersion = [version](($pythonVersionOutput -replace 'Python ', '').Trim())

    Write-Host "Python version detected: $pythonVersion"

    if ($pythonVersion -lt $requiredPythonVersion) {
        Write-Host ""
        Write-Host "Your Python version is too old."
        Write-Host "Space Observer requires Python $requiredPythonVersion or newer."
        Write-Host ""

        $choice = Read-Host "Would you like to open the Python download page? (Y/N)"

        if ($choice -eq "Y" -or $choice -eq "y") {
            Start-Process "https://www.python.org/downloads/"
        }

        exit 1
    }

    Write-Host "Python version is compatible."
}
else {
    Write-Host "Python is not installed."
    Write-Host "Space Observer requires Python $requiredPythonVersion or newer."
    Write-Host ""

    $choice = Read-Host "Would you like to open the Python download page? (Y/N)"

    if ($choice -eq "Y" -or $choice -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }

    exit 1
}