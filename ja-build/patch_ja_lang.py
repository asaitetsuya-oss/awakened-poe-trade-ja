"""
patch_ja_lang.py
client-log.ts / hotkeyable-actions.ts / make-index-files.mjs に ja エントリを追加する
"""
import sys, os, re

def patch_file(path, patches):
    if not os.path.exists(path):
        print(f"  [ERROR] Not found: {path}")
        return False
    content = open(path, encoding='utf-8').read()
    changed = False
    for desc, check, old, new in patches:
        if check in content:
            print(f"  [SKIP] {desc}: already exists")
            continue
        if old not in content:
            print(f"  [WARN] {desc}: pattern not found")
            continue
        content = content.replace(old, new)
        print(f"  [OK] {desc}")
        changed = True
    if changed:
        open(path, 'w', encoding='utf-8').write(content)
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_ja_lang.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    # ── client-log.ts ──────────────────────────────────────
    f1 = os.path.join(repo, 'renderer', 'src', 'web', 'client-log', 'client-log.ts')
    content = open(f1, encoding='utf-8').read()

    # 改行コードを統一して扱う
    crlf = '\r\n' in content
    content = content.replace('\r\n', '\n')

    changed = False

    # TRADE_WHISPER: cmn-Hant 行の直前に ja を挿入
    ja_whisper = "  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab \"(?<tab_name>.*)\"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/,"
    if "'ja': /^Hi, I would like" in content:
        print("  [SKIP] TRADE_WHISPER ja: already exists")
    else:
        # cmn-Hant 行を探して前に挿入
        m = re.search(r"( *'cmn-Hant': /\^你好，我想購買)", content)
        if m:
            content = content[:m.start()] + ja_whisper + '\n' + content[m.start():]
            print("  [OK] TRADE_WHISPER ja added")
            changed = True
        else:
            print("  [WARN] TRADE_WHISPER cmn-Hant pattern not found")

    # TRADE_BULK_WHISPER: cmn-Hant 行の後、} の前に ja を挿入
    ja_bulk = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/,"
    if "'ja': /^Hi, I'd like" in content:
        print("  [SKIP] TRADE_BULK_WHISPER ja: already exists")
    else:
        # TRADE_BULK_WHISPER ブロック内の cmn-Hant 行を探す
        m = re.search(r"( *'cmn-Hant': /\^你好，我想用[^\n]*)\n(\})", content)
        if m:
            content = content[:m.end(1)] + '\n' + ja_bulk + '\n' + content[m.start(2):]
            print("  [OK] TRADE_BULK_WHISPER ja added")
            changed = True
        else:
            print("  [WARN] TRADE_BULK_WHISPER cmn-Hant pattern not found")

    if changed:
        if crlf:
            content = content.replace('\n', '\r\n')
        open(f1, 'w', encoding='utf-8').write(content)
    print("  client-log.ts done.")

    # ── hotkeyable-actions.ts ───────────────────────────────
    f2 = os.path.join(repo, 'renderer', 'src', 'web', 'item-check', 'hotkeyable-actions.ts')
    content2 = open(f2, encoding='utf-8').read()
    crlf2 = '\r\n' in content2
    content2 = content2.replace('\r\n', '\n')
    changed2 = False

    if "'ja':" in content2:
        print("  [SKIP] POEDB_LANGS ja: already exists")
    else:
        # パターン例: { 'en': 'us', 'ru': 'ru', 'cmn-Hant': 'cn' }
        m = re.search(r"('cmn-Hant':\s*'[^']*')\s*\}", content2)
        if m:
            content2 = content2[:m.end(1)] + ", 'ja': 'us' }" + content2[m.end():]
            print("  [OK] POEDB_LANGS ja added")
            changed2 = True
        else:
            # ko がある場合
            m = re.search(r"('ko':\s*'[^']*')\s*\}", content2)
            if m:
                content2 = content2[:m.end(1)] + ", 'ja': 'us' }" + content2[m.end():]
                print("  [OK] POEDB_LANGS ja added (after ko)")
                changed2 = True
            else:
                print("  [WARN] POEDB_LANGS pattern not found")

    if changed2:
        if crlf2:
            content2 = content2.replace('\n', '\r\n')
        open(f2, 'w', encoding='utf-8').write(content2)
    print("  hotkeyable-actions.ts done.")

    # ── make-index-files.mjs ────────────────────────────────
    f3 = os.path.join(repo, 'renderer', 'src', 'assets', 'make-index-files.mjs')
    if not os.path.exists(f3):
        print(f"  [WARN] Not found: {f3}")
    else:
        content3 = open(f3, encoding='utf-8').read()
        if "'ja'" in content3:
            print("  [SKIP] make-index-files.mjs ja: already exists")
        else:
            # ['en', 'ru', 'cmn-Hant', 'ko'] or ['en', 'ru', 'cmn-Hant']
            m = re.search(r"(const LANGUAGES\s*=\s*\[(?:[^\]]*?))'(cmn-Hant|ko)'(\s*\])", content3)
            if m:
                content3 = content3[:m.end(2)+1] + ", 'ja'" + content3[m.end(2)+1:]
                open(f3, 'w', encoding='utf-8').write(content3)
                print("  [OK] make-index-files.mjs ja added")
            else:
                print("  [WARN] LANGUAGES pattern not found in make-index-files.mjs")
    print("  make-index-files.mjs done.")

if __name__ == '__main__':
    main()
