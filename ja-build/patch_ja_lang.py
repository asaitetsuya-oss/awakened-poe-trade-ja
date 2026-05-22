"""
patch_ja_lang.py
client-log.ts / hotkeyable-actions.ts / make-index-files.mjs に ja エントリを追加する
部分置換ではなくブロック全体を置換する方式
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_ja_lang.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    # ── client-log.ts: TRADE_WHISPERとTRADE_BULK_WHISPERブロックを丸ごと置換 ──
    f1 = os.path.join(repo, 'renderer', 'src', 'web', 'client-log', 'client-log.ts')
    if not os.path.exists(f1):
        print(f"[ERROR] Not found: {f1}")
        sys.exit(1)

    content = open(f1, encoding='utf-8').read()

    # TRADE_WHISPER ブロック全体を ja 入りで置換
    OLD_WHISPER = """const TRADE_WHISPER = {
  'en': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab "(?<tab_name>.*)"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'ru': /^Здравствуйте, хочу купить у вас (?<item>.+) за (?<price>.+) в лиге (?<league>.+) \\(секция "(?<tab_name>.*)"; позиция: (?<tab_left>\\d+) столбец, (?<tab_top>\\d+) ряд\\)(?<message>.+)?$/,
  'ko': /^안녕하세요, (?<league>.+)\\(보관함 탭 "(?<tab_name>.*)", 위치: 왼쪽 (?<tab_left>\\d+), 상단 (?<tab_top>\\d+)\\)에 (?<price>.+)\\(으\\)로 올려놓은 (?<item>.+)\\(을\\)를 구매하고 싶습니다(?<message>.+)?$/,
  'de': /^Hi, ich möchte '(?<item>.+)' zum angebotenen Preis von (?<price>.+) in der (?<league>.+)-Liga kaufen \\(Truhenfach "(?<tab_name>.*)"; Position: (?<tab_left>\\d+) von links, (?<tab_top>\\d+) von oben\\)(?<message>.+)?$/,
  'fr': /^Bonjour, je souhaiterais t'acheter (?<item>.+) pour (?<price>.+) dans la ligue (?<league>.+) \\(onglet de réserve "(?<tab_name>.*)" ; (?<tab_left>\\d+)e en partant de la gauche, (?<tab_top>\\d+)e en partant du haut\\)(?<message>.+)?$/,
  'es': /^Hola, quisiera comprar tu (?<item>.+) listado por (?<price>.+) en (?<league>.+) \\(pestaña de alijo "(?<tab_name>.*)"; posición: izquierda(?<tab_left>\\d+), arriba (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'pt': /^Olá, eu gostaria de comprar o seu item (?<item>.+) listado por (?<price>.+) na (?<league>.+) \\(aba do baú: "(?<tab_name>.*)"; posição: esquerda (?<tab_left>\\d+), topo (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'th': /^สวัสดี, เราต้องการจะชื้อของคุณ (?<item>.+) ใน ราคา (?<price>.+) ใน (?<league>.+) \\(stash tab "(?<tab_name>.*)"; ตำแหน่ง: ซ้าย (?<tab_left>\\d+), บน (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'cmn-Hant': /^你好，我想購買 (?<item>.+) 標價 (?<price>.+) 在 (?<league>.+) \\(倉庫頁 "(?<tab_name>.*)"; 位置: 左 (?<tab_left>\\d+), 上 (?<tab_top>\\d+)\\)(?<message>.+)?$/
}"""

    NEW_WHISPER = """const TRADE_WHISPER = {
  'en': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab "(?<tab_name>.*)"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'ru': /^Здравствуйте, хочу купить у вас (?<item>.+) за (?<price>.+) в лиге (?<league>.+) \\(секция "(?<tab_name>.*)"; позиция: (?<tab_left>\\d+) столбец, (?<tab_top>\\d+) ряд\\)(?<message>.+)?$/,
  'ko': /^안녕하세요, (?<league>.+)\\(보관함 탭 "(?<tab_name>.*)", 위치: 왼쪽 (?<tab_left>\\d+), 상단 (?<tab_top>\\d+)\\)에 (?<price>.+)\\(으\\)로 올려놓은 (?<item>.+)\\(을\\)를 구매하고 싶습니다(?<message>.+)?$/,
  'de': /^Hi, ich möchte '(?<item>.+)' zum angebotenen Preis von (?<price>.+) in der (?<league>.+)-Liga kaufen \\(Truhenfach "(?<tab_name>.*)"; Position: (?<tab_left>\\d+) von links, (?<tab_top>\\d+) von oben\\)(?<message>.+)?$/,
  'fr': /^Bonjour, je souhaiterais t'acheter (?<item>.+) pour (?<price>.+) dans la ligue (?<league>.+) \\(onglet de réserve "(?<tab_name>.*)" ; (?<tab_left>\\d+)e en partant de la gauche, (?<tab_top>\\d+)e en partant du haut\\)(?<message>.+)?$/,
  'es': /^Hola, quisiera comprar tu (?<item>.+) listado por (?<price>.+) en (?<league>.+) \\(pestaña de alijo "(?<tab_name>.*)"; posición: izquierda(?<tab_left>\\d+), arriba (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'pt': /^Olá, eu gostaria de comprar o seu item (?<item>.+) listado por (?<price>.+) na (?<league>.+) \\(aba do baú: "(?<tab_name>.*)"; posição: esquerda (?<tab_left>\\d+), topo (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'th': /^สวัสดี, เราต้องการจะชื้อของคุณ (?<item>.+) ใน ราคา (?<price>.+) ใน (?<league>.+) \\(stash tab "(?<tab_name>.*)"; ตำแหน่ง: ซ้าย (?<tab_left>\\d+), บน (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'cmn-Hant': /^你好，我想購買 (?<item>.+) 標價 (?<price>.+) 在 (?<league>.+) \\(倉庫頁 "(?<tab_name>.*)"; 位置: 左 (?<tab_left>\\d+), 上 (?<tab_top>\\d+)\\)(?<message>.+)?$/,
  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab "(?<tab_name>.*)"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/
}"""

    # TRADE_BULK_WHISPER ブロック全体を ja 入りで置換
    OLD_BULK = """const TRADE_BULK_WHISPER = {
  'en': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/,
  'ru': /^Здравствуйте, хочу купить у вас (?<item>.+) за (?<price>.+) в лиге (?<league>.+)\\.(?<message>.+)?$/,
  'cmn-Hant': /^你好，我想用 (?<price>.+) 購買 (?<item>.+) in (?<league>.+)\\.(?<message>.+)?$/
}"""

    NEW_BULK = """const TRADE_BULK_WHISPER = {
  'en': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/,
  'ru': /^Здравствуйте, хочу купить у вас (?<item>.+) за (?<price>.+) в лиге (?<league>.+)\\.(?<message>.+)?$/,
  'cmn-Hant': /^你好，我想用 (?<price>.+) 購買 (?<item>.+) in (?<league>.+)\\.(?<message>.+)?$/,
  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/
}"""

    changed = False

    if "'ja': /^Hi, I would like" in content:
        print("  [SKIP] TRADE_WHISPER ja already exists")
    elif OLD_WHISPER in content:
        content = content.replace(OLD_WHISPER, NEW_WHISPER)
        print("  [OK] TRADE_WHISPER ja added")
        changed = True
    else:
        print("  [WARN] TRADE_WHISPER block not found exactly - trying CRLF variant")
        old_crlf = OLD_WHISPER.replace('\n', '\r\n')
        new_crlf = NEW_WHISPER.replace('\n', '\r\n')
        if old_crlf in content:
            content = content.replace(old_crlf, new_crlf)
            print("  [OK] TRADE_WHISPER ja added (CRLF)")
            changed = True
        else:
            print("  [ERROR] TRADE_WHISPER block not found")

    if "'ja': /^Hi, I'd like" in content:
        print("  [SKIP] TRADE_BULK_WHISPER ja already exists")
    elif OLD_BULK in content:
        content = content.replace(OLD_BULK, NEW_BULK)
        print("  [OK] TRADE_BULK_WHISPER ja added")
        changed = True
    else:
        old_crlf = OLD_BULK.replace('\n', '\r\n')
        new_crlf = NEW_BULK.replace('\n', '\r\n')
        if old_crlf in content:
            content = content.replace(old_crlf, new_crlf)
            print("  [OK] TRADE_BULK_WHISPER ja added (CRLF)")
            changed = True
        else:
            print("  [ERROR] TRADE_BULK_WHISPER block not found")

    if changed:
        open(f1, 'w', encoding='utf-8', newline='').write(content)
        print("  client-log.ts saved.")
    else:
        print("  client-log.ts: no changes.")

    # ── hotkeyable-actions.ts ───────────────────────────────
    f2 = os.path.join(repo, 'renderer', 'src', 'web', 'item-check', 'hotkeyable-actions.ts')
    if not os.path.exists(f2):
        print(f"[ERROR] Not found: {f2}")
        sys.exit(1)

    content2 = open(f2, encoding='utf-8').read()
    changed2 = False

    if "'ja':" in content2:
        print("  [SKIP] POEDB_LANGS ja already exists")
    else:
        # cmn-Hant か ko の後に ja を追加
        for anchor in ["'cmn-Hant': 'cn'", "'cmn-Hant': 'us'", "'ko': 'kr'"]:
            if anchor in content2:
                content2 = content2.replace(anchor + " }", anchor + ", 'ja': 'us' }")
                print(f"  [OK] POEDB_LANGS ja added after {anchor}")
                changed2 = True
                break
        if not changed2:
            # アンカーが見つからない場合は正規表現で探す
            m = re.search(r"('(?:cmn-Hant|ko)':\s*'[^']*')\s*\}", content2)
            if m:
                content2 = content2[:m.end(1)] + ", 'ja': 'us' }" + content2[m.end():]
                print("  [OK] POEDB_LANGS ja added (regex)")
                changed2 = True
            else:
                print("  [WARN] POEDB_LANGS pattern not found")

    if changed2:
        open(f2, 'w', encoding='utf-8', newline='').write(content2)
        print("  hotkeyable-actions.ts saved.")

    # ── make-index-files.mjs ────────────────────────────────
    f3 = os.path.join(repo, 'renderer', 'src', 'assets', 'make-index-files.mjs')
    if not os.path.exists(f3):
        print(f"  [WARN] Not found: {f3}")
    else:
        content3 = open(f3, encoding='utf-8').read()
        if "'ja'" in content3:
            print("  [SKIP] make-index-files.mjs ja already exists")
        else:
            for old3, new3 in [
                ("['en', 'ru', 'cmn-Hant', 'ko']", "['en', 'ru', 'cmn-Hant', 'ko', 'ja']"),
                ("['en', 'ru', 'cmn-Hant']",        "['en', 'ru', 'cmn-Hant', 'ja']"),
            ]:
                if old3 in content3:
                    content3 = content3.replace(old3, new3)
                    open(f3, 'w', encoding='utf-8', newline='').write(content3)
                    print(f"  [OK] make-index-files.mjs ja added")
                    break
            else:
                print("  [WARN] LANGUAGES pattern not found in make-index-files.mjs")

    print("  Done.")

if __name__ == '__main__':
    main()
