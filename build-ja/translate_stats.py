import json, re, sys, os

def trade_text_to_apt(text):
    text = text.replace(' (ローカル)', '').replace('(ローカル)', '')
    text = text.replace(' (盾)', '').replace('(盾)', '')
    text = re.sub(r'[+\-]#', '#', text)
    return text.strip()

def make_negate_pairs(ja_str):
    pairs = []
    if '増加する' in ja_str:
        pairs.append(ja_str.replace('増加する', '減少する'))
    if '上昇する' in ja_str:
        pairs.append(ja_str.replace('上昇する', '低下する'))
    return pairs

def build_id_to_ja(trade_stats_json):
    id_to_ja = {}
    for group in trade_stats_json.get('result', []):
        for entry in group.get('entries', []):
            stat_id = entry.get('id', '')
            text = entry.get('text', '')
            if stat_id and text:
                apt_str = trade_text_to_apt(text)
                if apt_str and apt_str not in id_to_ja.get(stat_id, []):
                    if stat_id not in id_to_ja:
                        id_to_ja[stat_id] = []
                    id_to_ja[stat_id].append(apt_str)
    return id_to_ja

# トレードAPIに日本語訳がないpseudo statの手動マッピング
MANUAL_PSEUDO_MAP = {
    "pseudo.pseudo_global_critical_strike_multiplier": ["グローバルクリティカルダメージ倍率合計 #%"],
    "pseudo.pseudo_global_critical_strike_chance": ["グローバルクリティカル率合計 #%"],
}

def build_anoint_name_map(trade_stats_json):
    """アノイントID -> 日本語名のマッピング"""
    # enchant.stat_2954116742, enchant.stat_3459808765, enchant.stat_1898784841, enchant.stat_1422267548
    ANOINT_STAT_IDS = {
        'enchant.stat_2954116742',
        'enchant.stat_3459808765',
        'enchant.stat_1898784841',
        'enchant.stat_1422267548',
    }
    name_map = {}
    for group in trade_stats_json.get('result', []):
        for entry in group.get('entries', []):
            if entry.get('id') in ANOINT_STAT_IDS:
                options = entry.get('option', {}).get('options', [])
                for opt in options:
                    name_map[opt['id']] = opt['text']
    return name_map

def translate_anoint_matchers(obj, anoint_name_map):
    """Allocates XXX 形式のmatcherを日本語に変換"""
    changed = False
    matchers = obj.get('matchers', [])
    new_matchers = []
    for m in matchers:
        s = m.get('string', '')
        # "Allocates XXX" 形式
        if s.startswith('Allocates ') and 'value' in m:
            val = m['value']
            ja_name = anoint_name_map.get(val)
            if ja_name:
                new_m = dict(m)
                new_m['string'] = f'{ja_name} を割り当てる'
                new_matchers.append(new_m)
                changed = True
            else:
                new_matchers.append(m)
        else:
            new_matchers.append(m)
    if changed:
        obj['matchers'] = new_matchers
    return changed

def add_ja_to_stat(stat_obj, id_to_ja):
    all_ids = set()
    for id_list in stat_obj.get('trade', {}).get('ids', {}).values():
        for sid in id_list:
            all_ids.add(sid)

    existing = {m.get('string', '') for m in stat_obj.get('matchers', [])}
    ja_matchers = []
    seen = set()

    for full_id in all_ids:
        for apt_str in id_to_ja.get(full_id, []):
            if apt_str not in existing and apt_str not in seen:
                ja_matchers.append({'string': apt_str})
                seen.add(apt_str)
                for neg_str in make_negate_pairs(apt_str):
                    if neg_str not in existing and neg_str not in seen:
                        ja_matchers.append({'string': neg_str, 'negate': True})
                        seen.add(neg_str)

    if ja_matchers:
        stat_obj['matchers'] = ja_matchers + stat_obj.get('matchers', [])
        return True
    return False

def translate(filepath, id_to_ja, anoint_name_map):
    if not os.path.exists(filepath):
        print(f"  [ERROR] Not found: {filepath}")
        return 0

    raw = open(filepath, 'rb').read()
    lines = raw.decode('utf-8').splitlines()
    translated = 0
    out = []

    for line_str in lines:
        line_str = line_str.strip()
        if not line_str:
            continue
        try:
            obj = json.loads(line_str)
            changed = False

            # アノイント名の翻訳
            if anoint_name_map and translate_anoint_matchers(obj, anoint_name_map):
                changed = True

            if 'stats' in obj:
                for stat in obj['stats']:
                    if add_ja_to_stat(stat, id_to_ja):
                        changed = True
            else:
                all_ids = set()
                for id_list in obj.get('trade', {}).get('ids', {}).values():
                    for sid in id_list:
                        all_ids.add(sid)

                existing = {m.get('string', '') for m in obj.get('matchers', [])}
                ja_matchers = []
                seen = set()

                for full_id in all_ids:
                    for apt_str in id_to_ja.get(full_id, []):
                        if apt_str not in existing and apt_str not in seen:
                            ja_matchers.append({'string': apt_str})
                            seen.add(apt_str)
                            for neg_str in make_negate_pairs(apt_str):
                                if neg_str not in existing and neg_str not in seen:
                                    ja_matchers.append({'string': neg_str, 'negate': True})
                                    seen.add(neg_str)

                if ja_matchers:
                    obj['matchers'] = ja_matchers + obj.get('matchers', [])
                    changed = True

            if changed:
                translated += 1

            out.append(json.dumps(obj, ensure_ascii=False))

        except Exception as e:
            print(f"  [WARN] {e}: {line_str[:80]}")
            out.append(line_str)

    content = '\n'.join(out) + '\n'
    open(filepath, 'wb').write(content.encode('utf-8'))
    return translated

def main():
    if len(sys.argv) < 3:
        print("Usage: py translate_stats.py <data_dir> <poe1_trade_stats_ja.json>")
        sys.exit(1)

    data_dir, trade_json_path = sys.argv[1], sys.argv[2]
    target = os.path.join(data_dir, 'ja', 'stats.ndjson')

    if not os.path.exists(target):
        print(f"  [ERROR] Not found: {target}")
        sys.exit(1)
    if not os.path.exists(trade_json_path):
        print(f"  [ERROR] Not found: {trade_json_path}")
        sys.exit(1)

    en_path = os.path.join(data_dir, 'en', 'stats.ndjson')
    if os.path.exists(en_path):
        print(f"  Copying en/stats.ndjson to ja/stats.ndjson...")
        raw = open(en_path, 'rb').read().replace(b'\r\n', b'\n')
        open(target, 'wb').write(raw)

    print(f"  Loading {trade_json_path}...")
    trade_json = json.load(open(trade_json_path, encoding='utf-8'))

    print("  Building stat ID -> ja text map...")
    id_to_ja = build_id_to_ja(trade_json)
    id_to_ja.update(MANUAL_PSEUDO_MAP)
    print(f"  Total stat IDs with Japanese text: {len(id_to_ja)}")

    print("  Building anointment name map...")
    anoint_name_map = build_anoint_name_map(trade_json)
    print(f"  Total anointment names: {len(anoint_name_map)}")

    print(f"  Translating {target}...")
    n = translate(target, id_to_ja, anoint_name_map)
    print(f"  Translated {n} stats.")
    print("  Done.")

if __name__ == '__main__':
    main()
