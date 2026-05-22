param([string]$RepoDir)

# ── client-log.ts ──────────────────────────────────────────
$f = "$RepoDir\renderer\src\web\client-log\client-log.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)

# TRADE_WHISPER に ja を追加
if ($c.Contains("'ja': /^Hi, I would like")) {
    Write-Host '    TRADE_WHISPER ja already exists.'
} elseif ($c.Contains("'cmn-Hant': /^")) {
    $jaLine = "  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \(stash tab ""(?<tab_name>.*)""; position: left (?<tab_left>\d+), top (?<tab_top>\d+)\)(?<message>.+)?`$/,"
    # cmn-Hant 行の先頭にマッチして前に挿入
    $c = $c -replace "(?m)^(\s*'cmn-Hant': /\^你好，我想購買)", "$jaLine`r`n`$1"
    Write-Host '    TRADE_WHISPER ja added (before cmn-Hant).'
} else {
    Write-Host '    [WARN] TRADE_WHISPER cmn-Hant pattern not found.'
}

# TRADE_BULK_WHISPER に ja を追加
if ($c.Contains("'ja': /^Hi, I'd like")) {
    Write-Host '    TRADE_BULK_WHISPER ja already exists.'
} elseif ($c.Contains("'ko': /^_FIX_ME_")) {
    $jaBulkLine = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\.(?<message>.+)?`$/,"
    $c = $c -replace "(?m)^(\s*'ko': /\^_FIX_ME_[^\r\n]*)\r?\n(\})", "`$1,`r`n$jaBulkLine`r`n`$2"
    Write-Host '    TRADE_BULK_WHISPER ja added (after ko).'
} else {
    # ko がない場合: 閉じ } の直前に追加
    $jaBulkLine = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\.(?<message>.+)?`$/,"
    # TRADE_BULK_WHISPER ブロックの最後のエントリの後に挿入
    # cmn-Hant エントリの後ろの } を探して ja を差し込む
    $c = $c -replace "(?m)^(\s*'cmn-Hant': /\^[^\r\n]*)\r?\n(\})", "`$1`r`n$jaBulkLine`r`n`$2"
    Write-Host '    TRADE_BULK_WHISPER ja added (no ko, after cmn-Hant).'
}

[IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)

# ── hotkeyable-actions.ts ──────────────────────────────────
$f2 = "$RepoDir\renderer\src\web\item-check\hotkeyable-actions.ts"
$c2 = [IO.File]::ReadAllText($f2, [Text.Encoding]::UTF8)

if ($c2.Contains("'ja':")) {
    Write-Host '    POEDB_LANGS ja already exists.'
} elseif ($c2.Contains("'ko': 'kr'")) {
    $c2 = $c2.Replace("'ko': 'kr' }", "'ko': 'kr', 'ja': 'us' }")
    Write-Host '    POEDB_LANGS ja added (after ko).'
} elseif ($c2.Contains("'cmn-Hant':")) {
    # ko がない場合: cmn-Hant エントリの後に追加
    $c2 = $c2 -replace "('cmn-Hant':\s*'[^']*')\s*\}", "`$1, 'ja': 'us' }"
    Write-Host '    POEDB_LANGS ja added (after cmn-Hant, no ko).'
} else {
    Write-Host '    [WARN] POEDB_LANGS pattern not found.'
}

[IO.File]::WriteAllText($f2, $c2, [Text.Encoding]::UTF8)

# ── make-index-files.mjs ───────────────────────────────────
$f3 = "$RepoDir\renderer\src\assets\make-index-files.mjs"
$c3 = [IO.File]::ReadAllText($f3, [Text.Encoding]::UTF8)

if ($c3.Contains("'ja'")) {
    Write-Host '    make-index-files.mjs: ja already in LANGUAGES.'
} elseif ($c3.Contains("'ko'")) {
    $c3 = $c3.Replace("const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko']", "const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko', 'ja']")
    Write-Host '    make-index-files.mjs: ja added (with ko).'
} else {
    $c3 = $c3.Replace("const LANGUAGES = ['en', 'ru', 'cmn-Hant']", "const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ja']")
    Write-Host '    make-index-files.mjs: ja added (no ko).'
}

[IO.File]::WriteAllText($f3, $c3, [Text.Encoding]::UTF8)

Write-Host '    Done.'
