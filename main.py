import math
import random
import string
from zxcvbn import zxcvbn

# EFF Large Wordlist Sample (Shortened for fast standalone execution)
# For production, replace this array with the full 7,776-word EFF Large List file
EFF_LARGE_WORDLIST = [
    "abacus", "abdomen", "abdominal", "abide", "abiding", "ability", "ablaze", "able",
    "abnormal", "abrasive", "abrasion", "abroad", "abrupt", "absence", "absentee", "absentmind",
    "absorbent", "absorbing", "abstract", "absurd", "accent", "accept", "access", "accessible",
    "accident", "acclaim", "accommodate", "accompanist", "accompany", "accomplish", "accord", "accordion",
    "accountant", "accounting", "accuracy", "accurate", "acoustics", "acquire", "acreage", "acrobat",
    "acronym", "action", "activate", "activator", "active", "activism", "activist", "activity",
    "actress", "acts", "acuity", "acupuncture", "adaptable", "adapter", "adaptive", "addition",
    "beacon", "canyon", "falcon", "glacier", "harbor", "jungle", "lantern", "magnet", "nebula",
    "pebble", "quartz", "radar", "shadow", "timber", "vortex", "willow", "zenith", "alpine"
]

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

def generate_passphrase(word_count=5, separator="-"):
    """Generates a human-readable passphrase from the EFF Large Wordlist."""
    while True:
        candidate = separator.join(random.choice(EFF_LARGE_WORDLIST) for _ in range(word_count))
        result = audit_password(candidate)
        if result["passed"]:
            return result

def generate_string_password(length=18):
    """Generates a high-entropy random character string password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    while True:
        candidate = "".join(random.choice(alphabet) for _ in range(length))
        result = audit_password(candidate)
        if result["passed"]:
            return result

def main():
    print("==================================================")
    print("         ENTROPY-X BY kolossal2                   ")
    print("==================================================")
    print("Options:")
    print("  • Type any password to test its strength.")
    print("  • Type 'gen' to create a new password/passphrase.")
    print("  • Type 'exit' to quit.\n")

    while True:
        user_input = input("Entropy-X > ").strip()

        if user_input.lower() == "exit":
            print("\nExiting Entropy-X. Stay secure!")
            break

        if not user_input:
            continue

        # Option: Generate Password Choice
        if user_input.lower() == "gen":
            print("\nSelect Generator Mode:")
            print("  [1] Readable Passphrase (Best for Master Passwords)")
            print("  [2] Random Character Scramble (Best for App Vault Logins)")
            
            gen_choice = input("Choice (1/2) > ").strip()

            if gen_choice == "1":
                res = generate_passphrase()
                print("\n[ Generated 4/4 EFF Passphrase ]")
                print(f" Passphrase  : {res['password']}")
                print(f" Score       : {res['score']}")
                print(f" Entropy     : {res['entropy_bits']} bits")
                print(f" Summary     : {res['summary']}\n")
            elif gen_choice == "2":
                res = generate_string_password()
                print("\n[ Generated 4/4 Character Scramble Password ]")
                print(f" Password    : {res['password']}")
                print(f" Score       : {res['score']}")
                print(f" Entropy     : {res['entropy_bits']} bits")
                print(f" Summary     : {res['summary']}\n")
            else:
                print("❌ Invalid option selected. Returning to main menu.\n")

        # Option: Test typed password
        else:
            res = audit_password(user_input)
            print("\n[ Password Analysis ]")
            print(f" Score       : {res['score']}")
            print(f" Entropy     : {res['entropy_bits']} bits")
            print(f" Gatekeeper  : {'GRANTED ✅' if res['passed'] else 'REJECTED ❌'}")
            print(f" Summary     : {res['summary']}\n")

if __name__ == "__main__":
    main()
