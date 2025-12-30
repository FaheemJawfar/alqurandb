# Metadata.json Data Quality Analysis Report

**Date:** 2025-12-30
**File:** `/home/faheem/Projects/alqurandb/alqurandb_api/data/metadata.json`
**Total Translations:** 178

---

## Executive Summary

The metadata.json file contains 178 Quran translation entries from 4 different sources. The analysis revealed **NO critical issues** (like duplicate IDs), but found **several data quality inconsistencies** that should be addressed for standardization and maintainability.

### Overall Health: **Good** ✓
- No duplicate IDs
- All entries have required fields
- Source consistency is good

### Issues Found: **12 categories**
- Language naming inconsistencies (8 languages affected)
- Unknown translators (4 entries)
- HTML entities not decoded (9 entries)
- Potential duplicate translators (2 cases)
- Minor formatting issues

---

## 1. Duplicate IDs

**Status:** ✓ **PASS**

No duplicate IDs found. All 178 translation IDs are unique.

---

## 2. Duplicate Language+Translator Combinations

**Status:** ⚠️ **1 ISSUE FOUND**

### Found 1 duplicate combination:

#### Chinese - Ma Jian
- **ID 1:** `chinese_jian`
- **ID 2:** `chinese_majian`
- **Translator:** Ma Jian (same person)
- **Issue:** Same language and translator with different IDs
- **Note:** One appears to be simplified, other traditional Chinese (based on name_in_language: "Ma Jian" vs "Ma Jian (Traditional)")

**Recommendation:** These appear to be different versions (simplified vs traditional) of the same translator's work. The metadata should clarify this distinction in the language field or add a variant field.

---

## 3. Language Naming Inconsistencies

**Status:** ⚠️ **8 LANGUAGES AFFECTED**

The following languages have inconsistent naming patterns (some with "Translation" suffix, some without):

### 3.1 Bosnian (4 translations)
- **Variant 1:** "Bosnian" (2 translations)
  - `bosnian_korkut` (tanzil.net)
  - `bosnian_mlivo` (tanzil.net)
- **Variant 2:** "Bosnian Translation" (2 translations)
  - `bosnian_mihanovich` (quranenc.com)
  - `bosnian_rwwad` (quranenc.com)

### 3.2 Chinese (4 translations)
- **Variant 1:** "Chinese" (3 translations)
  - `chinese_jian` (tanzil.net)
  - `chinese_majian` (tanzil.net)
  - `chinese_suliman` (quranenc.com)
- **Variant 2:** "Chinese Translation" (1 translation)
  - `chinese_makin` (quranenc.com)

### 3.3 English (20 translations)
- **Variant 1:** "English" (18 translations from tanzil.net + 1 from quranenc.com)
- **Variant 2:** "English Translation" (2 translations from quranenc.com)
  - `english_hilali_khan`
  - `english_saheeh`

### 3.4 Filipino (2 translations)
- **Variant 1:** "Filipino (Bisayan)" (1 translation)
  - `bisayan_rwwad`
- **Variant 2:** "Filipino (Tagalog)- Rowwad Translation Center" (1 translation)
  - `tagalog_rwwad` ⚠️ **Contains translator name in language field**

### 3.5 Indonesian (6 translations)
- **Variant 1:** "Indonesian" (5 translations)
- **Variant 2:** "Indonesian Translation" (1 translation)
  - `indonesian_sabiq`

### 3.6 Somali (2 translations)
- **Variant 1:** "Somali" (1 translation)
  - `somali_abduh`
- **Variant 2:** "Somali Translation" (1 translation)
  - `somali_yacob`

### 3.7 Spanish (5 translations)
- **Variant 1:** "Spanish" (4 translations)
- **Variant 2:** "Spanish (Latin)" (1 translation)
  - `spanish_montada_latin`

### 3.8 Turkish (13 translations)
- **Variant 1:** "Turkish" (12 translations)
- **Variant 2:** "Turkish Translation" (1 translation)
  - `turkish_shaban`

