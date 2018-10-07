' 
' Usage/sybtax: ZiraSpeaking.vbs <path to script file> 
' Note: to stop the script before it ends, use Task Manager to find "Microsoft ® Windows Based Script Host"
' or run "stopVBScript"
'

Option Explicit
Const ForReading = 1 
Dim msgs, Zira, id
Dim fso, scriptFilePath, args

Function AddItem(ByRef arr, val)
    ReDim Preserve arr(UBound(arr) + 1)
    arr(UBound(arr)) = val
End Function

Function readFileAsArray(ByVal scriptFilePath)
	Dim msgs, fso, objTextFile, strNextLine
	msgs = Array()
	Set fso = CreateObject("Scripting.FileSystemObject") 
	Set objTextFile = fso.OpenTextFile(scriptFilePath, ForReading) 

	Do Until objTextFile.AtEndOfStream 
		strNextLine = trim(objTextFile.Readline)
		If strNextLine <> "" Then
			AddItem msgs, strNextLine
		End If
	Loop 	
	readFileAsArray = msgs
End Function

Set args = Wscript.Arguments
Set fso = CreateObject("Scripting.FileSystemObject")
scriptFilePath = fso.GetAbsolutePathName(args(0))
msgs = readFileAsArray(scriptFilePath)

Set Zira = CreateObject("sapi.spvoice")
Set Zira.Voice = Zira.GetVoices.Item(1)

For id = 0 to uBound(msgs)
	If IsNumeric(msgs(id)) Then
	    WScript.Sleep msgs(id)
	Else
		Zira.Speak msgs(id)
	End If
Next
