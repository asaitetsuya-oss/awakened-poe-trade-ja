param([string]$RepoDir)
$f = "$RepoDir\main\src\AppTray.ts"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)
$c = $c.Replace('Awakened PoE Trade v', 'Awakened PoE Trade (POE1) v')
$c = $c.Replace("public overlayKey = 'Shift + Space'", "public overlayKey = 'Shift + F1'")
$c = $c.Replace("label: 'Settings/League'", "label: '設定 / リーグ変更'")
$c = $c.Replace("label: 'Open in Browser'", "label: 'ブラウザで開く'")
$c = $c.Replace("label: 'Open config folder'", "label: '設定フォルダを開く'")
$c = $c.Replace("label: 'Quit'", "label: '終了'")
[IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
Write-Host '    Done.'