**Pattern Observed:**
- tanzil.net entries typically use simple language name (e.g., "English")
- quranenc.com entries inconsistently use either "Language" or "Language Translation"

**Recommendation:** Standardize to one format. Suggest using simple language name without "Translation" suffix for consistency with tanzil.net entries.

---

## 4. Missing or Inconsistent Fields

**Status:** ✓ **PASS**

All translations have the required fields:
- `id`
- `language`
- `translator`
- `name_in_language`
- `source`

---

## 5. Source Consistency

**Status:** ✓ **GOOD** (with notes)

### 5.1 Source Distribution
| Source | Count | Has source_id | Without source_id |
|--------|-------|---------------|-------------------|
| tanzil.net | 111 | 111 | 0 |
| quranenc.com | 64 | 0 | 64 |
| tamililquran.com | 2 | 2 | 0 |
| acju.lk | 1 | 1 | 0 |

### 5.2 Source Field Patterns

**tanzil.net entries:**
- ✓ All 111 entries have `source_id` field
- ✓ Consistent format
- Example: `source_id: "en.sahih"`

**quranenc.com entries:**
- ✓ None have `source_id` field (consistent)
- All use pattern: "Language translation - Translator" in `name_in_language`

**tamililquran.com entries:**
- ✓ Both have `source_id` field
- Format: `source_id: "ift"`, `source_id: "king_fahd"`

**acju.lk entries:**
- ✓ Has `source_id` field
- Format: `source_id: "acju"`

**Conclusion:** Source consistency is good. Each source follows its own pattern consistently.

---

## 6. Invalid or Suspicious Values

**Status:** ⚠️ **4 CRITICAL ISSUES**

### 6.1 Unknown Translators (4 entries)

These entries have translator marked as "Unknown" and need proper attribution:

1. **asante_harun**
   - Language: "Akan Translation (Asante)- Harun Ismail"
   - Issue: Language field contains translator name, but translator field says "Unknown"
   - Name in language: "Akan Translation (Asante)- Harun Ismail"
   - Source: quranenc.com
   - **FIX:** Set translator to "Harun Ismail" and language to "Akan (Asante)"

2. **tagalog_rwwad**
   - Language: "Filipino (Tagalog)- Rowwad Translation Center"
   - Issue: Language field contains translator name, but translator field says "Unknown"
   - Name in language: "Filipino (Tagalog) translation- Rowwad Translation Center"
   - Source: quranenc.com
   - **FIX:** Set translator to "Rowwad Translation Center" and language to "Filipino (Tagalog)"

3. **japanese_standard**
   - Language: "Japanese"
   - Name in language: "Japanese"
   - Source: tanzil.net
   - Source ID: ja.japanese
   - **FIX:** Research actual translator from tanzil.net source

4. **korean_standard**
   - Language: "Korean"
   - Name in language: "Korean"
   - Source: tanzil.net
   - Source ID: ko.korean
   - **FIX:** Research actual translator from tanzil.net source

---

## 7. HTML Entities Not Decoded

**Status:** ⚠️ **9 ENTRIES**

The following entries contain `&amp;` HTML entity that should be decoded to `&`:

1. **amharic_sadiq** - `ሳዲቅ &amp; ሳኒ ሐቢብ`
2. **azerbaijani_mammadaliyev** - `Məmmədəliyev &amp; Bünyadov`
3. **english_hilali** - `Hilali &amp; Khan`
4. **english_qaribullah** - `Qaribullah &amp; Darwish`
5. **german_bubenheim** - `Bubenheim &amp; Elyas`
6. **hindi_farooq** - `फ़ारूक़ ख़ान &amp; अहमद`
7. **hindi_khan_nadwi** - `फ़ारूक़ ख़ान &amp; नदवी`
8. **malayalam_abdulhameed** - `അബ്ദുല്‍ ഹമീദ് &amp; പറപ്പൂര്‍`
9. **malayalam_karakunnu** - `കാരകുന്ന് &amp; എളയാവൂര്`

