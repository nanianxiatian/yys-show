' YYS Guess System - Silent Startup
' Services run in background without CMD windows

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Get current directory
strPath = FSO.GetParentFolderName(WScript.ScriptFullName)

' Show startup message
MsgBox "Starting YYS Guess System..." & vbCrLf & vbCrLf & _
       "Backend: http://localhost:5000" & vbCrLf & _
       "Frontend: http://localhost:5173" & vbCrLf & vbCrLf & _
       "Click OK to start services." & vbCrLf & _
       "Please wait 10 seconds before accessing.", _
       vbInformation, "YYS Guess System"

' Build backend command
backendPath = strPath & "\backend"
backendCmd = "cmd /c cd /d " & Chr(34) & backendPath & Chr(34) & " && call venv\Scripts\activate && python run.py"

' Start backend service (hidden window)
WshShell.Run backendCmd, 0, False

' Wait for backend to start
WScript.Sleep 5000

' Build frontend command
frontendPath = strPath & "\frontend"
frontendCmd = "cmd /c cd /d " & Chr(34) & frontendPath & Chr(34) & " && npm run dev"

' Start frontend service (hidden window)
WshShell.Run frontendCmd, 0, False

' Wait for frontend to start
WScript.Sleep 5000

' Open browser
WshShell.Run "http://localhost:5173", 1, False

' Show success message
MsgBox "Services started!" & vbCrLf & vbCrLf & _
       "Backend: http://localhost:5000" & vbCrLf & _
       "Frontend: http://localhost:5173" & vbCrLf & vbCrLf & _
       "Browser opened automatically." & vbCrLf & _
       "To stop services, run stop.bat or use Task Manager.", _
       vbInformation, "YYS Guess System - Running"

Set WshShell = Nothing
Set FSO = Nothing
