import re

STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "saya", "adalah",
    "untuk", "pada", "dengan", "atau", "juga", "tidak", "ada", "akan",
    "sudah", "saat", "ketika", "karena", "jadi", "nya", "lalu", "kalau",
    "bisa", "tersebut", "sangat", "terus", "sama",
}


def clean_text(text: str) -> str:
    """Lowercase, strip punctuation/numbers, remove extra whitespace.
    Stopwords are intentionally NOT removed from the TF-IDF input because
    domain words like 'tidak' change meaning (e.g. 'tidak bisa konek');
    a light custom stopword list is kept here for optional experiments
    (see notebooks/model_experiment.ipynb).
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text: str) -> str:
    tokens = [t for t in text.split() if t not in STOPWORDS_ID]
    return " ".join(tokens)
