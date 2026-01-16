
import re

# --- Base Processor ---

class LanguageProcessor:
    def __init__(self, name, rules=None):
        self.name = name
        self.rules = rules or {}

    def get_length(self, n):
        """Returns the 'length' of number n in this language."""
        raise NotImplementedError

# --- Specific Implementations ---

class WesternProcessor(LanguageProcessor):
    def get_name(self, n):
        """Generates the word name for a number."""
        if n > 999: return ""
        
        direct_rules = self.rules.get("direct", {})
        lang_name = self.name.lower()

        if n in direct_rules: return direct_rules[n]
        
        parts = []
        if n >= 100:
            h = n // 100
            rem = n % 100
            
            prefix = direct_rules.get(h, "")
            
            # Special case for German "ein" vs "eins"
            if "german" in lang_name and h == 1 and prefix == "eins":
                prefix = "ein"
            if "spanish" in lang_name and h == 1:
                prefix = ""
                
            parts.append(prefix)
            parts.append(self.rules.get("hundred", ""))
            
            if rem > 0:
                if self.rules.get("hundred_sep"): parts.append(self.rules["hundred_sep"])
                parts.append(self.get_name(rem))
            return "".join(parts)

        if n >= 20:
            t = n // 10
            rem = n % 10
            tens_rules = self.rules.get("tens", [])
            tens_val = ""
            if t < len(tens_rules):
                tens_val = tens_rules[t]
                
            if rem > 0:
                ten_sep = self.rules.get("ten_sep", "")
                if ten_sep in ["und", "و"]: # German, Arabic, etc.
                    unit_str = direct_rules.get(rem, "")
                    if "german" in lang_name and rem == 1 and unit_str == "eins":
                        unit_str = "ein"
                    parts.extend([unit_str, ten_sep, tens_val])
                else:
                    parts.append(tens_val)
                    if ten_sep: parts.append(ten_sep)
                    parts.append(direct_rules.get(rem, ""))
            else:
                parts.append(tens_val)
        
        return "".join(parts)

    def get_length(self, n):
        name = self.get_name(n)
        # Remove spaces and hyphens for length calculation
        return len(name.replace(" ", "").replace("-", ""))


