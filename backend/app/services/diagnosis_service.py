import json

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.models import Complaint, Diagnosis
from app.database.seed_data import QUESTIONS_BY_CODE
from app.ml.predict import predict
from app.services import recommendation_service, rule_engine
from app.services.explanation_service import build_reasoning


def _build_follow_up_questions(problem_code: str, already_answered_ids: set[str]) -> list[dict]:
    questions = QUESTIONS_BY_CODE.get(problem_code, [])
    return [
        {"id": qid, "question": qtext, "options": ["Yes", "No", "Not sure"]}
        for qid, qtext in questions
        if qid not in already_answered_ids
    ]


def _augment_text_with_answers(base_text: str, answers: list) -> str:
    """Fold guided-mode yes/no answers back into the text so a second
    ML prediction pass can use the extra signal (very simple refinement:
    a 'yes' answer to a symptom question re-emphasizes that symptom)."""
    extra_words = []
    for ans in answers:
        if ans.answer.lower() == "yes":
            # crude keyword injection based on the question id
            extra_words.append(ans.question_id.replace("q_", "").replace("_", " "))
    if not extra_words:
        return base_text
    return f"{base_text} {' '.join(extra_words)}"


def diagnose(
    db: Session,
    complaint_text: str,
    answers: list | None = None,
    user_id: int | None = None,
) -> dict:
    answers = answers or []
    answered_ids = {a.question_id for a in answers}

    effective_text = _augment_text_with_answers(complaint_text or "", answers)
    ml_result = predict(effective_text)

    confidence = ml_result["confidence"]
    predicted_code = ml_result["prediction"]
    is_low_confidence = confidence < settings.LOW_CONFIDENCE_THRESHOLD

    # Persist the complaint (only once per conversation ideally; kept simple here)
    complaint = Complaint(
        user_id=user_id,
        complaint_text=complaint_text or "",
        answers_json=json.dumps([a.dict() for a in answers]) if answers else None,
    )
    db.add(complaint)
    db.flush()

    if is_low_confidence and not answers:
        # Ask follow-up questions instead of committing to a diagnosis yet
        follow_ups = _build_follow_up_questions(predicted_code, answered_ids)
        db.commit()
        return {
            "diagnosis_id": None,
            "diagnosis": {
                "problem": None,
                "category": None,
                "confidence": confidence,
                "is_low_confidence": True,
            },
            "priority": "UNKNOWN",
            "estimated_time": "N/A",
            "possible_causes": [],
            "reasoning": ["We need more information to determine the problem confidently."],
            "troubleshooting_steps": [],
            "safety_warning": None,
            "follow_up_questions": follow_ups,
            "top_predictions": dict(list(ml_result["probabilities"].items())[:3]),
        }

    problem = recommendation_service.get_problem_by_code(db, predicted_code)
    if problem is None:
        db.commit()
        return {
            "diagnosis_id": None,
            "diagnosis": {"problem": predicted_code, "category": None, "confidence": confidence, "is_low_confidence": is_low_confidence},
            "priority": "MEDIUM",
            "estimated_time": "N/A",
            "possible_causes": [],
            "reasoning": ["No knowledge-base entry found for this problem yet."],
            "troubleshooting_steps": [],
            "safety_warning": None,
            "follow_up_questions": [],
            "top_predictions": dict(list(ml_result["probabilities"].items())[:3]),
        }

    priority = rule_engine.determine_priority(problem.severity, complaint_text)
    safety_warning = rule_engine.get_safety_warning(problem.code, priority)
    steps = recommendation_service.build_troubleshooting_steps(problem)
    reasoning = build_reasoning(problem.code, complaint_text)

    diagnosis = Diagnosis(
        complaint_id=complaint.id,
        problem_id=problem.id,
        confidence=confidence,
        priority=priority,
        model_version=ml_result["model_version"],
        is_low_confidence=1 if is_low_confidence else 0,
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return {
        "diagnosis_id": diagnosis.id,
        "diagnosis": {
            "problem": problem.name,
            "category": problem.category.name if problem.category else None,
            "confidence": confidence,
            "is_low_confidence": is_low_confidence,
        },
        "priority": priority,
        "estimated_time": rule_engine.estimate_time_label(problem.estimated_time_min, problem.estimated_time_max),
        "possible_causes": problem.causes_list(),
        "reasoning": reasoning,
        "troubleshooting_steps": steps,
        "safety_warning": safety_warning,
        "follow_up_questions": [],
        "top_predictions": dict(list(ml_result["probabilities"].items())[:3]),
    }
