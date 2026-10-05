export type Priority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | "UNKNOWN";

export interface TroubleshootingStep {
  step: number;
  title: string;
  description: string;
  warning?: string | null;
  is_advanced: boolean;
}

export interface FollowUpQuestion {
  id: string;
  question: string;
  options: string[];
}

export interface DiagnosisResult {
  problem: string | null;
  category: string | null;
  confidence: number;
  is_low_confidence: boolean;
}

export interface DiagnosisResponse {
  diagnosis_id: number | null;
  diagnosis: DiagnosisResult;
  priority: Priority;
  estimated_time: string;
  possible_causes: string[];
  reasoning: string[];
  troubleshooting_steps: TroubleshootingStep[];
  safety_warning?: string | null;
  follow_up_questions: FollowUpQuestion[];
  top_predictions: Record<string, number>;
}

export interface GuidedAnswer {
  question_id: string;
  answer: "Yes" | "No" | "Not sure";
}

export interface HistoryItem {
  diagnosis_id: number;
  complaint_text: string;
  problem_name: string | null;
  confidence: number;
  priority: Priority;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  description?: string | null;
}

export interface ProblemSummary {
  id: number;
  code: string;
  name: string;
  severity: Priority;
}

export interface TroubleshootingStepDetail {
  step_number: number;
  title: string;
  description: string;
  warning?: string | null;
}

export interface ProblemDetail extends ProblemSummary {
  description?: string | null;
  estimated_time_min: number;
  estimated_time_max: number;
  category?: Category | null;
  troubleshooting_steps: TroubleshootingStepDetail[];
}

export interface DashboardStats {
  total_diagnoses: number;
  resolved: number;
  high_priority: number;
  ai_accuracy: number | null;
  most_common_problems: { name: string; count: number; percentage: number }[];
}

export interface ServiceRecord {
  id: number;
  diagnosis_id: number;
  customer_name: string;
  device_model?: string | null;
  actual_diagnosis?: string | null;
  service_performed?: string | null;
  status: string;
  created_at: string;
}
