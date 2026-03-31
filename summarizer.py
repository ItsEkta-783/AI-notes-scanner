import re

def summarize_text(text):
    # Clean text
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # Split sentences
    sentences = text.split('.')

    # Filter useful sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    # Take top 3–5 lines
    summary = '. '.join(sentences[:4])

    return summary

def bullet_summary(text):
    sentences = text.split('.')
    points = [s.strip() for s in sentences if len(s.strip()) > 20]

    return points[:5]