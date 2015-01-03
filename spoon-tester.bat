SETLOCAL enabledelayedexpansion
echo starting selenium-grid
spoon try -d base,spoonbrew/selenium-grid hub

rem todo: wait until the grid starts

echo executing tests

set final_errorlevel=0
for /f "delims=" %%f in ('dir .\tests /b /a-d-h-s') do (
	spoon try -a base,python python-tester.bat .\tests\%%f > .\results\%%f.log
	if !errorlevel! neq 0 (
		set final_errorlevel=!errorlevel!
		echo %%f failed with error code: !final_errorlevel!
		goto cleanup
	)
)

echo tests ran successfully!

:cleanup
spoon stop -a
exit /b %final_errorlevel%
ENDLOCAL
