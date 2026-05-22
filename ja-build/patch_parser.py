"""
patch_parser.py
Parser.ts と create-item-filters.ts を日本語向けに修正する
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_parser.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    # ── 1. Parser.ts ───────────────────────────────────────────────────
    f1 = os.path.join(repo, 'renderer', 'src', 'parser', 'Parser.ts')
    if not os.path.exists(f1):
        print(f"[ERROR] Not found: {f1}")
        sys.exit(1)

    c = open(f1, encoding='utf-8').read()
    changed = False

    # quality fix: 品質 ( にも対応
    old_q = 'line.startsWith(_$.QUALITY)'
    new_q = 'line.startsWith(_$.QUALITY) || line.startsWith("品質 (")'
    if new_q in c:
        print("  [SKIP] Parser.ts: quality already patched")
    elif old_q in c:
        c = c.replace(old_q, new_q, 1)
        print("  [OK] Parser.ts: quality patched")
        changed = True
    else:
        print("  [WARN] Parser.ts: QUALITY pattern not found")

    # ITEM_BY_TRANSLATED for unique names
    broken = "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_TRANSLATED('UNIQUE', item.name)"
    original = "ITEM_BY_REF('UNIQUE', item.name)"
    correct = "ITEM_BY_TRANSLATED('UNIQUE', item.name) ?? ITEM_BY_REF('UNIQUE', item.name)"

    if correct in c:
        print("  [SKIP] Parser.ts: ITEM_BY_TRANSLATED already patched")
    elif broken in c:
        c = c.replace(broken, correct)
        print("  [OK] Parser.ts: ITEM_BY_TRANSLATED fixed (broken form)")
        changed = True
    elif original in c:
        c = c.replace(original, correct)
        print("  [OK] Parser.ts: ITEM_BY_TRANSLATED patched")
        changed = True
    else:
        print("  [WARN] Parser.ts: UNIQUE pattern not found")

    if changed:
        open(f1, 'w', encoding='utf-8').write(c)
        print("  Parser.ts saved.")

    # ── 2. create-item-filters.ts ──────────────────────────────────────
    f2 = os.path.join(repo, 'renderer', 'src', 'web', 'price-check', 'filters', 'create-item-filters.ts')
    if not os.path.exists(f2):
        print(f"[WARN] Not found: {f2}")
        return

    c2 = open(f2, encoding='utf-8').read()
    changed2 = False

    target_new = "ITEM_BY_REF('ITEM', item.info.unique.base)![0].refName"
    if target_new in c2:
        print("  [SKIP] create-item-filters.ts: unique refName already patched")
    else:
        new_c2, n = re.subn(
            r"t\(opts,\s*ITEM_BY_REF\('ITEM',\s*item\.info\.unique\.base\)!\[0\]\)",
            "ITEM_BY_REF('ITEM', item.info.unique.base)![0].refName",
            c2
        )
        if n > 0:
            c2 = new_c2
            open(f2, 'w', encoding='utf-8').write(c2)
            print("  [OK] create-item-filters.ts: unique refName patched")
        else:
            print("  [WARN] create-item-filters.ts: target line not found")

    print("  Done.")

if __name__ == '__main__':
    main()
