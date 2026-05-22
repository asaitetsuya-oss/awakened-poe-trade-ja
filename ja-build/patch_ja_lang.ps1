param([string]$RepoDir)

# client-log.ts: ja エントリを追加
$f = "$RepoDir\renderer\src\web\client-log\client-log.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)

# 壊れたパターンをクリーンアップ（前回のパッチが誤って挿入した場合）
$c = $c -replace "\}\s*'ja': /\^Hi, I would like[^\n]+\n\}\}", "}"

# TRADE_WHISPER に ja を追加（cmn-Hant の前に挿入）
if (-not $c.Contains("'ja': /^Hi, I would like")) {
    $jaLine = "  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \(stash tab ""(?<tab_name>.*)""; position: left (?<tab_left>\d+), top (?<tab_top>\d+)\)(?<message>.+)?`$/,"
    $c = $c.Replace("  'cmn-Hant': /^你好，我想購買", "$jaLine`r`n  'cmn-Hant': /^你好，我想購買")
    Write-Host '    TRADE_WHISPER ja added.'
} else { Write-Host '    TRADE_WHISPER ja already exists or not needed.' }

# TRADE_BULK_WHISPER に ja を追加
if (-not $c.Contains("'ja': /^Hi, I'd like")) {
    $jaBulkLine = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\.(?<message>.+)?`$/,"
    $c = $c.Replace("  'ko': /^_FIX_ME_`$/`r`n}", "  'ko': /^_FIX_ME_`$/,`r`n$jaBulkLine`r`n}")
    Write-Host '    TRADE_BULK_WHISPER ja added.'
} else { Write-Host '    TRADE_BULK_WHISPER ja already exists or not needed.' }

[IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)

# hotkeyable-actions.ts: POEDB_LANGS に ja を追加
$f2 = "$RepoDir\renderer\src\web\item-check\hotkeyable-actions.ts"
$c2 = [IO.File]::ReadAllText($f2, [Text.Encoding]::UTF8)
if ($c2.Contains("'ko': 'kr'") -and -not $c2.Contains("'ja':")) {
    $c2 = $c2.Replace("'ko': 'kr' }", "'ko': 'kr', 'ja': 'us' }")
    Write-Host '    POEDB_LANGS ja added.'
} else { Write-Host '    POEDB_LANGS ja already exists.' }
[IO.File]::WriteAllText($f2, $c2, [Text.Encoding]::UTF8)

# make-index-files.mjs: LANGUAGES に ja を追加
$f3 = "$RepoDir\renderer\src\assets\make-index-files.mjs"
$c3 = [IO.File]::ReadAllText($f3, [Text.Encoding]::UTF8)
if (-not $c3.Contains("'ja'")) {
    $c3 = $c3.Replace("const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko']", "const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko', 'ja']")
    [IO.File]::WriteAllText($f3, $c3, [Text.Encoding]::UTF8)
    Write-Host '    make-index-files.mjs: ja added to LANGUAGES.'
} else { Write-Host '    make-index-files.mjs: ja already in LANGUAGES.' }

Write-Host '    Done.'
