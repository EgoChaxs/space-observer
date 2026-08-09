$modelsDirectory = "assets/models"

$rfDetrDirectory = "$modelsDirectory/rf_detr_small"
$rfDetrWeights = "$rfDetrDirectory/rf-detr-small.pth"

$dinoDirectory = "$modelsDirectory/dinov2"
$dinoRequiredFiles = @(
    "config.json",
    "model.safetensors",
    "preprocessor_config.json"
)


function Initialize-ModelsDirectory {
    if (-not (Test-Path $modelsDirectory)) {
        Write-Host "Creating models directory..."
        New-Item -ItemType Directory -Path $modelsDirectory | Out-Null
    }
}


function Test-RFDETR {
    return Test-Path $rfDetrWeights
}


function Test-DINOv2 {
    if (-not (Test-Path $dinoDirectory)) {
        return $false
    }

    foreach ($file in $dinoRequiredFiles) {
        $filePath = Join-Path $dinoDirectory $file

        if (-not (Test-Path $filePath)) {
            return $false
        }
    }

    return $true
}


function Install-RFDETR {
    Write-Host ""
    Write-Host "RF-DETR Small is missing or incomplete."

    $choice = Read-Host "Download RF-DETR Small? (Y/N)"

    if ($choice -ne "Y" -and $choice -ne "y") {
        Write-Host "RF-DETR Small is required."
        exit 1
    }

    Write-Host "Downloading RF-DETR Small..."

    python scripts/helpers/download_models.py rfdetr

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to download RF-DETR Small."
        exit 1
    }

    if (-not (Test-RFDETR)) {
        Write-Host "RF-DETR download completed, but the model was not found."
        exit 1
    }

    Write-Host "RF-DETR Small installed successfully."
}


function Install-DINOv2 {
    Write-Host ""
    Write-Host "DINOv2 Small is missing or incomplete."

    $choice = Read-Host "Download DINOv2 Small? (Y/N)"

    if ($choice -ne "Y" -and $choice -ne "y") {
        Write-Host "DINOv2 Small is required."
        exit 1
    }

    Write-Host "Downloading DINOv2 Small..."

    python scripts/helpers/download_models.py dinov2

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to download DINOv2 Small."
        exit 1
    }

    if (-not (Test-DINOv2)) {
        Write-Host "DINOv2 download completed, but the model is incomplete."
        exit 1
    }

    Write-Host "DINOv2 Small installed successfully."
}


Initialize-ModelsDirectory

if (Test-RFDETR) {
    Write-Host "RF-DETR Small is already installed."
}
else {
    Install-RFDETR
}

if (Test-DINOv2) {
    Write-Host "DINOv2 Small is already installed."
}
else {
    Install-DINOv2
}

Write-Host ""
Write-Host "All required models are installed."
exit 0