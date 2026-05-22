param([string]$RepoDir)

# main/package.json のリポジトリURLを自分のリポジトリに変更
$f = "$RepoDir\main\package.json"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)

if ($c.Contains('asaitetsuya-oss/awakened-poe-trade-ja')) {
    Write-Host "    package.json: repository already patched."
} else {
    $c = $c -replace '"repository":\s*"[^"]*"', '"repository": "https://github.com/asaitetsuya-oss/awakened-poe-trade-ja"'
    [IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
    Write-Host "    package.json: repository URL patched."
}

Write-Host "    Done."
