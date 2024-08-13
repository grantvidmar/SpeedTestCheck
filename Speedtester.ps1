#For this to work you will need to download the Ookla Speed Test CLI module from https://www.speedtest.net/apps/cli
#You will also need to extract it to c:\temp
# File to store the JSON results
$json_file = "speedtest_results.json" 

# Path to the Speedtest CLI executable
$speedtest_path = "c:\temp\speedtest.exe"  # Adjust if the filename is different

# Run for an hour (3600 seconds)
$end_time = [datetime]::Now.AddSeconds(3600)

# Create an empty array to store the results
$all_results = @() 

# Loop until the end time is reached
while ([datetime]::Now -lt $end_time) {
    $results = & $speedtest_path -f json-pretty  # Get results in json-pretty format
    $all_results += $results | ConvertFrom-Json  # Convert to object and add to array
    Start-Sleep -Seconds 10
}

# Convert the array of results back to JSON and save to file
$all_results | ConvertTo-Json -Depth 10 | Out-File $json_file 

# --- JSON to CSV Conversion ---

# Path to the output CSV file
$csv_file = "speedtest_results.csv"

# Extract only the necessary properties, convert bandwidth to Mbps, and create custom objects
$csv_data = $all_results | ForEach-Object {
    [PSCustomObject]@{
        'Timestamp' = $_.timestamp
        'Ping' = $_.ping.latency
        'Download (Mbps)' = [math]::Round( $_.download.bandwidth / 125000, 2)  # Convert to Mbps and round to 2 decimals
        'Upload (Mbps)' = [math]::Round( $_.upload.bandwidth / 125000, 2)   # Convert to Mbps and round to 2 decimals
    }
}

# Export the data to a CSV file
$csv_data | Export-Csv $csv_file -NoTypeInformation

Write-Host "Testing and conversion complete. Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 
