param([string]$RepoDir)
$f = "$RepoDir\renderer\src\web\Config.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)

# language型定義にjaを追加（複数パターン対応・重複チェック）
if ($c.Contains("| 'ja'") -or $c.Contains('| "ja"')) {
    Write-Host "    Config.ts: language type already has ja."
} elseif ($c.Contains("'en' | 'ru' | 'cmn-Hant' | 'ko'")) {
    $c = $c.Replace("language: 'en' | 'ru' | 'cmn-Hant' | 'ko'", "language: 'en' | 'ru' | 'cmn-Hant' | 'ko' | 'ja'")
    Write-Host "    Config.ts: language type ja added (with ko)."
} elseif ($c.Contains("'en' | 'ru' | 'cmn-Hant'")) {
    $c = $c.Replace("language: 'en' | 'ru' | 'cmn-Hant'", "language: 'en' | 'ru' | 'cmn-Hant' | 'ja'")
    Write-Host "    Config.ts: language type ja added (without ko)."
} else {
    Write-Host "    [WARN] Config.ts: language type pattern not found. Manual fix may be needed."
}

# overlayKeyのデフォルトをShift+F1に変更
$c = $c.Replace("overlayKey: 'Shift + Space'", "overlayKey: 'Shift + F1'")

# デフォルト言語をjaに変更
$c = $c.Replace("language: 'en',", "language: 'ja',")

# poeWebApiにjaのケースを追加（複数パターン対応・重複チェック）
if ($c.Contains("case 'ja':")) {
    Write-Host "    Config.ts: ja case already exists."
} elseif ($c.Contains("case 'ko': return 'poe.game.daum.net'")) {
    $c = $c.Replace(
        "    case 'ko': return 'poe.game.daum.net'",
        "    case 'ko': return 'poe.game.daum.net'`r`n    case 'ja': return 'www.pathofexile.com'"
    )
    Write-Host "    Config.ts: ja case added (after ko)."
} elseif ($c.Contains("case 'cmn-Hant':")) {
    # koがない場合はcmn-Hantの後に追加
    $c = $c -replace "(case 'cmn-Hant':[^\n]+)", "`$1`r`n    case 'ja': return 'www.pathofexile.com'"
    Write-Host "    Config.ts: ja case added (after cmn-Hant)."
} else {
    Write-Host "    [WARN] Config.ts: poeWebApi pattern not found. Manual fix may be needed."
}

[IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
Write-Host "    Done."
