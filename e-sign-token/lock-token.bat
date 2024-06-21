REM del C:\Users\MaxVN\AppData\Local\e-sign-token\lock.txt

taskkill /IM "chrome.exe" /F
taskkill /IM "msedge.exe" /F
taskkill /IM "ecussign_pro.exe" /F
taskkill /IM "ffmpeg.exe" /F

REM taskkill /IM "UltraViewer_Desktop.exe" /F
REM start "" "C:\Program Files (x86)\UltraViewer\UltraViewer_Desktop.exe"

C:\Windows\System32\rundll32.exe user32.dll, LockWorkStation