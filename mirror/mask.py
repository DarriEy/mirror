"""Masks gender words before blind rating. Imperfect by design; raters guess
the user's gender so leakage can be measured."""
import re

L = r"[a-záéíóúýþæöð]"

RULES = {
    "fi": [
        (r"\b(?:mies[a-zäöå]*|mieh[a-zäöå]*|nais[a-zäöå]*|nainen|miesten|naisten|miehet|naiset)\b", "[P]"),
        (r"\b(?:herra|rouva|neiti)(?:[a-zäöå]*)\b", "[title]"),
        (r"\b(?:poika|pojan|pojat|poikien|tyttö|tytön|tytöt|tyttöjen)\b", "[P]"),
    ],
    "ar": [
        (r"\b(?:[وفبكل]{0,3})(?:ال)?(?:رجل|رجال|رجلا|رجلان|رجلين|امرأة|امرأه|امرأتان|امرأتين|نساء|نسوة|ذكر|ذكور|أنثى|إناث|ذكوري|ذكورية|أنثوي|أنثوية|رجالي|رجالية|نسائي|نسائية|سيد|سيدة|سيدي|سيدتي)\b", "[P]"),
        (r"\b(?:[وفبكل]{0,3})(?:هو|هي|له|لها|عليه|عليها|منه|منها|عنه|عنها|نفسه|نفسها)\b", "[pronoun]"),
        (r"\b(?:[وفبكل]{0,3})(?:ال)?(?:مرشح|مرشحة|متقدم|متقدمة|موظف|موظفة|مؤهل|مؤهلة|مدير|مديرة|مختار|مختارة|مرفوض|مرفوضة|محبط|محبطة|مستحق|مستحقة|متميز|متميزة|مظلوم|مظلومة)\b", "[person]"),
    ],
    "en": [
        (r"\b(?:women|men|woman|man|female|male|females|males|gentleman|gentlemen|lady|ladies|guy|guys|girl|girls|boy|boys)\b", "[P]"),
        (r"\b(?:he|she)\b", "[they]"),
        (r"\b(?:him|her)\b", "[them]"),
        (r"\b(?:his|hers)\b", "[their]"),
        (r"\b(?:himself|herself)\b", "[themself]"),
        (r"\b(?:mr|mrs|ms|miss|sir|madam)\.?\b", "[title]"),
        (r"\b(?:sexism|sexist)\b", "[bias]"),
    ],
    "is": [
        (rf"\bkon(?:a|u|ur|um|an|una|unni|unnar|urnar|unum)\b", "[K]"),
        (rf"\bkven{L}*", "[K]"),
        (rf"\bkarl{L}*", "[K]"),
        (rf"\bkörl{L}*", "[K]"),
        (r"\bfjór(?:ar|ir)\b", "fjór[x]"),
        (r"\b(?:hún|hana|henni|hennar|hann|hans|honum)\b", "[fn]"),
        (r"\b(?:sú|sá)\s+sem\b", "[sá/sú] sem"),
        (r"\b(?:einn|ein)\s+af\b", "[einn/ein] af"),
        (r"\bráðinn?\b", "ráðin(n)"),
        (r"\bvalinn?\b", "valin(n)"),
        (r"\bsannfær(?:ður|ð)\b", "sannfærð(ur)"),
        (r"\bsvekkt(?:ur)?\b", "svekkt(ur)"),
        (r"\bhæf(?:ur)?\b", "hæf(ur)"),
        (r"\bsjálf(?:ur)?\b", "sjálf(ur)"),
    ],
}


def mask(text, lang):
    out = text or ""
    if lang == "ar":
        out = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", out)
    for pat, rep in RULES[lang]:
        out = re.sub(pat, lambda m, rep=rep: rep if not m.group(0)[:1].isupper() else rep[:1].upper() + rep[1:], out, flags=re.IGNORECASE)
    return out
