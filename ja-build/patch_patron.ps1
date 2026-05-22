param([string]$RepoDir)

# CheckedItem.vue: パトロン表示を無効化
$f = "$RepoDir\renderer\src\web\price-check\CheckedItem.vue"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)
if ($c.Contains('showSupportLinks.value = true')) {
    $c = $c.Replace('showSupportLinks.value = true', 'showSupportLinks.value = false')
    [IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
    Write-Host '    CheckedItem.vue: patron display disabled.'
} else { Write-Host '    CheckedItem.vue: already patched.' }

# SettingsWindow.vue: カエル画像＋パトロンリンクを削除
$f2 = "$RepoDir\renderer\src\web\settings\SettingsWindow.vue"
$c2 = [IO.File]::ReadAllText($f2, [Text.Encoding]::UTF8)
if ($c2.Contains('peepoLove2x.webp')) {
    $idx = $c2.IndexOf('peepoLove2x.webp')
    $divStart = $c2.LastIndexOf('<div', $idx)
    $divEnd = $c2.IndexOf('</div>', $idx) + 6
    $c2 = $c2.Substring(0, $divStart) + $c2.Substring($divEnd)
    [IO.File]::WriteAllText($f2, $c2, [Text.Encoding]::UTF8)
    Write-Host '    SettingsWindow.vue: peepo+patreon removed.'
} else { Write-Host '    SettingsWindow.vue: peepo already removed.' }

# SettingsWindow.vue: サポーターマーキーをv-if=falseで非表示
$f3 = "$RepoDir\renderer\src\web\settings\SettingsWindow.vue"
$c3 = [IO.File]::ReadAllText($f3, [Text.Encoding]::UTF8)
$old3 = ':class="[$style.patronsHorizontal, { ' + "'invisible': podiumVisible }]" + '"'
$new3 = ':class="[$style.patronsHorizontal]" v-if="false"'
if (-not $c3.Contains('patronsHorizontal]" v-if="false"')) {
    $c3 = $c3.Replace($old3, $new3)
    [IO.File]::WriteAllText($f3, $c3, [Text.Encoding]::UTF8)
    Write-Host '    SettingsWindow.vue: supporter marquee hidden.'
} else { Write-Host '    SettingsWindow.vue: marquee already hidden.' }

Write-Host '    Done.'
