"""
patch_config.py
renderer/src/web/Config.ts に ja サポートを追加する
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_config.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    f = os.path.join(repo, 'renderer', 'src', 'web', 'Config.ts')
    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()
    changed = False

    # ── 1. language 型定義に 'ja' を追加 ──────────────────────────────
    # 例: language: 'en' | 'ru' | 'cmn-Hant'
    #     language: 'en' | 'ru' | 'cmn-Hant' | 'ko'
    #     language: 'en' | 'ru' | 'cmn-Hant' | 'ko' | 'de' | ...
    if "'ja'" in content and "language:" in content:
        print("  [SKIP] language type: 'ja' already present")
    else:
        # language: で始まりクォートされた言語リストを持つ行を探す
        new_content, n = re.subn(
            r"(language:\s*(?:'[^']+'\s*\|\s*)*'cmn-Hant'(?:\s*\|\s*'[^']+')*)(?!\s*\|\s*'ja')",
            r"\1 | 'ja'",
            content
        )
        if n > 0:
            content = new_content
            print(f"  [OK] language type: 'ja' added ({n} occurrence(s))")
            changed = True
        else:
            print("  [WARN] language type pattern not found")

    # ── 2. デフォルト言語を 'ja' に変更 ───────────────────────────────
    if "language: 'ja'," in content:
        print("  [SKIP] default language: already 'ja'")
    elif "language: 'en'," in content:
        content = content.replace("language: 'en',", "language: 'ja',")
        print("  [OK] default language set to 'ja'")
        changed = True
    else:
        print("  [WARN] default language 'en' not found")

    # ── 3. overlayKey のデフォルトを Shift+F1 に変更 ──────────────────
    if "overlayKey: 'Shift + F1'" in content:
        print("  [SKIP] overlayKey: already Shift + F1")
    elif "overlayKey: 'Shift + Space'" in content:
        content = content.replace("overlayKey: 'Shift + Space'", "overlayKey: 'Shift + F1'")
        print("  [OK] overlayKey set to Shift + F1")
        changed = True

    # ── 4. poeWebApi に ja ケースを追加 ───────────────────────────────
    if "case 'ja':" in content:
        print("  [SKIP] poeWebApi ja case: already exists")
    else:
        # case 'cmn-Hant': か case 'ko': の後に ja を追加
        new_content, n = re.subn(
            r"(case '(?:cmn-Hant|ko)':[^\n]+\n)",
            r"\1    case 'ja': return 'www.pathofexile.com'\n",
            content
        )
        if n > 0:
            content = new_content
            print(f"  [OK] poeWebApi ja case added")
            changed = True
        else:
            print("  [WARN] poeWebApi case pattern not found")

    if changed:
        open(f, 'w', encoding='utf-8').write(content)
        print("  Config.ts saved.")
    else:
        print("  Config.ts: no changes.")

if __name__ == '__main__':
    main()
