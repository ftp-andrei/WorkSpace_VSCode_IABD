# Define the file path and size
$filePath = "E:\Rafa\BDA\Tema 3\Hadoop\data\data.txt"
$fileSizeMB = 600
$fileSizeBytes = $fileSizeMB * 1MB

# Create a file with the specified size
$buffer = New-Object byte[] (1MB)
$random = New-Object Random

# Open a file stream
$fileStream = [System.IO.File]::OpenWrite($filePath)

try {
    for ($i = 0; $i -lt $fileSizeMB; $i++) {
        $random.NextBytes($buffer)
        $fileStream.Write($buffer, 0, $buffer.Length)
    }
} finally {
    $fileStream.Close()
}

Write-Output "File of size $fileSizeMB MB created at $filePath"