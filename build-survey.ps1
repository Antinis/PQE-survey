$ErrorActionPreference = 'Stop'

# Compile the complete project, including its chapter files and bibliography.
$latexmkCommand = Get-Command latexmk.exe -ErrorAction SilentlyContinue
if ($latexmkCommand) {
    $latexmkPath = $latexmkCommand.Source
} elseif (Test-Path -LiteralPath 'D:\texlive\bin\windows\latexmk.exe') {
    $latexmkPath = 'D:\texlive\bin\windows\latexmk.exe'
} else {
    throw 'latexmk was not found. Install TeX Live and add its bin directory to PATH.'
}

Push-Location $PSScriptRoot
try {
    & $latexmkPath -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
    if ($LASTEXITCODE -ne 0) {
        throw 'Compilation failed. See build/main.log for details.'
    }
    $pdfDirectory = Join-Path $PSScriptRoot 'output\pdf'
    New-Item -ItemType Directory -Path $pdfDirectory -Force | Out-Null
    $pdfPath = Join-Path $pdfDirectory 'survey.pdf'
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'build\main.pdf') -Destination $pdfPath -Force
    Write-Output "Compiled PDF: $pdfPath"
} finally {
    Pop-Location
}
