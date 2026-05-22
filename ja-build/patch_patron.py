"""
patch_patron.py
パトロン表示・サポーターマーキーを非表示にする
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_patron.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    # ── CheckedItem.vue: パトロン表示を無効化 ──────────────────────────
    f1 = os.path.join(repo, 'renderer', 'src', 'web', 'price-check', 'CheckedItem.vue')
    if not os.path.exists(f1):
        print(f"  [WARN] Not found: {f1}")
    else:
        c = open(f1, encoding='utf-8').read()
        if 'showSupportLinks.value = false' in c:
            print("  [SKIP] CheckedItem.vue: already patched")
        elif 'showSupportLinks.value = true' in c:
            c = c.replace('showSupportLinks.value = true', 'showSupportLinks.value = false')
            open(f1, 'w', encoding='utf-8').write(c)
            print("  [OK] CheckedItem.vue: patron display disabled")
        else:
            print("  [WARN] CheckedItem.vue: showSupportLinks pattern not found")

    # ── SettingsWindow.vue: カエル画像＋パトロンリンクを削除 ────────────
    f2 = os.path.join(repo, 'renderer', 'src', 'web', 'settings', 'SettingsWindow.vue')
    if not os.path.exists(f2):
        print(f"  [WARN] Not found: {f2}")
    else:
        c2 = open(f2, encoding='utf-8').read()

        # peepoLove2x.webp を含む <div>...</div> ブロックを削除
        if 'peepoLove2x.webp' not in c2:
            print("  [SKIP] SettingsWindow.vue: peepo already removed")
        else:
            idx = c2.index('peepoLove2x.webp')
            div_start = c2.rfind('<div', 0, idx)
            div_end = c2.index('</div>', idx) + len('</div>')
            c2 = c2[:div_start] + c2[div_end:]
            print("  [OK] SettingsWindow.vue: peepo+patreon removed")

        # サポーターマーキーを v-if="false" で非表示
        if 'patronsHorizontal]" v-if="false"' in c2 or "patronsHorizontal]' v-if=\"false\"" in c2:
            print("  [SKIP] SettingsWindow.vue: marquee already hidden")
        else:
            # :class="[$style.patronsHorizontal, { 'invisible': podiumVisible }]" を探す
            new_c2, n = re.subn(
                r':class="\[\$style\.patronsHorizontal,\s*\{[^}]*\}\]"',
                ':class="[$style.patronsHorizontal]" v-if="false"',
                c2
            )
            if n > 0:
                c2 = new_c2
                print("  [OK] SettingsWindow.vue: supporter marquee hidden")
            else:
                print("  [WARN] SettingsWindow.vue: marquee pattern not found")

        open(f2, 'w', encoding='utf-8').write(c2)
        print("  SettingsWindow.vue saved.")

if __name__ == '__main__':
    main()
