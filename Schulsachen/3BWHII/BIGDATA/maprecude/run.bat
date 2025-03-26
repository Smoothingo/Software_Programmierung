@echo off
set /p input_file=Enter the input file name: 

set /p action=Do you want to (d)isplay the output or (s)ave it to a JSON file? 
if /i "%action%"=="d" (
    type %input_file% | python mapper.py | sort | python reducer.py
) else if /i "%action%"=="s" (
    type %input_file% | python mapper.py | sort | python reducer.py | python saver.py
    echo Output saved to output.json
) else (
    echo Invalid option. Please enter 'd' to display or 's' to save.
    exit /b 1
)
pause