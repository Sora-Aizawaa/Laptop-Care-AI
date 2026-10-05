import { useCallback, useState } from "react";
import { friendlyErrorMessage, postDiagnosis } from "../services/api";
import type { DiagnosisResponse, GuidedAnswer } from "../types/diagnosis";

export function useDiagnosis() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DiagnosisResponse | null>(null);
  const [originalComplaint, setOriginalComplaint] = useState<string>("");
  const [collectedAnswers, setCollectedAnswers] = useState<GuidedAnswer[]>([]);

  const analyze = useCallback(async (complaint: string) => {
    setLoading(true);
    setError(null);
    setOriginalComplaint(complaint);
    setCollectedAnswers([]);
    try {
      const data = await postDiagnosis(complaint, []);
      setResult(data);
    } catch (err) {
      setError(friendlyErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  const answerFollowUp = useCallback(
    async (questionId: string, answer: "Yes" | "No" | "Not sure") => {
      setLoading(true);
      setError(null);
      const nextAnswers = [...collectedAnswers, { question_id: questionId, answer }];
      setCollectedAnswers(nextAnswers);
      try {
        const data = await postDiagnosis(originalComplaint, nextAnswers);
        setResult(data);
      } catch (err) {
        setError(friendlyErrorMessage(err));
      } finally {
        setLoading(false);
      }
    },
    [collectedAnswers, originalComplaint]
  );

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
    setOriginalComplaint("");
    setCollectedAnswers([]);
  }, []);

  return { loading, error, result, analyze, answerFollowUp, reset };
}
