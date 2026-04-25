# hosts
hosts
pyinstaller --noconsole --onefile --uac-admin your_script.py

##

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /v AllowDeletingBrowserHistory /t REG_DWORD /d 0 /f

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserAddPersonEnabled /t REG_DWORD /d 0

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserGuestModeEnabled  /t REG_DWORD /d 0

