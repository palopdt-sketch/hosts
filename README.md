# hosts
hosts

python -m PyInstaller --noconsole --onefile --uac-admin  your_script.py

python -m PyInstaller --clean --noconfirm --windowed --onefile --uac-admin --icon=app.ico --name=CasioCal casio_calculator.py

python -m PyInstaller --clean --noconfirm --windowed --onefile --add-data "app.png;." --uac-admin --icon=app.png --name=ManagerChungThu manager.py

winget install ImageMagick.ImageMagick

magick appicon.png app.ico

python -m PyInstaller --noconsole --onefile --uac-admin --icon=app.ico localpy.py

python -m PyInstaller --clean --noconfirm --noconsole --onefile --uac-admin --icon=appicon.ico --name=NhaTui localpy.py

python -m PyInstaller --noconsole --onefile --uac-admin --icon=app_icon_preview.png --exclude-module PyQt5 sharemonitor.py

##

reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome" /v AllowDeletingBrowserHistory /t REG_DWORD /d 0 /f

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserAddPersonEnabled /t REG_DWORD /d 0

##

REG ADD HKLM\SOFTWARE\Policies\Google\Chrome /v BrowserGuestModeEnabled  /t REG_DWORD /d 0

##

Remove-Item "$env:APPDATA\Microsoft\Windows\Recent\*" -Force -Recurse
