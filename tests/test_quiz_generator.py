from ai_cli.quiz_generator import generate_mcqs_from_text, MCQ


def test_generate_mcqs_from_text_basic():
    text = (
        "Python is a popular programming language used in many domains. "
        "Developers rely on Python for data science, automation, and web development. "
        "The language emphasizes readability and rapid prototyping."
    )

    mcqs = generate_mcqs_from_text(text, num_questions=5)
    assert isinstance(mcqs, list)
    assert mcqs, "Expected at least one MCQ to be generated."
    assert isinstance(mcqs[0], MCQ)
    assert len(mcqs[0].options) >= 4
    assert 0 <= mcqs[0].answer_index < len(mcqs[0].options)
