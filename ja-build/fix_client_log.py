"""
fix_client_log.py
client-log.ts に ja エントリを追加する

使い方:
  py fix_client_log.py <repo_dir>
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py fix_client_log.py <repo_dir>")
        sys.exit(1)

    repo_dir = sys.argv[1]
    f = os.path.join(repo_dir, 'renderer', 'src', 'web', 'client-log', 'client-log.ts')

    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()

    # 既にjaが追加されている場合はスキップ
    if "'ja': /^Hi, I would like" in content:
        print("  TRADE_WHISPER ja already exists.")
    else:
        # cmn-Hantの行の前にjaを挿入
        ja_line = "  'ja': /^Hi, I would like to buy your (?<item>.+) listed for (?<price>.+) in (?<league>.+) \\(stash tab \"(?<tab_name>.*)\"; position: left (?<tab_left>\\d+), top (?<tab_top>\\d+)\\)(?<message>.+)?$/,"
        content = content.replace(
            "  'cmn-Hant': /^你好，我想購買",
            f"{ja_line}\n  'cmn-Hant': /^你好，我想購買"
        )
        print("  TRADE_WHISPER ja added.")

    # TRADE_BULK_WHISPERにjaを追加
    if "'ja': /^Hi, I'd like" in content:
        print("  TRADE_BULK_WHISPER ja already exists.")
    else:
        ja_bulk = "  'ja': /^Hi, I'd like to buy your (?<item>.+) for my (?<price>.+) in (?<league>.+)\\.(?<message>.+)?$/,"
        content = content.replace(
            "  'ko': /^_FIX_ME_$/\n}",
            f"  'ko': /^_FIX_ME_$/,\n{ja_bulk}\n}}"
        )
        print("  TRADE_BULK_WHISPER ja added.")

    open(f, 'w', encoding='utf-8').write(content)
    print("  Done.")

if __name__ == '__main__':
    main()
