$logFile = "C:\recent-clear.log"

# Function to log messages
function Log-Message {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "${timestamp}: $message"
    Add-Content -Path $logFile -Value $logEntry
}
try {
    # Log start of script
    Log-Message "Starting the script."

    # Clear Recent Items in File Explorer
    $recentItemsPath = [System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Recent')

    # Check if the Recent Items folder exists
    if (Test-Path $recentItemsPath) {
        Remove-Item "$recentItemsPath\*" -Force -Recurse -ErrorAction SilentlyContinue
        Log-Message "Cleared recent items in File Explorer."
    } else {
        Log-Message "Recent Items folder does not exist."
    }

    # Clear Recent Files in Windows Media Player
    $mediaPlayerRecentItemsPathLocal = [System.IO.Path]::Combine($env:LOCALAPPDATA, 'Packages\Microsoft.ZuneMusic_8wekyb3d8bbwe\LocalState')

    # Check if the Media Player Recent Items folder exists in Local folder
    if (Test-Path $mediaPlayerRecentItemsPathLocal) {
        # Remove the current database file, which includes recent file history
        Remove-Item "$mediaPlayerRecentItemsPathLocal\MediaPlayer.db-wal" -Force -ErrorAction SilentlyContinue
        Log-Message "Cleared all Media Player files."
    } else {
        Log-Message "Media Player folder does not exist."
    }
} catch {
    Log-Message "An error occurred: $_"
}

# Log end of script
Log-Message "Script completed."