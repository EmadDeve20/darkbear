class Colors:
    RED = "\033[91m"
    YELLOW = "\033[33m"
    WHITE = "\033[97m"
    DEFAULT = "\033[0m"

def report(rep_type: str, messgae: str):
    
    if rep_type == "suspicious":
        print(f"[{Colors.YELLOW}{rep_type}{Colors.DEFAULT}] {Colors.WHITE}{messgae}{Colors.DEFAULT}")
    if rep_type == "very suspicious":
        print(f"[{Colors.RED}{rep_type}{Colors.DEFAULT}] {Colors.WHITE}{messgae}{Colors.DEFAULT}")
