param([string]$RepoDir)
$f = "$RepoDir\renderer\src\web\settings\general.vue"
$c = [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8)
if ($c -notmatch 'value="ja"') {
    $ja = "<option value=""ja"">日本語</option>"
    $c = $c.Replace("<option value=""ko"">한국어</option>", "<option value=""ko"">한국어</option>`n        $ja")
    [IO.File]::WriteAllText($f, $c, [Text.Encoding]::UTF8)
    Write-Host '    Done.'
} else {
    Write-Host '    Already patched.'
}