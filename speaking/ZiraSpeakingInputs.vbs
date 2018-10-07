Option Explicit
Dim msg, Zira
Do
	msg = InputBox("Enter your text for conversion: For Ex. MissingCube","MissingCube: Text2Speech Converter")
	Set Zira = CreateObject("sapi.spvoice")
	Set Zira.Voice = Zira.GetVoices.Item(1)
	Zira.Speak msg
Loop Until msg = ""
