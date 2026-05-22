"""
patch_general.py
renderer/src/web/settings/general.vue に日本語選択肢を追加する
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_general.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    f = os.path.join(repo, 'renderer', 'src', 'web', 'settings', 'general.vue')
    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()

    if 'value="ja"' in content:
        print("  [SKIP] ja option already exists")
        return

    ja_option = '<option value="ja">日本語</option>'
    changed = False

    # ko の後に追加
    for anchor in [
        '<option value="ko">한국어</option>',
        "<option value='ko'>한국어</option>",
    ]:
        if anchor in content:
            content = content.replace(anchor, anchor + '\n        ' + ja_option)
            print("  [OK] ja option added after ko")
            changed = True
            break

    # ko がない場合は cmn-Hant の後に追加
    if not changed:
        for anchor in [
            '<option value="cmn-Hant">繁體中文</option>',
            "<option value='cmn-Hant'>繁體中文</option>",
        ]:
            if anchor in content:
                content = content.replace(anchor, anchor + '\n        ' + ja_option)
                print("  [OK] ja option added after cmn-Hant")
                changed = True
                break

    # それでも見つからない場合は </select> の直前に追加
    if not changed:
        m = re.search(r'(<option[^>]+>[^<]*</option>)(\s*</select>)', content)
        if m:
            content = content[:m.end(1)] + '\n        ' + ja_option + content[m.end(1):]
            print("  [OK] ja option added before </select>")
            changed = True
        else:
            print("  [WARN] Could not find insertion point in general.vue")

    if changed:
        open(f, 'w', encoding='utf-8').write(content)
        print("  general.vue saved.")

if __name__ == '__main__':
    main()
