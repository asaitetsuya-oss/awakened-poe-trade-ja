"""
patch_version.py
main/package.json のリポジトリURLを自分のリポジトリに変更する
"""
import sys, os, re

def main():
    if len(sys.argv) < 2:
        print("Usage: py patch_version.py <repo_dir>")
        sys.exit(1)
    repo = sys.argv[1]

    f = os.path.join(repo, 'main', 'package.json')
    if not os.path.exists(f):
        print(f"[ERROR] Not found: {f}")
        sys.exit(1)

    content = open(f, encoding='utf-8').read()

    if 'asaitetsuya-oss/awakened-poe-trade-ja' in content:
        print("  [SKIP] package.json: repository already patched")
        return

    new_content, n = re.subn(
        r'"repository":\s*"[^"]*"',
        '"repository": "https://github.com/asaitetsuya-oss/awakened-poe-trade-ja"',
        content
    )
    if n > 0:
        # BOMなしUTF-8で保存
        open(f, 'w', encoding='utf-8').write(new_content)
        print("  [OK] package.json: repository URL patched")
    else:
        print("  [WARN] package.json: repository field not found")

if __name__ == '__main__':
    main()
