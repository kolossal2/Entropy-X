import math
import random
import string
import os
from zxcvbn import zxcvbn

def load_local_eff_wordlist(filepath="eff_large_wordlist.txt"):
    """
    Reads the EFF Large Wordlist from a local file.
    Expects lines formatted as: 11111\tword
    """
    if not os.path.exists(filepath):
        print(f"⚠️ Error: Local file '{filepath}' not found!")
        print("Please download it from: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt")
        print("Place it in the same directory as this script for offline passphrase generation.\n")
        return []

    words = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                words.append(parts[1])
    
    print(f"SUCCESS: Loaded {len(words)} words locally from '{filepath}'.\n")
    return words

def calculate_entropy_bits(guesses):
    """Converts zxcvbn guess count into information entropy bits."""
    if guesses <= 1:
        return 0.0
    return math.log2(guesses)

def format_summary(result):
    """Translates zxcvbn match metadata into a plain-English explanation."""
    sequence = result.get("sequence", [])
    matches = [match.get("pattern") for match in sequence]
    
    if result["score"] == 4:
        return "✅ Passed! High entropy with no predictable structural patterns."
    elif "dictionary" in matches or "spatial" in matches:
        return "⚠️ Vulnerable: Relies on dictionary words or keyboard row sequences (like 'qwerty')."
    elif "repeat" in matches or "sequence" in matches:
        return "⚠️ Vulnerable: Contains repeated characters or predictable numerical sequences."
    else:
        return "⚠️ Vulnerable: Needs more length or variance to resist brute-force guessing."

def audit_password(password):
    """Audits input password using zxcvbn and entropy calculations."""
    analysis = zxcvbn(password)
    score = analysis["score"]
    guesses = analysis["guesses"]
    entropy = calculate_entropy_bits(guesses)
    summary = format_summary(analysis)
    
    return {
        "password": password,
        "score": f"{score}/4",
        "entropy_bits": round(entropy, 2),
        "passed": score == 4,
        "summary": summary
    }

def generate_passphrase(wordlist, word_count=5, separator="-"):
    """Generates a human-readable passphrase using the local EFF wordlist."""
    if not wordlist:
        return None

    while True:
        candidate = separator.join(random.choice(wordlist) for _ in range(word_count))
        result = audit_password(candidate)
        if result["passed"]:
            return result

def generate_string_password(length=18):
    """Generates a high-entropy random character string password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    while True:
        candidate = "".join(random.
