param([string]$RepoDir)
$f = "$RepoDir\main\src\AppTray.ts"
$c = ([IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))).ReadToEnd()
$c = $c.Replace('Awakened PoE Trade v', 'Awakened PoE Trade (POE1) v')
$c = $c.Replace("public overlayKey = 'Shift + Space'", "public overlayKey = 'Shift + F1'")
$c = $c.Replace("label: 'Settings/League'", "label: '設定 / リーグ変更'")
$c = $c.Replace("label: 'Open in Browser'", "label: 'ブラウザで開く'")
$c = $c.Replace("label: 'Open config folder'", "label: '設定フォルダを開く'")
$c = $c.Replace("label: 'Quit'", "label: '終了'")
$_writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
$_writer.Write($c)
$_writer.Close()
Write-Host '    Done.'