**Recommendation:** Replace all `&amp;` with `&` in the `name_in_language` field.

---

## 8. Potential Duplicate Translators

**Status:** ⚠️ **2 CASES**

### 8.1 Swahili - Al-Barwani/Al-Berwani (90.48% similarity)

**Likely the SAME person with different name spellings:**

- **Entry 1:** `swahili_barwani`
  - Language: Swahili
  - Translator: "Ali Muhsin Al-Barwani"
  - Source: tanzil.net

- **Entry 2:** `swahili_barawani`
  - Language: Swahili
  - Translator: "Ali Muhsen Al-Berwani"
  - Source: quranenc.com

**Differences:**
- Muhsin vs Muhsen
- Al-Barwani vs Al-Berwani
- Different sources

**Recommendation:** Verify if these are the same person. If yes, standardize the name. The correct spelling appears to be "Ali Muhsin Al-Barwani" based on common usage.

### 8.2 Indonesian - Ministry of Religious Affairs (84.06% similarity)

- **Entry 1:** `indonesian_ministry`
  - Translator: "Indonesian Ministry of Religious Affairs"
  - Source: tanzil.net

- **Entry 2:** `indonesian_affairs`
  - Translator: "Ministry of Religious Affairs"
  - Source: quranenc.com

**Recommendation:** Standardize to "Indonesian Ministry of Religious Affairs" for both entries.

---

## 9. Translator Name Formatting Issues

**Status:** ⚠️ **5 ENTRIES**

### 9.1 Trailing Spaces (5 entries)

The following translators have trailing spaces that should be removed:

1. **dutch_keyzer** - `'Salomo Keyzer '`
2. **hindi_farooq** - `'Muhammad Farooq Khan and Muhammad Ahmed  '` (also has double space)
3. **portuguese_elhayek** - `'Samir El-Hayek '`
4. **spanish_cortes** - `'Julio Cortes '`
5. **urdu_najafi** - `'Muhammad Hussain Najafi '`

**Recommendation:** Trim all translator fields to remove leading/trailing whitespace.

---

## 10. ID Naming Inconsistency

**Status:** ⚠️ **1 ISSUE**

### Dash in ID

- **russian_kuliev-alsaadi** - Uses dash instead of underscore

**Observation:** All other IDs use underscore as separator. This single entry uses a dash.

**Recommendation:** Either:
1. Keep as-is if the dash is intentional to represent the compound nature
2. Change to `russian_kuliev_alsaadi` for consistency

---

## 11. Language Field Contains Translator Info

**Status:** ⚠️ **1 CRITICAL ISSUE**

- **tagalog_rwwad**
  - Language field: "Filipino (Tagalog)- Rowwad Translation Center"
  - Translator field: "Unknown"

**Recommendation:** Move "Rowwad Translation Center" to translator field and clean up language field to "Filipino (Tagalog)".

---

## 12. Akan Translation Issue

**Status:** ⚠️ **1 ISSUE**

- **asante_harun**
  - Language: "Akan Translation (Asante)- Harun Ismail"
  - Translator: "Unknown"

Similar to tagalog_rwwad issue.

**Recommendation:** Set translator to "Harun Ismail" and language to "Akan (Asante)".

---

## Field Structure Analysis

**Status:** ✓ **CONSISTENT**

There are 2 field structures, both valid:

### Structure 1 (114 entries)
Fields: `id`, `language`, `name_in_language`, `source`, `source_id`, `translator`

Used by: tanzil.net, tamililquran.com, acju.lk

### Structure 2 (64 entries)
Fields: `id`, `language`, `name_in_language`, `source`, `translator`

Used by: quranenc.com (no source_id field)

**This is expected and correct.**

---

## Summary Statistics

