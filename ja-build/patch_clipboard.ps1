param([string]$RepoDir)
$f = "$RepoDir\main\src\shortcuts\HostClipboard.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)
if (-not $c.Contains("'ja'")) {
    $c = $c.Replace(
        "  lang: 'cmn-Hans',`r`n  firstLine: '物品类别: '`r`n}]",
        "  lang: 'cmn-Hans',`r`n  firstLine: '物品类别: '`r`n}, {`r`n  lang: 'ja',`r`n  firstLine: 'アイテムクラス: '`r`n}]")
    [IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
    Write-Host '    HostClipboard.ts: ja added.'
} else { Write-Host '    HostClipboard.ts: ja already exists.' }