param([string]$RepoDir)

# main/package.json のリポジトリURLを自分のリポジトリに変更
$f = "$RepoDir\main\package.json"

# BOMなしUTF-8で読み書きするためStreamReaderを使用
$reader = [IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))
$c = $reader.ReadToEnd()
$reader.Close()

if ($c.Contains('asaitetsuya-oss/awakened-poe-trade-ja')) {
    Write-Host "    package.json: repository already patched."
} else {
    $c = $c -replace '"repository":\s*"[^"]*"', '"repository": "https://github.com/asaitetsuya-oss/awakened-poe-trade-ja"'
    $writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
    $writer.Write($c)
    $writer.Close()
    Write-Host "    package.json: repository URL patched."
}

Write-Host "    Done."
