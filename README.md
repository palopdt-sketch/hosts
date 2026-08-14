# hosts
hosts

python -m PyInstaller --noconsole --onefile --uac-admin  your_script.py

winget install ImageMagick.ImageMagick

magick appicon.png app.ico

python -m PyInstaller --noconsole --onefile --uac-admin --icon=app.ico localpy.py

##

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /v AllowDeletingBrowserHistory /t REG_DWORD /d 0 /f

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserAddPersonEnabled /t REG_DWORD /d 0

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserGuestModeEnabled  /t REG_DWORD /d 0

##

Remove-Item "$env:APPDATA\Microsoft\Windows\Recent\*" -Force -Recurse
