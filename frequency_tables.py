# Language Frequency Tables (Most Common to Least Common)

TABLES = {
    "American English": "etaoinshrdlcumwfgypbvkjxqz",
    "French": "easnruliodptcvmqfbghjxyzwk",
    "German": "enisratdhulcgmobwfkzvjpqy",
    "Spanish": "eaosrnidltcum pbgvyqhfzjkñxw",
    "Arabic": "ا ل ي و ه م ن ر ت ب ד כ ע ק פ צ ג ז ח ט י ל מ נ ס ע פ צ ק ר ש ת", # Simplified search results
    "Russian": "оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъ",
    "Italian": "eaiolnstcrdupmvghfbqzkjxyw",
    "Hebrew": "יהו אל ר מ ש ת ב כ ד ע ק פ צ ג ז ח ט", # Primary characters
    "Japanese": "のいたにてとしはなるをかっでもがうられまそりこくんあす", # Hiragana
    "Ancient Sumerian": "" # Not alphabetic, will use sign count or default to 1
}

def get_weight_map(lang_name):
    order = TABLES.get(lang_name, "")
    if not order:
        return {}
    return {char: i + 1 for i, char in enumerate(order)}
