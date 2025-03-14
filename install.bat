@echo off
setlocal

:: Get the correct username
set "USERNAME=%USERNAME%"

:: Define the destination path
set "DEST=C:\Users\%USERNAME%\AppData\Local\Programs\Python\create"

:: Create the destination folder if it doesn't exist
if not exist "%DEST%" mkdir "%DEST%"

:: Create an exclusion file for xcopy
(
    echo .git
    echo .gitignore
    echo .venv
    echo install.bat
    echo exclude.txt
    echo readme.md
) > exclude.txt

:: Copy all files from the current directory to the destination folder
echo Copying files...
xcopy "." "%DEST%" /E /I /H /EXCLUDE:exclude.txt

:: Check if the copying was successful
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to copy files.
    pause
    exit /b 1
)

:: Rename main.py to create.py in the destination folder
if exist "%DEST%\main.py" (
    ren "%DEST%\main.py" "create.py"
    echo Renamed main.py to create.py
)

:: Remove the temporary exclusion file
del exclude.txt

:: Navigate to the destination folder
cd /d "%DEST%"

:: Install required packages
if exist requirements.txt (
    echo Installing packages...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found, skipping package installation.
)

:: Check if the destination path is already in the PATH variable
echo %PATH% | find /I "%DEST%" >nul
if errorlevel 1 (
    echo Setting environment variable...
    :: Get the existing PATH without breaking on special characters
    for /f "tokens=*" %%p in ('powershell -Command "[System.Environment]::GetEnvironmentVariable('PATH', 'User')"') do set "TRIMMED_PATH=%%p"
    :: Trim the path to the first 900 characters to make room
    set "TRIMMED_PATH=%TRIMMED_PATH:~0,900%"
    setx PATH "%TRIMMED_PATH%;%DEST%"
) else (
    echo Path already exists in the environment variable.
)

:: Add .py to PATHEXT if not already present
echo Modifying PATHEXT...
echo %PATHEXT% | find /I ".py" >nul
if errorlevel 1 (
    setx PATHEXT "%PATHEXT%;.py"
) else (
    echo .py already exists in PATHEXT
)

echo Installation completed successfully!
pause
endlocal
