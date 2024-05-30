Function ConvertCurrency(currencyPair As String, conversionDate As String, amount As Double) As Variant
    Dim xml As Object
    Dim url As String
    Dim responseText As String
    Dim lines As Variant
    Dim line As String
    Dim parts As Variant
    Dim i As Integer
    Dim rate As Double
    Dim found As Boolean

    ' Error handling
    On Error GoTo ErrorHandler

    ' Validate conversionDate format
    If Not IsDate(conversionDate) Then
        ConvertCurrency = CVErr(xlErrValue)
        Exit Function
    End If

    ' Construct URL for fetching exchange rates
    url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=" & conversionDate

    ' Fetch data from URL
    Set xml = CreateObject("MSXML2.XMLHTTP")
    xml.Open "GET", url, False
    xml.send
    responseText = xml.responseText

    ' Check if responseText contains data
    If Len(responseText) = 0 Then
        ConvertCurrency = CVErr(xlErrValue)
        Exit Function
    End If

    ' Split response text into lines
    If InStr(responseText, vbCrLf) > 0 Then
        lines = Split(responseText, vbCrLf)
    ElseIf InStr(responseText, vbLf) > 0 Then
        lines = Split(responseText, vbLf)
    Else
        lines = Split(responseText, vbCr)
    End If

    found = False

    ' Loop through the lines skipping headers
    For i = 2 To UBound(lines)
        line = lines(i)
        If InStr(line, currencyPair) > 0 Then
            parts = Split(line, "|")
            If UBound(parts) >= 4 And parts(3) = Left(currencyPair, 3) Then
                rate = CDbl(parts(4))
                found = True
                Exit For
            End If
        End If
    Next i

    ' Return the conversion result
    If found Then
        ConvertCurrency = amount * rate
    Else
        ConvertCurrency = CVErr(xlErrNA)
    End If

    Exit Function

 ErrorHandler:
    ConvertCurrency = CVErr(xlErrValue)
End Function