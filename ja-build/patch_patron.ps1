param([string]$RepoDir)

# CheckedItem.vue: パトロン表示を無効化
$f = "$RepoDir\renderer\src\web\price-check\CheckedItem.vue"
$c = ([IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))).ReadToEnd()
if ($c.Contains('showSupportLinks.value = true')) {
    $c = $c.Replace('showSupportLinks.value = true', 'showSupportLinks.value = false')
    $_writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
    $_writer.Write($c)
    $_writer.Close()
    Write-Host '    CheckedItem.vue: patron display disabled.'
} else { Write-Host '    CheckedItem.vue: already patched.' }

# SettingsWindow.vue: カエル画像＋パトロンリンクを削除
$f2 = "$RepoDir\renderer\src\web\settings\SettingsWindow.vue"
$c2 = ([IO.StreamReader]::new($f2, [Text.UTF8Encoding]::new($false))).ReadToEnd()
if ($c2.Contains('peepoLove2x.webp')) {
    $idx = $c2.IndexOf('peepoLove2x.webp')
    $divStart = $c2.LastIndexOf('<div', $idx)
    $divEnd = $c2.IndexOf('</div>', $idx) + 6
    $c2 = $c2.Substring(0, $divStart) + $c2.Substring($divEnd)
    $_writer = [IO.StreamWriter]::new($f2, $false, [Text.UTF8Encoding]::new($false))
    $_writer.Write($c2)
    $_writer.Close()
    Write-Host '    SettingsWindow.vue: peepo+patreon removed.'
} else { Write-Host '    SettingsWindow.vue: peepo already removed.' }

# SettingsWindow.vue: サポーターマーキーをv-if=falseで非表示
$f3 = "$RepoDir\renderer\src\web\settings\SettingsWindow.vue"
$c3 = ([IO.StreamReader]::new($f3, [Text.UTF8Encoding]::new($false))).ReadToEnd()
$old3 = ':class="[$style.patronsHorizontal, { ' + "'invisible': podiumVisible }]" + '"'
$new3 = ':class="[$style.patronsHorizontal]" v-if="false"'
if (-not $c3.Contains('patronsHorizontal]" v-if="false"')) {
    $c3 = $c3.Replace($old3, $new3)
    $_writer = [IO.StreamWriter]::new($f3, $false, [Text.UTF8Encoding]::new($false))
    $_writer.Write($c3)
    $_writer.Close()
    Write-Host '    SettingsWindow.vue: supporter marquee hidden.'
} else { Write-Host '    SettingsWindow.vue: marquee already hidden.' }

Write-Host '    Done.'
