import re

with open("talmud_sample.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Hebrew/Aramaic range: U+0590 to U+05FF
hebrew_chars = re.findall(r'[\u0590-\u05FF]+', text)
hebrew_text = " ".join(hebrew_chars)

count = len(hebrew_text)
print(f"Found {len(hebrew_chars)} Hebrew/Aramaic word segments.")
print(f"Total Hebrew/Aramaic characters: {count}")
if count > 0:
    print(f"Sample: {hebrew_text[:100]}...")
else:
    print("No Hebrew/Aramaic text found in the sample.")
