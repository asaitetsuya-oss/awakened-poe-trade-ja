param([string]$RepoDir)
$f = "$RepoDir\renderer\src\web\Config.ts"
$c = ([IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))).ReadToEnd()

# language型定義にjaを追加（重複チェック）
if (-not $c.Contains("'ko' | 'ja'")) {
    $c = $c.Replace("language: 'en' | 'ru' | 'cmn-Hant' | 'ko'", "language: 'en' | 'ru' | 'cmn-Hant' | 'ko' | 'ja'")
    Write-Host "    Config.ts: language type ja added."
} else {
    Write-Host "    Config.ts: language type already has ja."
}

# overlayKeyのデフォルトをShift+F1に変更
$c = $c.Replace("overlayKey: 'Shift + Space'", "overlayKey: 'Shift + F1'")

# デフォルト言語をjaに変更
$c = $c.Replace("language: 'en',", "language: 'ja',")

# poeWebApiにjaのケースを追加（重複チェック）
if (-not $c.Contains("case 'ja': return 'www.pathofexile.com'")) {
    $c = $c.Replace(
        "    case 'ko': return 'poe.game.daum.net'",
        "    case 'ko': return 'poe.game.daum.net'`r`n    case 'ja': return 'www.pathofexile.com'"
    )
    Write-Host "    Config.ts: ja case added."
} else {
    Write-Host "    Config.ts: ja case already exists."
}

$_writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
$_writer.Write($c)
$_writer.Close()
Write-Host "    Done."