class SumerianProcessor(LanguageProcessor):
    def get_length(self, n):
        """
        Calculates the number of Cuneiform signs for a Sumerian number (Base 60).
        Logic:
        0-59: Sum of signs for Tens (10,20,30,40,50) and Units (1-9).
        60+: Decomposed into multiples of 60.
        """
        if n == 0: return 0 # No zero in Sumerian
        
        # Check direct rules first
        direct_rules = self.rules.get("direct", {})
        if n in direct_rules: return len(direct_rules[n])

        # Decompose into Base 60: n = 60*h + Remainder
        h = n // 60
        rem = n % 60
        
        length = 0
        
        # Handle the '60's place (GESH)
        if h > 0:
            # Recursively get length for h (if h is 1, it's 1 GESH sign. If h=2, 2 GESH signs?)
            # Assuming h signs of GESH.
            length += self.get_length(h) 

        # Handle Remainder (0-59)
        if rem > 0:
            tens = (rem // 10) * 10
            units = rem % 10
            
            # Add Tens sign count
            if tens > 0:
                if tens in direct_rules:
                    length += len(direct_rules[tens])
                else:
                    # Check tens array
                    tens_idx = tens // 10
                    tens_rules = self.rules.get("tens", [])
                    if tens_idx < len(tens_rules) and tens_rules[tens_idx]:
                        length += len(tens_rules[tens_idx])
            
            # Add Units sign count
            if units > 0:
                if units in direct_rules:
                    length += len(direct_rules[units])

        return length


class HebrewProcessor(LanguageProcessor):
    def get_length(self, n):
        """
        Calculates the length of the Hebrew name for n, counting native letters.
        Uses the standard masculine form for abstract counting.
        """
        if n > 999: return 15 # Approximation for simplicity

        # Letter counts for native Hebrew spelling (masculine form)
        units_len = {
            0: 3,  # efes
            1: 3,  # echad
            2: 4,  # shnayim
            3: 4,  # shlosha
            4: 4,  # arba'a
            5: 4,  # chamisha
            6: 3,  # shisha
            7: 4,  # shiv'a
            8: 4,  # shmona
            9: 4   # tish'a
        }
        
        if n <= 10:
            if n in units_len: return units_len[n]
            if n == 10: return 3 # eser

        # Teens (e.g., achad-asar -> 3+3=6)
        if n < 20:
            u = n - 10
            # "asar" is 3 letters
            # Exceptions for 11 and 12 which have unique forms
            if n == 11: return 6 # achad-asar
            if n == 12: return 7 # shneim-asar
            # For 13-19, it's shlosha-asar, etc.
            return units_len[u] + 3

        # Tens (esrim, shloshim...)
        tens_len = {
            20: 4, 30: 5, 40: 5, 50: 5, 60: 4, 70: 5, 80: 5, 90: 5
        }
        if n < 100:
            t = (n // 10) * 10
            u = n % 10
            if u == 0: return tens_len[t]
            # e.g., "esrim ve'echad" -> ten_len + 1 (ve) + unit_len
            return tens_len[t] + 1 + units_len[u]

        # Hundreds
        # me'a (100) = 3, mata'yim (200) = 5, shlosh me'ot (300) = 3+4=7
        if n < 1000:
            h = n // 100
            rem = n % 100
            if rem == 0:
                if h == 1: return 3 # me'a
                if h == 2: return 5 # mata'yim
                return units_len[h] + 4 # shlosh me'ot
            
            hundred_base = 0
            if h == 1: hundred_base = 3
            elif h == 2: hundred_base = 5
            else: hundred_base = units_len[h] + 4
            
            return hundred_base + 1 + self.get_length(rem)

        return 0 # Fallback


class HebrewGematriaProcessor(LanguageProcessor):
    def __init__(self, name, rules=None):
        super().__init__(name, rules)
        self.gematria_map = {
            'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
            'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
            'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
            'ך': 20, 'ם': 40, 'ן': 50, 'ף': 80, 'ץ': 90 # Sofit forms
        }
        # Number names in Hebrew (Masculine)
        self.names = {
            0: "אפס", 1: "אחד", 2: "שנים", 3: "שלשה", 4: "ארבעה",
            5: "חמשה", 6: "ששה", 7: "שבעה", 8: "שמנה", 9: "תשעה",
            10: "עשר", 11: "אחד עשר", 12: "שנים עשר",
            13: "שלשה עשר", 14: "ארבעה עשר", 15: "חמשה עשר",
            16: "ששה עשר", 17: "שבעה עשר", 18: "שמנה עשר", 19: "תשעה עשר",
            20: "עשרים", 30: "שלשים", 40: "ארבעים", 50: "חמשים",
            60: "ששים", 70: "שבעים", 80: "שמנים", 90: "תשעים",
            100: "מאה", 200: "מאתים", 300: "שלש מאות", 400: "ארבע מאות",
            500: "חמש מאות", 600: "שש מאות", 700: "שבע מאות", 800: "שמנה מאות", 900: "תשע מאות"
        }

    def get_gematria(self, text):
        total = 0
        for char in text:
            total += self.gematria_map.get(char, 0)
        return total

    def get_hebrew_name(self, n):
        if n == 0: return self.names.get(0, "אפס")
        if n in self.names: return self.names[n]
        
        parts = []
        
        # Thousands
        if n >= 1000:
            thousands = n // 1000
            n = n % 1000
            if thousands == 1:
                parts.append("אלף")
            elif thousands == 2:
                parts.append("אלפיים")
            elif thousands < 10:
                parts.append(self.get_hebrew_name(thousands) + "ת אלפים")
            else:
                parts.append(self.get_hebrew_name(thousands) + " אלף")
        
        # Hundreds
        if n >= 100:
            hundreds = (n // 100) * 100
            n = n % 100
            if parts: parts.append("ו" + self.names[hundreds])
            else: parts.append(self.names[hundreds])
            
        # Tens and Units
        if n > 0:
            if n in self.names:
                if parts: parts.append("ו" + self.names[n])
                else: parts.append(self.names[n])
            else:
                tens = (n // 10) * 10
                units = n % 10
                if parts:
                    parts.append("ו" + self.names[tens])
                    parts.append("ו" + self.names[units])
                else:
                    parts.append(self.names[tens])
                    parts.append("ו" + self.names[units])
                    
        return " ".join(parts)

    def get_length(self, n):
        if n == 0: return 0
        name = self.get_hebrew_name(n)
        return self.get_gematria(name)


# --- Factory / Registry ---

PROCESSOR_REGISTRY = {
    "western": WesternProcessor,
    "sumerian": SumerianProcessor,
    "hebrew": HebrewProcessor,
    "hebrew_gematria": HebrewGematriaProcessor
}

def get_processor(math_type, lang_name, rules):
    processor_class = PROCESSOR_REGISTRY.get(math_type.lower(), WesternProcessor)
    return processor_class(lang_name, rules)
