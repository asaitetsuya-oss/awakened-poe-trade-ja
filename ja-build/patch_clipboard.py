"""
patch_clipboard.py
main/src/shortcuts/HostClipboard.ts に日本語クライアント検出を追加する
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_clipboard.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    f = os.path.join(repo, 'main', 'src', 'shortcuts', 'HostClipboard.ts')
    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()

    if "'ja'" in content:
        print("  [SKIP] HostClipboard.ts: ja already exists")
        return

    # cmn-Hans エントリの後に ja を追加（改行コード問わず）
    # パターン: lang: 'cmn-Hans', firstLine: '物品类别: ' }] の末尾
    new_entry = ",\n  firstLine: 'アイテムクラス: '\n}]"
    old_endings = [
        "  lang: 'cmn-Hans',\r\n  firstLine: '物品类别: '\r\n}]",
        "  lang: 'cmn-Hans',\n  firstLine: '物品类别: '\n}]",
    ]
    new_endings = [
        "  lang: 'cmn-Hans',\r\n  firstLine: '物品类别: '\r\n}, {\r\n  lang: 'ja',\r\n  firstLine: 'アイテムクラス: '\r\n}]",
        "  lang: 'cmn-Hans',\n  firstLine: '物品类别: '\n}, {\n  lang: 'ja',\n  firstLine: 'アイテムクラス: '\n}]",
    ]

    changed = False
    for old, new in zip(old_endings, new_endings):
        if old in content:
            content = content.replace(old, new)
            print("  [OK] HostClipboard.ts: ja added")
            changed = True
            break

    if not changed:
        # 正規表現でフォールバック
        new_content, n = re.subn(
            r"(lang:\s*'cmn-Hans'[^}]*firstLine:\s*'[^']*'\s*\})\]",
            r"\1, {\n  lang: 'ja',\n  firstLine: 'アイテムクラス: '\n}]",
            content
        )
        if n > 0:
            content = new_content
            print("  [OK] HostClipboard.ts: ja added (regex)")
            changed = True
        else:
            print("  [WARN] HostClipboard.ts: cmn-Hans pattern not found")

    if changed:
        open(f, 'w', encoding='utf-8').write(content)
        print("  HostClipboard.ts saved.")

if __name__ == '__main__':
    main()
