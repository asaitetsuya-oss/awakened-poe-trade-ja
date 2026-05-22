param([string]$RepoDir)
$parserPath = "$RepoDir\renderer\src\parser\Parser.ts"
$filterPath = "$RepoDir\renderer\src\web\price-check\filters\create-item-filters.ts"

# 1. Parser.ts: quality fix
$content = Get-Content $parserPath -Raw -Encoding UTF8
if ($content -match 'line\.startsWith\(_\$\.QUALITY\) \|\| line\.startsWith\("品質 \("') {
    Write-Host "    Parser.ts: quality already patched."
} else {
    $content = $content -replace 'line\.startsWith\(_\$\.QUALITY\)', 'line.startsWith(_$.QUALITY) || line.startsWith("品質 (")'
    Set-Content $parserPath $content -Encoding UTF8 -NoNewline
    Write-Host "    Parser.ts: quality patched."
}

# 2. Parser.ts: ITEM_BY_TRANSLATED for unique names (correct form check)
$content = Get-Content $parserPath -Raw -Encoding UTF8
if ($content -match "ITEM_BY_TRANSLATED\('UNIQUE', item\.name\) \?\? ITEM_BY_REF\('UNIQUE', item\.name\)") {
    Write-Host "    Parser.ts: ITEM_BY_TRANSLATED already patched."
} else {
    # Fix broken form (TRANSLATED ?? TRANSLATED) or original (REF)
    $content = $content -replace "ITEM_BY_TRANSLATED\('UNIQUE', item\.name\) \?\? ITEM_BY_TRANSLATED\('UNIQUE', item\.name\)", "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_REF('UNIQUE', item.name)"
    $content = $content -replace "ITEM_BY_REF\('UNIQUE', item\.name\)", "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_REF('UNIQUE', item.name)"
    Set-Content $parserPath $content -Encoding UTF8 -NoNewline
    Write-Host "    Parser.ts: ITEM_BY_TRANSLATED patched."
}

# 3. create-item-filters.ts: always use refName for unique base type
$content = Get-Content $filterPath -Raw -Encoding UTF8
if ($content -match "ITEM_BY_REF\('ITEM', item\.info\.unique\.base\)!\[0\]\.refName") {
    Write-Host "    create-item-filters.ts: unique refName already patched."
} elseif ($content -match "ITEM_BY_REF\('ITEM', item\.info\.unique\.base\)") {
    $content = $content -replace "t\(opts, ITEM_BY_REF\('ITEM', item\.info\.unique\.base\)!\[0\]\)", "ITEM_BY_REF('ITEM', item.info.unique.base)![0].refName"
    Set-Content $filterPath $content -Encoding UTF8 -NoNewline
    Write-Host "    create-item-filters.ts: unique refName patched."
} else {
    Write-Host "    create-item-filters.ts: target line not found, skipping."
}

Write-Host "    Done."
