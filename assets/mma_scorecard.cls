VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "mma_scorecard"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Sub ProcessData()
    Dim wbSource As Workbook
    Dim wsSource As Worksheet
    Dim wbTarget As Workbook
    Dim wsTarget As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim j As Long
    Dim targetFile As String
    Dim targetFolder As String

    ' Get the path of the MMA Scorecard file
    Dim scorecardPath As String
    scorecardPath = ThisWorkbook.Path & "\MMA_Scorecard_Felucha_2025.xlsm"  ' Adjust if different
    
    Set wbTarget = Workbooks.Open(scorecardPath)
    
    ' Get the path of the Fightcard file
    Dim fightcardPath As String
    fightcardPath = ThisWorkbook.Path & "\Fightcard.xlsx"  ' Adjust if different
    
    ' Create the subfolder
    targetFolder = ThisWorkbook.Path & "\Scorecard_Output\"
    MkDir targetFolder

    ' Open source and target workbooks
    Set wbSource = Workbooks.Open(fightcardPath)
    Set wbTarget = Workbooks.Open(scorecardPath)

    ' Set target worksheet (assuming Sheet1)
    Set wsTarget = wbTarget.Sheets("Sheet1")
        
    ' Find the last row in the source data
    With wbSource.Sheets("Sheet1")
        lastRow = .Cells(Rows.Count, 1).End(xlUp).Row
    End With

    ' Loop through each row in the source data
    For i = 2 To lastRow
    
        ' Copy data to specific cells
        wsTarget.Range("F2").Value = wbSource.Sheets("Sheet1").Cells(i, 1).Value
        wsTarget.Range("N2").Value = wbSource.Sheets("Sheet1").Cells(i, 1).Value
        wsTarget.Range("V2").Value = wbSource.Sheets("Sheet1").Cells(i, 1).Value
        wsTarget.Range("A4").Value = wbSource.Sheets("Sheet1").Cells(i, 2).Value
        wsTarget.Range("I4").Value = wbSource.Sheets("Sheet1").Cells(i, 2).Value
        wsTarget.Range("Q4").Value = wbSource.Sheets("Sheet1").Cells(i, 2).Value
        wsTarget.Range("F4").Value = wbSource.Sheets("Sheet1").Cells(i, 3).Value
        wsTarget.Range("N4").Value = wbSource.Sheets("Sheet1").Cells(i, 3).Value
        wsTarget.Range("V4").Value = wbSource.Sheets("Sheet1").Cells(i, 3).Value

        ' Save a copy of the Scorecard
        targetFile = targetFolder & "Scorecard_" & i - 1 & ".xlsm"
        wbTarget.SaveAs Filename:=targetFile, FileFormat:=xlOpenXMLWorkbookMacroEnabled

        ' Clear target worksheet for next iteration (optional)
        ' wsTarget.Cells.ClearContents

    Next i


    ' Close workbooks
    wbSource.Close
    wbTarget.Close SaveChanges:=False


    MsgBox "All Scorecard files created in: " & targetFolder

Exit Sub
ErrorHandler:
    MsgBox "An error occurred: " & Err.Description
End Sub

Sub PrintAllFilesInFolder()
    Dim fso As Object ' Defines the filesystem object
    Dim folder As Object
    Dim file As Object
    Dim wb As Workbook

    ' Folder path (replace with your actual folder path)
    Dim folderPath As String
    folderPath = ThisWorkbook.Path & "\Scorecard_Output\"

    Set fso = CreateObject("Scripting.FileSystemObject")
    Set folder = fso.GetFolder(folderPath)

    For Each file In folder.Files
        On Error Resume Next ' Ignore errors if file cannot be opened as Excel
        Set wb = Workbooks.Open(file.Path)
        wb.PrintOut
        wb.Close SaveChanges:=False
        On Error GoTo 0
    Next file

    MsgBox "All files processed."
End Sub

