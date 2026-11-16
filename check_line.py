with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line_no in [92565, 92566, 92567, 92568]:
    l = lines[line_no - 1]
    print(f"Line {line_no} (len {len(l)}):")
    print(repr(l))
