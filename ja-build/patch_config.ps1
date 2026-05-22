param([string]$RepoDir)
$f = "$RepoDir\renderer\src\web\Config.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)

# language型定義にjaを追加（重複チェック）
if ($c -notmatch "language: 'en' \| 'ru' \| 'cmn-Hant' \| 'ko' \| 'ja'[^|]") {
    $c = $c.Replace("language: 'en' | 'ru' | 'cmn-Hant' | 'ko'", "language: 'en' | 'ru' | 'cmn-Hant' | 'ko' | 'ja'")
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
}

[IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
Write-Host '    Done.'
