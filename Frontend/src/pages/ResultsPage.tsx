import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { apiGet } from "../lib/api";

interface InterviewSummaryItem {
  question: string;
  answer: string | null;
  relevance_score: number | null;
  confidence_level: number | null;
}

interface InterviewSummaryResponse {
  interview_id: number;
  overall_score: number | null;
  items: InterviewSummaryItem[];
  completed_at: string | null;
}

interface FeedbackResponse {
  feedback_id: number;
  interview_id: number;
  comments: string | null;
  suggestions: string | null;
  report_url: string | null;
}

export function ResultsPage() {
  const { interviewId } = useParams<{ interviewId: string }>();
  const navigate = useNavigate();
  const [summary, setSummary] = useState<InterviewSummaryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<FeedbackResponse | null>(null);

  useEffect(() => {
    if (!interviewId) return;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [summaryData, feedbackData] = await Promise.all([
          apiGet<InterviewSummaryResponse>(
            `/api/interview/${interviewId}/summary`,
          ),
          apiGet<FeedbackResponse>(
            `/api/interview/${interviewId}/feedback`,
          ),
        ]);

        setSummary(summaryData);
        setFeedback(feedbackData);
      } catch (err: any) {
        setError(err.message ?? "Failed to load summary");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [interviewId]);

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center">
      <div className="w-full max-w-4xl mt-10 mb-8 bg-zinc-900 border border-zinc-700 rounded-xl p-6 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-semibold">Interview Results</h1>
            <p className="text-sm text-zinc-400">
              Interview ID: {interviewId}
            </p>
          </div>
          <button
            onClick={() => navigate("/interview")}
            className="text-sm text-zinc-300 hover:text-white underline"
          >
            Back to dashboard
          </button>
        </div>

        {loading && <p className="text-sm text-zinc-400">Loading summary...</p>}
        {error && <p className="text-sm text-red-400">{error}</p>}

        {summary && (
          <>
            <div className="mb-4">
              <p className="text-sm text-zinc-300">
                Overall score: {summary.overall_score ?? "N/A"}
              </p>
            </div>

            <div className="space-y-3 text-sm">
              {summary.items.map((item, idx) => (
                <div
                  key={idx}
                  className="border border-zinc-700 rounded-lg p-3 bg-zinc-950/60"
                >
                  <p className="font-medium mb-1">Q{idx + 1}: {item.question}</p>
                  {item.answer && (
                    <p className="text-zinc-200 mb-1">
                      <span className="font-medium">Answer:</span> {item.answer}
                    </p>
                  )}
                  <p className="text-xs text-zinc-400">
                    Relevance: {item.relevance_score ?? "N/A"} / Confidence: {item.confidence_level ?? "N/A"}
                  </p>
                </div>
              ))}
            </div>

            {feedback && (
              <div className="mt-6 border-t border-zinc-800 pt-4">
                <h2 className="text-lg font-semibold mb-2">Detailed Feedback</h2>
                {feedback.comments && (
                  <div className="mb-3 text-sm text-zinc-200">
                    {feedback.comments}
                  </div>
                )}
                {feedback.suggestions && (
                  <div className="text-sm text-zinc-300">
                    <span className="font-semibold">Suggestions:</span> {feedback.suggestions}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
