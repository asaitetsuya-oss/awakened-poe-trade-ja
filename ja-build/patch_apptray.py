"""
patch_apptray.py
main/src/AppTray.ts を日本語向けに修正する
"""
import sys, os

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_apptray.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    f = os.path.join(repo, 'main', 'src', 'AppTray.ts')
    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()
    changed = False

    replacements = [
        ('Awakened PoE Trade v',        'Awakened PoE Trade (POE1) v'),
        ("label: 'Settings/League'",    "label: '設定 / リーグ変更'"),
        ("label: 'Open in Browser'",    "label: 'ブラウザで開く'"),
        ("label: 'Open config folder'", "label: '設定フォルダを開く'"),
        ("label: 'Quit'",               "label: '終了'"),
    ]

    for old, new in replacements:
        if new in content:
            print(f"  [SKIP] already patched: {old[:40]}")
        elif old in content:
            content = content.replace(old, new)
            print(f"  [OK] {old[:40]}")
            changed = True
        else:
            print(f"  [WARN] not found: {old[:40]}")

    if changed:
        open(f, 'w', encoding='utf-8').write(content)
        print("  AppTray.ts saved.")
    else:
        print("  AppTray.ts: no changes.")

if __name__ == '__main__':
    main()
