@echo off
:menu
cls
echo.
echo 1. Process GCAG data
echo 2. Process GISTEMP data
echo 3. Plot from existing JSON file
echo 4. Exit
echo.
set /p choice=Choose an option (1-4): 

if "%choice%"=="1" (
    set source=gcag
    call :process
    goto menu
) else if "%choice%"=="2" (
    set source=gistemp
    call :process
    goto menu
) else if "%choice%"=="3" (
    call :plot
    goto menu
) else if "%choice%"=="4" (
    exit /b
) else (
    echo Invalid choice. Please try again.
    pause
    goto menu
)

:process
cls
echo.
echo 1. Display results
echo 2. Save to JSON
echo 3. Save and plot
echo 4. Back to main menu
echo.
set /p action=Choose action (1-4): 

if "%action%"=="1" (
    type monthly.csv | python mapper.py --source %source% | sort | python reducer.py
    pause
    goto :eof
) else if "%action%"=="2" (
    type monthly.csv | python mapper.py --source %source% | sort | python reducer.py | python saver.py > output.json
    echo Data saved to output.json
    pause
    goto :eof
) else if "%action%"=="3" (
    type monthly.csv | python mapper.py --source %source% | sort | python reducer.py | python saver.py > output.json
    python plotter.py output.json
    pause
    goto :eof
) else if "%action%"=="4" (
    goto :eof
) else (
    echo Invalid choice. Please try again.
    pause
    goto process
)

:plot
cls
set /p filename=Enter JSON filename (e.g. output.json): 
python plotter.py "%filename%"
pause
goto :eof