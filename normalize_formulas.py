#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formula Normalizer for MarketDict
Cleans up concatenated MathML / KaTeX artifacts and replaces broken Persian translations
with pure, textbook-grade LaTeX formulas wrapped in $$...$$.
"""

import json
import re

DICT_FILE = "bilingual_dictionary.json"

def clean_paragraph_with_formula(p_text):
    if not p_text or not isinstance(p_text, str):
        return p_text
    
    # 1. Check for \begin{aligned} ... \end{aligned} or any \begin{...} ... \end{...}
    m_env = re.search(r'(\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})', p_text, flags=re.DOTALL)
    if m_env:
        latex = m_env.group(1).strip()
        latex = latex.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        return f"$${latex}$$"

    # 2. Check for KaTeX annotation tag
    m_annot = re.search(r'<annotation[^>]*encoding=["\']application/x-tex["\'][^>]*>(.*?)</annotation>', p_text, flags=re.DOTALL)
    if m_annot:
        latex = m_annot.group(1).strip()
        latex = latex.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        return f"$${latex}$$"

    # 3. Check for standalone equation like \text{...} = \frac{...}{...}
    m_eq = re.search(r'(\\text\{[^{}]+\}\s*=\s*.*?(?=(?:\u200b|\s[A-Z][a-z]+|$)))', p_text, flags=re.DOTALL)
    if m_eq:
        candidate = m_eq.group(1).strip()
        if '\\frac' in candidate or '\\times' in candidate or '\\left' in candidate:
            candidate = candidate.replace('&amp;', '&')
            return f"$${candidate}$$"

    # 4. Check for Variable = \frac{...}{...}
    m_frac = re.search(r'([A-Za-z0-9\s_-]+\s*=\s*\\frac\{.*?\}(?:\s*[-+/*]\s*\\text\{.*?\}|\{[^{}]+\}))', p_text, flags=re.DOTALL)
    if m_frac:
        candidate = m_frac.group(1).strip().replace('&amp;', '&')
        return f"$${candidate}$$"

    # 5. Check for summation e.g. NPV = -\$1,000,000 + \sum...
    m_sum = re.search(r'([A-Za-z0-9_-]+\s*=\s*.*?\\sum.*?)(?=(?:\u200b|\s{2,}|$))', p_text, flags=re.DOTALL)
    if m_sum:
        candidate = m_sum.group(1).strip().replace('&amp;', '&')
        return f"$${candidate}$$"

    # 6. Check for fraction percentage e.g. \frac{(335,000-250,000)}{250,000} \times 100 = 34\%
    m_frac_pct = re.search(r'(\\frac\{[^{}]+\}\{[^{}]+\}\s*\\times\s*[\d.]+\s*=\s*[-+]?[\d.]+\\?%)', p_text, flags=re.DOTALL)
    if m_frac_pct:
        candidate = m_frac_pct.group(1).strip().replace('&amp;', '&')
        return f"$${candidate}$$"

    # 7. Check for CAGR formula e.g. CAGR=\left(\frac...
    m_cagr = re.search(r'([A-Za-z0-9_-]+\s*=\s*\\left\(.*?=\s*[\d.]+\\?%)', p_text, flags=re.DOTALL)
    if m_cagr:
        candidate = m_cagr.group(1).strip().replace('&amp;', '&')
        return f"$${candidate}$$"

    return p_text

def clean_persian_formula_paragraph(p_fa, clean_formula):
    """
    Cleans the Persian paragraph corresponding to a formula.
    If it had a clean introductory sentence before the formula, preserves it and appends the formula.
    Otherwise, sets it to the clean formula itself.
    """
    if not p_fa or not isinstance(p_fa, str):
        return clean_formula
        
    # Check if there is genuine Persian prose at the beginning
    # e.g., "فرمول محاسبه بازده مورد انتظار به شرح زیر است:"
    lines = [l.strip() for l in p_fa.split('\n') if l.strip()]
    intro_lines = []
    for line in lines:
        if any(bad in line for bad in ['\\begin', '\\end', '\\text', '\\frac', 'aligned', 'تراز شده', 'شروع', '=', '+', '-', '$$']):
            break
        # Has Persian characters and no math operators
        fa_chars = len(re.findall(r'[\u0600-\u06FF]', line))
        if fa_chars > 15:
            intro_lines.append(line)
            
    if intro_lines:
        intro = " ".join(intro_lines)
        return f"{intro}\n\n{clean_formula}"
    
    return clean_formula

def normalize_database():
    print(f"Loading {DICT_FILE}...")
    with open(DICT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converted_en = 0
    converted_fa = 0

    for item in data:
        for sec in item.get('sections', []):
            p_en_list = sec.get('paragraphs_en', [])
            p_fa_list = sec.get('paragraphs_fa', [])
            
            for idx in range(len(p_en_list)):
                p_en = p_en_list[idx]
                if any(k in p_en for k in ['\\begin{aligned}', '\\frac', '\\left(', '\\right)', '\\times', '\\sum', '\\sqrt']):
                    clean_en = clean_paragraph_with_formula(p_en)
                    if clean_en != p_en and clean_en.startswith('$$') and clean_en.endswith('$$'):
                        p_en_list[idx] = clean_en
                        converted_en += 1
                        
                        # Normalize corresponding Persian paragraph
                        if idx < len(p_fa_list):
                            clean_fa = clean_persian_formula_paragraph(p_fa_list[idx], clean_en)
                            p_fa_list[idx] = clean_fa
                            converted_fa += 1

    print(f"Normalized {converted_en} English formula paragraphs and {converted_fa} Persian formula paragraphs.")

    print(f"Saving updated {DICT_FILE}...")
    with open(DICT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Database updated successfully!")

if __name__ == '__main__':
    normalize_database()
