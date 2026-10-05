"""
Rule Engine
-----------
The ML model only predicts *what* the problem probably is.
This module decides *how urgent* it is and whether a safety warning
is needed — kept separate from the ML model so the system stays
controllable and explainable (see project spec section 4/17/18).
"""

PRIORITY_BY_SEVERITY = {
    "LOW": "LOW",
    "MEDIUM": "MEDIUM",
    "HIGH": "HIGH",
    "CRITICAL": "CRITICAL",
}

# Extra keyword-based escalation: if these words appear in the raw complaint,
# bump priority regardless of the base severity of the predicted problem.
CRITICAL_KEYWORDS = ["terbakar", "asap", "meledak", "smoke", "burnt", "bau hangus", "percikan api"]
HIGH_ESCALATION_KEYWORDS = ["mati total", "tidak bisa dipakai sama sekali", "berulang kali"]


def determine_priority(problem_severity: str, complaint_text: str) -> str:
    text = (complaint_text or "").lower()

    if any(kw in text for kw in CRITICAL_KEYWORDS):
        return "CRITICAL"

    priority = PRIORITY_BY_SEVERITY.get(problem_severity, "MEDIUM")

    if priority == "MEDIUM" and any(kw in text for kw in HIGH_ESCALATION_KEYWORDS):
        priority = "HIGH"

    return priority


def get_safety_warning(problem_code: str, priority: str) -> str | None:
    if priority == "CRITICAL":
        return (
            "Segera hentikan pemakaian laptop dan bawa ke teknisi profesional untuk "
            "pemeriksaan lebih lanjut. Kondisi ini berpotensi membahayakan keselamatan."
        )

    warnings = {
        "overheating": (
            "Jika laptop terasa sangat panas, berbau hangus, atau mati berulang kali, "
            "hentikan pemakaian dan periksakan ke teknisi."
        ),
        "battery_not_charging": (
            "Jika baterai menggembung, sangat panas, atau mengeluarkan bau aneh, "
            "hentikan pengisian daya dan hubungi teknisi."
        ),
        "boot_problem": (
            "Jangan memaksa restart berulang kali karena berisiko merusak data atau storage."
        ),
    }
    return warnings.get(problem_code)


def estimate_time_label(time_min: int, time_max: int) -> str:
    if time_min == time_max:
        return f"{time_min} minutes"
    if time_max >= 60:
        return f"{round(time_min/60, 1)}-{round(time_max/60, 1)} hours".replace(".0", "")
    return f"{time_min}-{time_max} minutes"
