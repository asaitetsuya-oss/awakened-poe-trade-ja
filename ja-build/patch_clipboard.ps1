param([string]$RepoDir)
$f = "$RepoDir\main\src\shortcuts\HostClipboard.ts"
$c = ([IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))).ReadToEnd()
if (-not $c.Contains("'ja'")) {
    $c = $c.Replace(
        "  lang: 'cmn-Hans',`r`n  firstLine: '物品类别: '`r`n}]",
        "  lang: 'cmn-Hans',`r`n  firstLine: '物品类别: '`r`n}, {`r`n  lang: 'ja',`r`n  firstLine: 'アイテムクラス: '`r`n}]")
    $_writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
    $_writer.Write($c)
    $_writer.Close()
    Write-Host '    HostClipboard.ts: ja added.'
} else { Write-Host '    HostClipboard.ts: ja already exists.' }