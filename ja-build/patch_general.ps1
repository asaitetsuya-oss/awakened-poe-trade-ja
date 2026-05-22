param([string]$RepoDir)
$f = "$RepoDir\renderer\src\web\settings\general.vue"
$c = ([IO.StreamReader]::new($f, [Text.UTF8Encoding]::new($false))).ReadToEnd()
if ($c -notmatch 'value="ja"') {
    $ja = "<option value=""ja"">日本語</option>"
    $c = $c.Replace("<option value=""ko"">한국어</option>", "<option value=""ko"">한국어</option>`n        $ja")
    $_writer = [IO.StreamWriter]::new($f, $false, [Text.UTF8Encoding]::new($false))
    $_writer.Write($c)
    $_writer.Close()
    Write-Host '    Done.'
} else {
    Write-Host '    Already patched.'
}