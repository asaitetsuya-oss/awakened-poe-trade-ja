"""
patch_all.py
APT POE1日本語ビルド用パッチ適用スクリプト

使い方:
  py patch_all.py <repo_dir>
"""
import sys, os, re

def read(path):
    return open(path, encoding='utf-8').read()

def write(path, content):
    open(path, 'w', encoding='utf-8').write(content)

def patch(name, path, fn):
    if not os.path.exists(path):
        print(f"  [ERROR] Not found: {path}")
        return
    content = read(path)
    result, msg = fn(content)
    if result != content:
        write(path, result)
    print(f"  {name}: {msg}")

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_all.py <repo_dir>")
        sys.exit(1)

    R = sys.argv[1]

    # 1. AppTray.ts: トレイメニュー日本語化
    def patch_apptray(c):
        c = c.replace('Awakened PoE Trade v', 'Awakened PoE Trade (POE1) v')
        c = c.replace("label: 'Settings/League'", "label: '設定 / リーグ変更'")
        c = c.replace("label: 'Open in Browser'", "label: 'ブラウザで開く'")
        c = c.replace("label: 'Open config folder'", "label: '設定フォルダを開く'")
        c = c.replace("label: 'Quit'", "label: '終了'")
        return c, 'done'
    patch('AppTray.ts', os.path.join(R, 'main', 'src', 'AppTray.ts'), patch_apptray)

    # 2. Config.ts: 言語設定
    def patch_config(c):
        msg = []
        if "'ko' | 'ja'" not in c:
            c = c.replace("language: 'en' | 'ru' | 'cmn-Hant' | 'ko'",
                          "language: 'en' | 'ru' | 'cmn-Hant' | 'ko' | 'ja'")
            msg.append('language type added')
        else:
            msg.append('language type already has ja')
        c = c.replace("language: 'en',", "language: 'ja',")
        if "case 'ja': return 'www.pathofexile.com'" not in c:
            c = c.replace("    case 'ko': return 'poe.game.daum.net'",
                          "    case 'ko': return 'poe.game.daum.net'\n    case 'ja': return 'www.pathofexile.com'")
            msg.append('ja case added')
        else:
            msg.append('ja case already exists')
        return c, ', '.join(msg)
    patch('Config.ts', os.path.join(R, 'renderer', 'src', 'web', 'Config.ts'), patch_config)

    # 3. general.vue: 言語選択に日本語追加
    def patch_general(c):
        if 'value="ja"' in c:
            return c, 'already patched'
        c = c.replace('<option value="ko">한국어</option>',
                      '<option value="ko">한국어</option>\n        <option value="ja">日本語</option>')
        return c, 'done'
    patch('general.vue', os.path.join(R, 'renderer', 'src', 'web', 'settings', 'general.vue'), patch_general)

    # 4. HostClipboard.ts: 日本語クリップボード検出
    def patch_clipboard(c):
        if "'ja'" in c:
            return c, 'ja already exists'
        c = c.replace(
            "  lang: 'cmn-Hans',\n  firstLine: '物品类别: '\n}]",
            "  lang: 'cmn-Hans',\n  firstLine: '物品类别: '\n}, {\n  lang: 'ja',\n  firstLine: 'アイテムクラス: '\n}]"
        )
        return c, 'ja added'
    patch('HostClipboard.ts', os.path.join(R, 'main', 'src', 'shortcuts', 'HostClipboard.ts'), patch_clipboard)

    # 5. CheckedItem.vue: パトロン表示無効
    def patch_patron_checked(c):
        if 'showSupportLinks.value = false' in c:
            return c, 'already patched'
        c = c.replace('showSupportLinks.value = true', 'showSupportLinks.value = false')
        return c, 'patron display disabled'
    patch('CheckedItem.vue', os.path.join(R, 'renderer', 'src', 'web', 'price-check', 'CheckedItem.vue'), patch_patron_checked)

    # 6. SettingsWindow.vue: カエル画像＋マーキー非表示
    def patch_settings_window(c):
        msg = []
        if 'peepoLove2x.webp' in c:
            idx = c.find('peepoLove2x.webp')
            div_start = c.rfind('<div', 0, idx)
            div_end = c.find('</div>', idx) + 6
            c = c[:div_start] + c[div_end:]
            msg.append('peepo removed')
        else:
            msg.append('peepo already removed')
        old = ':class="[$style.patronsHorizontal, { \'invisible\': podiumVisible }]"'
        new = ':class="[$style.patronsHorizontal]" v-if="false"'
        if 'patronsHorizontal]" v-if="false"' not in c:
            c = c.replace(old, new)
            msg.append('marquee hidden')
        else:
            msg.append('marquee already hidden')
        return c, ', '.join(msg)
    patch('SettingsWindow.vue', os.path.join(R, 'renderer', 'src', 'web', 'settings', 'SettingsWindow.vue'), patch_settings_window)

    # 7. client-log.ts: TRADE_WHISPER/BULK_WHISPER に ja 追加
    def patch_client_log(c):
        msg = []
        if "'ja': /^Hi, I would like" not in c:
            ja_line = "  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab \"(?<tab_name>.*)\"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/,"
            c = c.replace("  'cmn-Hant': /^你好，我想購買",
                          f"{ja_line}\n  'cmn-Hant': /^你好，我想購買")
            msg.append('TRADE_WHISPER ja added')
        else:
            msg.append('TRADE_WHISPER ja already exists')
        if "'ja': /^Hi, I'd like" not in c:
            ja_bulk = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/,"
            c = c.replace("  'ko': /^_FIX_ME_$/\n}",
                          f"  'ko': /^_FIX_ME_$/,\n{ja_bulk}\n}}")
            msg.append('TRADE_BULK_WHISPER ja added')
        else:
            msg.append('TRADE_BULK_WHISPER ja already exists')
        return c, ', '.join(msg)
    patch('client-log.ts', os.path.join(R, 'renderer', 'src', 'web', 'client-log', 'client-log.ts'), patch_client_log)

    # 8. hotkeyable-actions.ts: POEDB_LANGS に ja 追加
    def patch_hotkeyable(c):
        if "'ja':" in c:
            return c, 'ja already exists'
        c = c.replace("'ko': 'kr' }", "'ko': 'kr', 'ja': 'us' }")
        return c, 'ja added'
    patch('hotkeyable-actions.ts', os.path.join(R, 'renderer', 'src', 'web', 'item-check', 'hotkeyable-actions.ts'), patch_hotkeyable)

    # 9. make-index-files.mjs: LANGUAGES に ja 追加
    def patch_make_index(c):
        if "'ja'" in c:
            return c, 'ja already in LANGUAGES'
        c = c.replace("const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko']",
                      "const LANGUAGES = ['en', 'ru', 'cmn-Hant', 'ko', 'ja']")
        return c, 'ja added'
    patch('make-index-files.mjs', os.path.join(R, 'renderer', 'src', 'assets', 'make-index-files.mjs'), patch_make_index)

    # 10. Parser.ts: 品質行パース修正 + ITEM_BY_TRANSLATED (UNIQUE + ITEMベースタイプ)
    def patch_parser(c):
        msg = []
        # 品質行パース
        if 'line.startsWith("品質 (")' not in c:
            c = c.replace('line.startsWith(_$.QUALITY)',
                          'line.startsWith(_$.QUALITY) || line.startsWith("品質 (")')
            msg.append('quality patched')
        else:
            msg.append('quality already patched')
        # UNIQUE名の日本語対応
        if "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_REF('UNIQUE', item.name)" not in c:
            c = c.replace("ITEM_BY_REF('UNIQUE', item.name)",
                          "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_REF('UNIQUE', item.name)")
            msg.append('ITEM_BY_TRANSLATED(UNIQUE) patched')
        else:
            msg.append('ITEM_BY_TRANSLATED(UNIQUE) already patched')
        # レア/マジック/ノーマルのベースタイプ日本語対応
        old_base = "info = ITEM_BY_REF('ITEM', item.baseType ?? item.name)"
        new_base = (
            "console.log('[APT-JA] baseType:', item.baseType, 'name:', item.name)\n"
            "    info = ITEM_BY_REF('ITEM', item.baseType ?? item.name) ??\n"
            "    ITEM_BY_TRANSLATED('ITEM', item.baseType ?? item.name)"
        )
        if "ITEM_BY_TRANSLATED('ITEM', item.baseType ?? item.name)" not in c:
            c = c.replace(old_base, new_base)
            msg.append('ITEM_BY_TRANSLATED(ITEM baseType) patched')
        else:
            msg.append('ITEM_BY_TRANSLATED(ITEM baseType) already patched')
        return c, ', '.join(msg)
    patch('Parser.ts', os.path.join(R, 'renderer', 'src', 'parser', 'Parser.ts'), patch_parser)

    # 11. create-item-filters.ts: ユニーク名とベースタイプをrefNameで検索
    def patch_filters(c):
        msg = []
        if "ITEM_BY_REF('ITEM', item.info.unique.base)![0].refName" not in c:
            c = c.replace("t(opts, ITEM_BY_REF('ITEM', item.info.unique.base)![0])",
                          "ITEM_BY_REF('ITEM', item.info.unique.base)![0].refName")
            msg.append('baseType refName patched')
        else:
            msg.append('baseType already patched')
        if 'nameTrade: item.info.refName' not in c:
            c = c.replace('nameTrade: t(opts, item.info),', 'nameTrade: item.info.refName,')
            msg.append('nameTrade refName patched')
        else:
            msg.append('nameTrade already patched')
        return c, ', '.join(msg)
    patch('create-item-filters.ts', os.path.join(R, 'renderer', 'src', 'web', 'price-check', 'filters', 'create-item-filters.ts'), patch_filters)


    # 12. PriceTrend.vue: "ベースアイテム"テキストを削除してアイコン画像を表示
    def patch_price_trend(c):
        old = (
            '        <template #item v-if="isValuableBasetype">\n'
            "          <span class=\"text-gray-400\">{{ t(':base_item') }}</span>\n"
            '        </template>'
        )
        if old not in c:
            return c, 'already patched or not found'
        c = c.replace(old, '')
        return c, 'base_item text removed, icon will show'
    patch('PriceTrend.vue', os.path.join(R, 'renderer', 'src', 'web', 'price-check', 'trends', 'PriceTrend.vue'), patch_price_trend)


    # 13. electron-builder.yml: publish先を自分のリポジトリに変更
    def patch_electron_builder(c):
        import re
        if 'asaitetsuya-oss' in c:
            return c, 'already patched'
        c = re.sub(r'owner: SnosMe', 'owner: asaitetsuya-oss', c)
        c = re.sub(r'repo: awakened-poe-trade', 'repo: awakened-poe-trade-ja', c)
        return c, 'publish target changed to asaitetsuya-oss/awakened-poe-trade-ja'
    patch('electron-builder.yml', os.path.join(R, 'main', 'electron-builder.yml'), patch_electron_builder)

    print("All patches applied.")

if __name__ == '__main__':
    main()