### Languages with Most Translations
1. English: 18 translations
2. Persian: 14 translations
3. Turkish: 12 translations
4. Russian: 9 translations
5. Urdu: 8 translations
6. Indonesian: 5 translations
7. Tamil: 5 translations
8. Dutch: 4 translations
9. German: 4 translations
10. Spanish: 4 translations

### Sources
- **tanzil.net:** 111 translations (62.4%)
- **quranenc.com:** 64 translations (36.0%)
- **tamililquran.com:** 2 translations (1.1%)
- **acju.lk:** 1 translation (0.6%)

---

## Recommendations for Cleanup

### Priority 1: Critical Issues (Must Fix)

1. **Fix 4 "Unknown" translator entries**
   - `asante_harun` → Translator: "Harun Ismail", Language: "Akan (Asante)"
   - `tagalog_rwwad` → Translator: "Rowwad Translation Center", Language: "Filipino (Tagalog)"
   - `japanese_standard` → Research actual translator
   - `korean_standard` → Research actual translator

2. **Remove HTML entities (9 entries)**
   - Replace all `&amp;` with `&` in name_in_language field

3. **Remove trailing spaces from 5 translator names**

### Priority 2: Data Quality (Should Fix)

4. **Standardize language naming**
   - Remove "Translation" suffix inconsistencies
   - Recommend: Use simple language name (e.g., "English" not "English Translation")
   - Affects: Bosnian (2), Chinese (1), English (2), Indonesian (1), Somali (1), Turkish (1)

5. **Verify duplicate translators**
   - Swahili: Verify if Al-Barwani/Al-Berwani are same person
   - Indonesian: Standardize Ministry of Religious Affairs name

6. **Fix Chinese Ma Jian entries**
   - Clarify that one is simplified, other is traditional
   - Consider updating language field to "Chinese (Simplified)" and "Chinese (Traditional)"

### Priority 3: Consistency (Nice to Have)

7. **Review ID naming convention**
   - Decide on `russian_kuliev-alsaadi` dash vs underscore

8. **Add metadata version field**
   - Consider adding a schema version field for future tracking

---

## Proposed Fixes (JSON snippets)

### Fix 1: asante_harun
```json
{
  "id": "asante_harun",
  "language": "Akan (Asante)",
  "translator": "Harun Ismail",
  "name_in_language": "Akan (Asante) translation - Harun Ismail",
  "source": "quranenc.com"
}
```

### Fix 2: tagalog_rwwad
```json
{
  "id": "tagalog_rwwad",
  "language": "Filipino (Tagalog)",
  "translator": "Rowwad Translation Center",
  "name_in_language": "Filipino (Tagalog) translation - Rowwad Translation Center",
  "source": "quranenc.com"
}
```

### Fix 3: Swahili standardization
```json
{
  "id": "swahili_barawani",
  "language": "Swahili",
  "translator": "Ali Muhsin Al-Barwani",
  "name_in_language": "Swahili translation - Ali Muhsin Al-Barwani",
  "source": "quranenc.com"
}
```

### Fix 4: Indonesian Ministry standardization
```json
{
  "id": "indonesian_affairs",
  "language": "Indonesian",
  "translator": "Indonesian Ministry of Religious Affairs",
  "name_in_language": "Indonesian translation - Indonesian Ministry of Religious Affairs",
  "source": "quranenc.com"
}
```

---

## Conclusion

The metadata.json file is in **good overall condition** with no critical structural issues. The main areas for improvement are:

1. **4 entries** with "Unknown" translators that need research and updating
2. **9 entries** with HTML entities that need decoding
3. **Language naming standardization** across 8 languages
4. **Minor formatting issues** (trailing spaces, etc.)

**Estimated cleanup effort:** 2-3 hours for a developer familiar with the project.

**Risk level of changes:** LOW - These are data quality improvements with no breaking changes.

---

**Report Generated:** 2025-12-30
**Analyst:** Claude Sonnet 4.5
