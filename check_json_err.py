import json

with open('bilingual_dictionary.json', 'r', encoding='utf-8') as f:
    text = f.read()

try:
    json.loads(text)
    print("Valid JSON!")
except json.JSONDecodeError as e:
    print(f"Error at line {e.lineno}, col {e.colno}, pos {e.pos}: {e.msg}")
    print("Snippet:")
    print(repr(text[max(0, e.pos - 80):min(len(text), e.pos + 80)]))
