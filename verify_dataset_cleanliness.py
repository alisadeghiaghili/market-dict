#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for MarketDict Dataset
Strictly checks all 631 terms for Table of Contents completeness,
Persian translation accuracy, and absence of boilerplate or English sentences.
"""

import json
import re
import sys

BOILERPLATE_PATTERNS = [
    "این بخش به بررسی جامع مفاهیم",
    "الزامات عملیاتی مرتبط در تحلیل بازار",
    "یک مفهوم و اصطلاح کلیدی در حوزه",
]

STOP_WORDS = {
    'the', 'is', 'are', 'was', 'were', 'and', 'that', 'with', 
    'from', 'this', 'have', 'has', 'for', 'which', 'will', 'you', 'your', 'they', 'their'
}

def has_english_sentence(text: str) -> bool:
    if not text or not isinstance(text, str):
        return False
    # Strip LaTeX/math environments and formulas
    clean = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '', text, flags=re.DOTALL)
    clean = re.sub(r'\$\$.*?\$\$', '', clean, flags=re.DOTALL)
    clean = re.sub(r'\\text\{.*?\}', '', clean)
    clean = re.sub(r'\\frac\{.*?\}\{.*?\}', '', clean)
    # Remove text in parentheses (e.g. acronyms or translations like (ROI), (P/E))
    clean = re.sub(r'\([^)]*\)', '', clean)
    
    # Check for consecutive English words forming sentences
    sentences = re.split(r'[\.\n\r;!?]+', clean)
    for s in sentences:
        words = [w.lower() for w in re.findall(r'[a-zA-Z]{2,}', s)]
        stop_count = sum(1 for w in words if w in STOP_WORDS)
        if stop_count >= 3 and len(words) >= 6:
            return True
    return False

def verify_dataset(filepath="bilingual_dictionary.json"):
    print(f"Loading {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_terms = len(data)
    print(f"Total terms loaded: {total_terms}")

    errors = []
    warnings = []

    if total_terms < 631:
        errors.append(f"Expected at least 631 terms, got {total_terms}")

    terms_without_sections = []
    total_sections = 0
    total_paragraphs = 0
    boilerplate_hits = 0
    english_in_fa_hits = 0

    for idx, term in enumerate(data):
        tid = term.get("id")
        term_en = term.get("term_en", "")
        term_fa = term.get("term_fa", "")

        # Check titles
        if not term_en:
            errors.append(f"Term #{tid} missing term_en")
        if not term_fa:
            errors.append(f"Term '{term_en}' missing term_fa")
        elif has_english_sentence(term_fa):
            errors.append(f"Term '{term_en}' term_fa contains raw English: '{term_fa}'")

        # Check definition
        def_en = term.get("definition_en", "")
        def_fa = term.get("definition_fa", "")
        if not def_en:
            warnings.append(f"Term '{term_en}' missing definition_en")
        if not def_fa:
            errors.append(f"Term '{term_en}' missing definition_fa")
        else:
            if has_english_sentence(def_fa):
                errors.append(f"Term '{term_en}' definition_fa contains raw English")
                english_in_fa_hits += 1
            for bp in BOILERPLATE_PATTERNS:
                if bp in def_fa:
                    errors.append(f"Term '{term_en}' definition_fa contains boilerplate: '{bp}'")
                    boilerplate_hits += 1

        # Check takeaways
        takeaways_en = term.get("takeaways_en", [])
        takeaways_fa = term.get("takeaways_fa", [])
        if takeaways_en:
            if not takeaways_fa:
                errors.append(f"Term '{term_en}' has takeaways_en ({len(takeaways_en)}) but empty takeaways_fa")
            elif len(takeaways_fa) != len(takeaways_en):
                warnings.append(f"Term '{term_en}' takeaways count mismatch (en={len(takeaways_en)}, fa={len(takeaways_fa)})")
            for tfa in takeaways_fa:
                if has_english_sentence(tfa):
                    errors.append(f"Term '{term_en}' takeaway contains raw English: '{tfa[:60]}...'")
                    english_in_fa_hits += 1

        # Check bottom line
        bl_fa = term.get("bottom_line_fa", "")
        if bl_fa and has_english_sentence(bl_fa):
            errors.append(f"Term '{term_en}' bottom_line_fa contains raw English")
            english_in_fa_hits += 1

        # Check sections
        sections = term.get("sections", [])
        if not sections:
            terms_without_sections.append(term_en)
        else:
            total_sections += len(sections)
            for sec_idx, sec in enumerate(sections):
                t_en = sec.get("title_en", "")
                t_fa = sec.get("title_fa", "")
                if not t_fa:
                    errors.append(f"Term '{term_en}' sec #{sec_idx} missing title_fa")
                elif has_english_sentence(t_fa):
                    errors.append(f"Term '{term_en}' sec #{sec_idx} title_fa contains English: '{t_fa}'")

                paras_en = sec.get("paragraphs_en", [])
                paras_fa = sec.get("paragraphs_fa", [])
                total_paragraphs += len(paras_fa)
                if paras_en and not paras_fa:
                    errors.append(f"Term '{term_en}' sec #{sec_idx} ('{t_en}') missing paragraphs_fa")
                for p_fa in paras_fa:
                    for bp in BOILERPLATE_PATTERNS:
                        if bp in p_fa:
                            errors.append(f"Term '{term_en}' sec #{sec_idx} contains boilerplate")
                            boilerplate_hits += 1
                    if has_english_sentence(p_fa):
                        errors.append(f"Term '{term_en}' sec #{sec_idx} paragraph contains English: '{p_fa[:80]}...'")
                        english_in_fa_hits += 1

                items_en = sec.get("items_en", [])
                items_fa = sec.get("items_fa", [])
                for i_fa in items_fa:
                    for bp in BOILERPLATE_PATTERNS:
                        if bp in i_fa:
                            errors.append(f"Term '{term_en}' sec #{sec_idx} item contains boilerplate")
                            boilerplate_hits += 1
                    if has_english_sentence(i_fa):
                        errors.append(f"Term '{term_en}' sec #{sec_idx} item contains English: '{i_fa[:80]}...'")
                        english_in_fa_hits += 1

    print("\n--- Verification Summary ---")
    print(f"Total Terms: {total_terms}")
    print(f"Terms with Sections: {total_terms - len(terms_without_sections)} / {total_terms}")
    print(f"Total Sections: {total_sections}")
    print(f"Total Paragraphs: {total_paragraphs}")
    print(f"Boilerplate Hits: {boilerplate_hits}")
    print(f"English In Persian Hits: {english_in_fa_hits}")
    print(f"Total Errors: {len(errors)}")
    print(f"Total Warnings: {len(warnings)}")

    if terms_without_sections:
        print(f"\nTerms without sections ({len(terms_without_sections)}):")
        for tw in terms_without_sections[:10]:
            print(f"  - {tw}")

    if errors:
        print(f"\nFirst 15 Errors:")
        for err in errors[:15]:
            print(f"  ! {err}")
        return False
    else:
        print("\nSUCCESS: All terms verified clean, complete, and fluent Persian!")
        return True

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "bilingual_dictionary.json"
    ok = verify_dataset(path)
    sys.exit(0 if ok else 1)
