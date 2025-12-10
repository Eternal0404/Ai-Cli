from ai_cli.utils import summarize_text


def test_summarize_text_reduces_length():
    text = (
        "This is the first sentence of a small document. "
        "This is the second sentence, which adds more detail. "
        "Here is the third sentence describing additional context. "
        "Finally, this is the fourth sentence that concludes the text."
    )

    summary = summarize_text(text, max_sentences=2)
    assert isinstance(summary, str)
    assert len(summary) < len(text)
    # Should contain at most 2–3 sentence terminators
    assert summary.count(".") <= 3
