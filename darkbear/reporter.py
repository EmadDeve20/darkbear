class FontColors:
    RED = "\033[91m"
    YELLOW = "\033[33m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    DEFAULT = "\033[0m"

def report(rep_type: str, messgae: str):
    
    if rep_type == "suspicious":
        print(f"[{FontColors.YELLOW}{rep_type}{FontColors.DEFAULT}] {FontColors.WHITE}{messgae}{FontColors.DEFAULT}")
    if rep_type == "very suspicious":
        print(f"[{FontColors.RED}{rep_type}{FontColors.DEFAULT}] {FontColors.WHITE}{messgae}{FontColors.DEFAULT}")
    if rep_type == "not found":
        print(f"[{FontColors.GREEN}{rep_type}{FontColors.DEFAULT}] {FontColors.WHITE}{messgae}{FontColors.DEFAULT}")
