"""
Very lightweight keyword-based explainability layer.
This does NOT drive the prediction (TF-IDF + Logistic Regression does) —
it only turns the complaint text into human-readable reasons, matching
the "Explainable" design principle in the project spec.
"""

SYMPTOM_KEYWORDS = {
    "overheating": [
        ("panas", "High temperature reported"),
        ("mati", "Automatic shutdown reported"),
        ("kipas", "Fan noise / behavior mentioned"),
        ("lama", "Problem occurs after prolonged use"),
    ],
    "wifi_problem": [
        ("wifi", "WiFi connectivity mentioned"),
        ("konek", "Connection failure mentioned"),
        ("sinyal", "Signal issue mentioned"),
    ],
    "bluetooth_problem": [
        ("bluetooth", "Bluetooth mentioned"),
        ("pairing", "Pairing issue mentioned"),
        ("konek", "Connection issue mentioned"),
    ],
    "black_screen": [
        ("layar", "Screen/display mentioned"),
        ("hitam", "Black/blank screen reported"),
        ("nyala", "Device still powers on"),
    ],
    "display_flickering": [
        ("kedip", "Flickering reported"),
        ("garis", "Visual artifacts (lines) reported"),
        ("layar", "Screen/display mentioned"),
    ],
    "slow_performance": [
        ("lambat", "Slowness reported"),
        ("lemot", "Slowness reported"),
        ("lag", "Lag/freeze reported"),
        ("hang", "Freezing reported"),
    ],
    "boot_problem": [
        ("boot", "Boot failure mentioned"),
        ("windows", "OS startup issue mentioned"),
        ("restart", "Restart loop reported"),
    ],
    "battery_not_charging": [
        ("baterai", "Battery symptom mentioned"),
        ("charge", "Charging issue mentioned"),
        ("cas", "Charging issue mentioned"),
    ],
    "storage_problem": [
        ("penyimpanan", "Storage capacity/health mentioned"),
        ("hardisk", "Drive hardware mentioned"),
        ("disk", "Disk issue mentioned"),
    ],
    "keyboard_problem": [
        ("keyboard", "Keyboard issue mentioned"),
        ("tombol", "Key(s) not responding mentioned"),
        ("tidak berfungsi", "Non-responsive component reported"),
    ],
}


def build_reasoning(problem_code: str, complaint_text: str) -> list[str]:
    text = (complaint_text or "").lower()
    reasons = []
    for keyword, reason in SYMPTOM_KEYWORDS.get(problem_code, []):
        if keyword in text and reason not in reasons:
            reasons.append(reason)
    if not reasons:
        reasons.append("The overall pattern of your description matches this problem category.")
    return reasons
