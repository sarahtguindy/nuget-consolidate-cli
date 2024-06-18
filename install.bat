@echo off
set URL=https://github.com/sarahtguindy/nuget-consolidate-cli/releases/download/v1.0.0/nuget-consolidate.exe
set DEST=%ProgramFiles%\NugetConsolidate\nuget-consolidate.exe

echo Downloading nuget-consolidate...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%URL%', '%DEST%')"

if %errorlevel% neq 0 (
    echo Error: Failed to download file.
    exit /b %errorlevel%
)

setx PATH "%PATH%;%ProgramFiles%\NugetConsolidate"
echo Installation for 'nuget-consolidate' complete.