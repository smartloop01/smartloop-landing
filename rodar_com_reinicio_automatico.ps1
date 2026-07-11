$ErrorActionPreference = "SilentlyContinue"

Set-Location $PSScriptRoot

$port = 8088
$watchedFiles = @(
    "main.py",
    "landing.py",
    "controls.py",
    "theme.py",
    "config.py",
    "lead_service.py"
)

function Stop-SmartLoopServer {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique

    foreach ($processId in $processIds) {
        if ($processId -and $processId -ne 0) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }

    if ($script:serverProcess -and -not $script:serverProcess.HasExited) {
        Stop-Process -Id $script:serverProcess.Id -Force -ErrorAction SilentlyContinue
    }
}

function Start-SmartLoopServer {
    Stop-SmartLoopServer
    $script:serverProcess = Start-Process `
        -FilePath "python" `
        -ArgumentList "main.py" `
        -WorkingDirectory $PSScriptRoot `
        -PassThru

    Start-Sleep -Seconds 2
    Write-Host ""
    Write-Host "SmartLoop rodando:" -ForegroundColor Green
    Write-Host "PC:     http://127.0.0.1:$port" -ForegroundColor Cyan
    Write-Host "iPhone: http://192.168.0.110:$port" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Quando salvar landing.py, o site reinicia sozinho." -ForegroundColor Yellow
    Write-Host "Para parar tudo, pressione Ctrl + C nesta janela." -ForegroundColor Yellow
}

function Get-LatestWriteTime {
    $latest = Get-Date "2000-01-01"

    foreach ($file in $watchedFiles) {
        if (Test-Path $file) {
            $writeTime = (Get-Item $file).LastWriteTime
            if ($writeTime -gt $latest) {
                $latest = $writeTime
            }
        }
    }

    return $latest
}

$lastWriteTime = Get-LatestWriteTime
Start-SmartLoopServer

try {
    while ($true) {
        Start-Sleep -Seconds 1
        $currentWriteTime = Get-LatestWriteTime

        if ($currentWriteTime -gt $lastWriteTime) {
            $lastWriteTime = $currentWriteTime
            Write-Host ""
            Write-Host "Arquivo salvo. Reiniciando SmartLoop..." -ForegroundColor Yellow
            Start-SmartLoopServer
        }
    }
}
finally {
    Stop-SmartLoopServer
}
