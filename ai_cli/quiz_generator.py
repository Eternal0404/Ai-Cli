"""
MCQ quiz generator from text or PDF content.
"""

import re
import random
from dataclasses import dataclass
from typing import List, Optional

from .utils import load_text_from_path, normalize_whitespace, split_sentences, STOPWORDS


@dataclass
class MCQ:
    question: str
    options: List[str]
    answer_index: int  # index into options list


def _select_answer_word(sentence: str, used_answers: set) -> Optional[str]:
    """
    Pick a candidate answer word from a sentence.
    Prefer longer, content-like words not used before.
    """
    tokens = re.findall(r"\w+", sentence)
    candidates = [
        t
        for t in tokens
        if len(t) > 3 and t.lower() not in STOPWORDS and t.lower() not in used_answers
    ]
    if not candidates:
        return None
    return random.choice(candidates)


def _build_question(sentence: str, answer: str) -> str:
    """
    Replace the answer word with a blank to form the question.
    """
    pattern = re.compile(rf"\b{re.escape(answer)}\b", flags=re.IGNORECASE)
    question = pattern.sub("____", sentence, count=1)
    return question


def _build_distractors(answer: str, vocabulary: List[str], k: int = 3) -> List[str]:
    """
    Build up to k distractors from a vocabulary list.
    Filters out the real answer and near-duplicates.
    """
    distractors: List[str] = []
    answer_lower = answer.lower()
    seen = {answer_lower}

    for token in vocabulary:
        token_lower = token.lower()
        if token_lower in seen:
            continue
        if len(token) <= 3 or token_lower in STOPWORDS:
            continue
        distractors.append(token)
        seen.add(token_lower)
        if len(distractors) >= k:
            break

    # If vocabulary is too small, synthesize simple distractors
    while len(distractors) < k:
        synthetic = f"{answer[:3]}{len(distractors) + 1}"
        if synthetic.lower() not in seen:
            distractors.append(synthetic)
            seen.add(synthetic.lower())

    return distractors[:k]


def generate_mcqs_from_text(text: str, num_questions: int = 5) -> List[MCQ]:
    """
    Generate MCQs directly from a text string.
    """
    text = normalize_whitespace(text)
    sentences = [s for s in split_sentences(text) if len(s.split()) >= 5]
    if not sentences:
        return []

    # Build a simple vocabulary for distractors
    vocab_tokens = re.findall(r"\w+", text)
    vocab_unique: List[str] = []
    seen = set()
    for token in vocab_tokens:
        token_lower = token.lower()
        if token_lower in seen or token_lower in STOPWORDS or len(token_lower) <= 3:
            continue
        seen.add(token_lower)
        vocab_unique.append(token)

    mcqs: List[MCQ] = []
    used_answers: set = set()

    for sentence in sentences:
        if len(mcqs) >= num_questions:
            break

        answer = _select_answer_word(sentence, used_answers)
        if not answer:
            continue

        question = _build_question(sentence, answer)
        if question == sentence:
            continue

        distractors = _build_distractors(answer, vocab_unique, k=3)
        options = distractors + [answer]
        random.shuffle(options)
        answer_index = options.index(answer)

        used_answers.add(answer.lower())
        mcqs.append(MCQ(question=question, options=options, answer_index=answer_index))

    return mcqs


def generate_mcqs_from_file(path: str, num_questions: int = 5) -> List[MCQ]:
    """
    Load text from a file and generate MCQs.
    """
    text = load_text_from_path(path)
    return generate_mcqs_from_text(text, num_questions=num_questions)
