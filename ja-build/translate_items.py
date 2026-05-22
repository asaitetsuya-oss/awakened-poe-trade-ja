import json, sys, os, urllib.request

REPOE_BASE_ITEMS_URL = "https://repoe-fork.github.io/Japanese/base_items.min.json"

def fetch_json(url):
    print(f"  Fetching: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "awakened-poe-trade-ja-builder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    if len(sys.argv) < 2:
        print("Usage: py translate_items.py <data_dir> [poe1_items_ja.json]")
        sys.exit(1)

    data_dir = sys.argv[1]
    items_ja_path = sys.argv[2] if len(sys.argv) > 2 else None
    en_path = os.path.join(data_dir, "en", "items.ndjson")
    ja_path = os.path.join(data_dir, "ja", "items.ndjson")

    if not os.path.exists(en_path):
        print(f"  [ERROR] Not found: {en_path}")
        sys.exit(1)

    # ベースアイテム名マップ（英語→日本語）
    try:
        ja_base = fetch_json(REPOE_BASE_ITEMS_URL)
        en_base = fetch_json("https://repoe-fork.github.io/base_items.min.json")
        name_map = {}
        for path, ja_data in ja_base.items():
            en_data = en_base.get(path, {})
            en_name = en_data.get("name", "")
            ja_name = ja_data.get("name", "")
            if en_name and ja_name and en_name != ja_name:
                name_map[en_name] = ja_name
        print(f"  Base item name map: {len(name_map)} entries")
    except Exception as e:
        print(f"  [ERROR] Failed to fetch base_items: {e}")
        sys.exit(1)

    # ユニーク名マップ（英語→日本語）: poe1_items_ja.jsonから構築
    unique_map = {}
    if items_ja_path and os.path.exists(items_ja_path):
        print(f"  Loading unique names from {items_ja_path}...")
        with open(items_ja_path, encoding="utf-8") as f:
            items_ja_data = json.load(f)

        # 日本語ベースタイプ→英語ベースタイプの逆引きマップ
        ja_type_to_en = {v: k for k, v in name_map.items()}

        # 英語ベースタイプ→英語ユニーク名リスト（en/items.ndjsonから）
        base_to_en_uniques = {}
        with open(en_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("namespace") == "UNIQUE":
                    base = obj.get("unique", {}).get("base", "")
                    if base:
                        base_to_en_uniques.setdefault(base, []).append(obj["refName"])

        # 日本語ベースタイプ→日本語ユニーク名リスト（poe1_items_ja.jsonから）
        ja_base_to_ja_uniques = {}
        for g in items_ja_data.get("result", []):
            for e in g.get("entries", []):
                if not e.get("flags", {}).get("unique"):
                    continue
                if e.get("disc"):  # legacyはスキップ
                    continue
                ja_name = e.get("name", "")
                ja_type = e.get("type", "")
                if ja_name and ja_type:
                    ja_base_to_ja_uniques.setdefault(ja_type, []).append(ja_name)

        # 英語ユニーク名→日本語ユニーク名をマッピング
        for en_base_name, en_uniques in base_to_en_uniques.items():
            ja_base_name = name_map.get(en_base_name, "")
            if not ja_base_name:
                continue
            ja_uniques = ja_base_to_ja_uniques.get(ja_base_name, [])
            if len(en_uniques) == 1 and len(ja_uniques) == 1:
                unique_map[en_uniques[0]] = ja_uniques[0]
            elif len(en_uniques) == len(ja_uniques):
                for en_u, ja_u in zip(sorted(en_uniques), sorted(ja_uniques)):
                    unique_map[en_u] = ja_u

        print(f"  Unique name map: {len(unique_map)} entries")
    else:
        print("  [WARN] poe1_items_ja.json not provided, unique names will remain in English")

    lines = open(en_path, encoding="utf-8").readlines()
    out = []
    translated = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            en_name = obj.get("name", "")
            ref_name = obj.get("refName", "")
            namespace = obj.get("namespace", "")

            if namespace == "UNIQUE":
                ja_name = unique_map.get(ref_name) or unique_map.get(en_name)
                if ja_name:
                    obj["name"] = ja_name
                    translated += 1
            else:
                ja_name = name_map.get(en_name) or name_map.get(ref_name)
                if ja_name:
                    obj["name"] = ja_name
                    translated += 1

            out.append(json.dumps(obj, ensure_ascii=False))
        except Exception as e:
            print(f"  [WARN] {e}: {line[:80]}")
            out.append(line)

    content = "\n".join(out) + "\n"
    open(ja_path, "wb").write(content.encode("utf-8"))
    print(f"  Translated {translated} items -> {ja_path}")
    print("  Done.")

if __name__ == "__main__":
    main()
