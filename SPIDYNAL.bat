@echo off
SETLOCAL EnableDelayedExpansion

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer with error checking
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe'}" 2>errorlog.txt
    IF !ERRORLEVEL! NEQ 0 (
        set /p ERRORMSG=<errorlog.txt
        echo Download failed due to: !ERRORMSG!
        :python_retry_prompt
        set "CHOICE="
        set /p CHOICE="Retry download? (y/n): "
        if /i "!CHOICE!"=="y" (
            powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe'}" 2>errorlog.txt
            IF !ERRORLEVEL! NEQ 0 (
                set /p ERRORMSG=<errorlog.txt
                echo Download failed again due to: !ERRORMSG!
                goto python_retry_prompt
            )
        ) else if /i "!CHOICE!"=="n" (
            echo Canceling Python installation...
            del errorlog.txt 2>nul
            exit /b 1
        ) else (
            echo Invalid input. Please enter 'y' or 'n'.
            goto python_retry_prompt
        )
    )
    del errorlog.txt 2>nul

    :: Install Python silently and add to PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    IF %ERRORLEVEL% NEQ 0 (
        echo Python installation failed with error code: %ERRORLEVEL%
        :install_retry_prompt
        set "CHOICE="
        set /p CHOICE="Retry installation? (y/n): "
        if /i "!CHOICE!"=="y" (
            python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
            IF !ERRORLEVEL! NEQ 0 (
                echo Installation failed again with error code: !ERRORLEVEL!
                goto install_retry_prompt
            )
        ) else if /i "!CHOICE!"=="n" (
            echo Canceling Python installation...
            del python_installer.exe 2>nul
            exit /b 1
        ) else (
            echo Invalid input. Please enter 'y' or 'n'.
            goto install_retry_prompt
        )
    )
    
    :: Delete installer after installation
    del python_installer.exe 2>nul

    :: Refresh environment variables
    setx PATH "%PATH%;C:\Python312\Scripts;C:\Python312"
    
    echo Python installed successfully. Restarting the script...
    start "" "%~f0"
    exit /b
)

:: Install required Python libraries with error checking
echo Installing required Python libraries...

:: Upgrade pip
python -m pip install --upgrade pip 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to upgrade pip due to: !ERRORMSG!
    :pip_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry upgrading pip? (y/n): "
    if /i "!CHOICE!"=="y" (
        python -m pip install --upgrade pip 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto pip_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping pip upgrade...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto pip_retry_prompt
    )
)
del errorlog.txt 2>nul

:: Install psutil
pip install psutil 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to install psutil due to: !ERRORMSG!
    :psutil_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry installing psutil? (y/n): "
    if /i "!CHOICE!"=="y" (
        pip install psutil 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto psutil_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping psutil installation...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto psutil_retry_prompt
    )
)
del errorlog.txt 2>nul

:: Install pygame
pip install pygame 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to install pygame due to: !ERRORMSG!
    :pygame_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry installing pygame? (y/n): "
    if /i "!CHOICE!"=="y" (
        pip install pygame 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto pygame_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping pygame installation...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto pygame_retry_prompt
    )
)
del errorlog.txt 2>nul

:: Install colorama
pip install colorama 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to install colorama due to: !ERRORMSG!
    :colorama_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry installing colorama? (y/n): "
    if /i "!CHOICE!"=="y" (
        pip install colorama 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto colorama_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping colorama installation...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto colorama_retry_prompt
    )
)
del errorlog.txt 2>nul

:: Install termcolor
pip install termcolor 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to install termcolor due to: !ERRORMSG!
    :termcolor_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry installing termcolor? (y/n): "
    if /i "!CHOICE!"=="y" (
        pip install termcolor 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto termcolor_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping termcolor installation...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto termcolor_retry_prompt
    )
)
del errorlog.txt 2>nul

<<<<<<< Updated upstream:SPIDYNAL.bat
<<<<<<< Updated upstream:SPIDYNAL.bat
<<<<<<< Updated upstream:SPIDYNAL.bat
:: Close the current CMD window and open a new one in maximized mode
=======
=======
>>>>>>> Stashed changes:build/spidy/mound/spidy.bat
=======
>>>>>>> Stashed changes:build/spidy/mound/spidy.bat
:: Install speedtest-cli
pip install speedtest-cli 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo Failed to install speedtest-cli due to: !ERRORMSG!
    :speedtest_retry_prompt
    set "CHOICE="
    set /p CHOICE="Retry installing speedtest-cli? (y/n): "
    if /i "!CHOICE!"=="y" (
        pip install speedtest-cli 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo Failed again due to: !ERRORMSG!
            goto speedtest_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo Skipping speedtest-cli installation...
    ) else (
        echo Invalid input. Please enter 'y' or 'n'.
        goto speedtest_retry_prompt
    )
)
del errorlog.txt 2>nul

:: Launch spidy.py in Windows Terminal maximized
>>>>>>> Stashed changes:build/spidy/mound/spidy.bat
echo Starting SPIDYNAL...
start /max cmd /k "python build/spidy/mound/spidy.py"
exit