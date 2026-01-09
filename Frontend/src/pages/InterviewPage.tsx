import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { apiPost } from "../lib/api";

interface QuestionDto {
  question_id: number;
  text: string;
}

interface InterviewStartResponse {
  interview_id: number;
  question: QuestionDto;
  conversation_url: string | null;
  tavus_error?: string | null;
}

function TavusFrame({ url }: { url: string }) {
  return (
    <iframe
      src={url}
      title="AI Interviewer"
      className="w-full h-full rounded-lg border-0"
      allow="camera; microphone; autoplay; encrypted-media; fullscreen;"
    />
  );
}

export function InterviewPage() {
  const { state } = useAuth();
  const navigate = useNavigate();

  const [interviewId, setInterviewId] = useState<number | null>(null);
  const [question, setQuestion] = useState<QuestionDto | null>(null);
  const [conversationUrl, setConversationUrl] = useState<string | null>(null);
  const [targetRole, setTargetRole] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tavusError, setTavusError] = useState<string | null>(null);

  useEffect(() => {
    if (!state.user) {
      navigate("/login");
    }
  }, [state.user, navigate]);

  async function handleStartInterview() {
    if (!state.user || !state.user.email || !state.user.name) {
      setError("You must be logged in and have a valid profile.");
      return;
    }

    setLoading(true);
    setError(null);
    setTavusError(null);

    try {
      const body = {
        candidate: {
          name: state.user.name,
          email: state.user.email,
          role: targetRole || state.user.role || "candidate",
          resume_summary: state.resumeSummary,
        },
        interviewer_id: 1,
        interview_type: targetRole || state.user.role || "candidate",
        skills: state.skills,
      };

      const data = await apiPost<InterviewStartResponse>(
        "/api/interview/start",
        body
      );

      setInterviewId(data.interview_id);
      setQuestion(data.question);
      setConversationUrl(data.conversation_url ?? null);
      setTavusError(data.tavus_error ?? null);
    } catch (err: any) {
      setError(err.message ?? "Failed to start interview");
    } finally {
      setLoading(false);
    }
  }

  const tavusKey = import.meta.env.VITE_TAVUS_PUBLIC_KEY as
    | string
    | undefined;

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header / controls */}
      <header className="w-full border-b border-zinc-800 px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Interview Room</h1>
          <p className="text-xs text-zinc-400">
            Logged in as {state.user?.email}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2">
            <label className="text-xs text-zinc-400">Target role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder={state.user?.role ?? "SDE Intern"}
              className="w-40 rounded-md bg-zinc-900 border border-zinc-700 px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <button
            onClick={handleStartInterview}
            disabled={loading}
            className="px-3 py-1.5 rounded-md bg-indigo-600 hover:bg-indigo-500 text-xs font-medium disabled:opacity-60"
          >
            {loading ? "Starting..." : conversationUrl ? "Restart" : "Start"}
          </button>
          <button
            className="text-xs text-zinc-300 hover:text-white underline"
            onClick={() => navigate("/profile")}
          >
            Edit profile
          </button>
        </div>
      </header>

      {/* Main 2-column layout: left 80% Tavus, right 20% chat */}
      <main className="flex-1 flex overflow-hidden">
        {/* Left: Tavus video area */}
        <section className="flex-[4] min-w-0 border-r border-zinc-800 flex flex-col">
          <div className="flex-1 p-4 flex flex-col gap-3">
            {tavusError && !conversationUrl && (
              <div className="rounded-xl border border-amber-600/40 bg-amber-950/30 px-4 py-3">
                <p className="text-sm text-amber-200 font-medium">
                  Avatar unavailable
                </p>
                <p className="text-xs text-amber-200/80 mt-1 break-words">
                  {tavusError}
                </p>
              </div>
            )}

            {!conversationUrl && (
              <div className="h-full flex items-center justify-center rounded-xl border border-dashed border-zinc-700 bg-zinc-950/40">
                <p className="text-sm text-zinc-400 max-w-sm text-center">
                  Click <span className="font-medium">Start</span> to launch the AI interviewer.
                </p>
              </div>
            )}

            {conversationUrl && (
              <div className="flex-1 rounded-xl overflow-hidden bg-black/40 border border-zinc-700">
                <TavusFrame url={conversationUrl} />
              </div>
            )}

            {question && (
              <div className="mt-3 bg-zinc-900 border border-zinc-700 rounded-xl p-3">
                <h2 className="text-sm font-semibold mb-1">Current Question</h2>
                <p className="text-sm text-zinc-100 mb-1">{question.text}</p>
                <p className="text-xs text-zinc-500">
                  Speak your answer to the avatar. This question is tracked for scoring in the backend.
                </p>
              </div>
            )}

            {interviewId && (
              <div className="mt-2 flex justify-end">
                <button
                  onClick={() => navigate(`/results/${interviewId}`)}
                  className="text-xs text-indigo-400 hover:text-indigo-300 underline"
                >
                  View results (after finishing)
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Right: chat sidebar */}
        <aside className="flex-[1] min-w-[260px] max-w-xs bg-zinc-950 border-l border-zinc-800 flex flex-col">
          <div className="px-4 py-3 border-b border-zinc-800">
            <h2 className="text-sm font-semibold">Notes / Chat</h2>
            <p className="text-[11px] text-zinc-500 mt-0.5">
              Use this panel to jot down points or future messages.
            </p>
          </div>
          <div className="flex-1 p-3 flex flex-col gap-2 overflow-y-auto text-xs">
            <div className="rounded-lg bg-zinc-900/70 border border-zinc-800 px-3 py-2 text-zinc-200">
              This is a placeholder chat area. Later, we can stream transcription
              or follow-up hints here.
            </div>
          </div>
          <div className="border-t border-zinc-800 p-3">
            <textarea
              rows={2}
              placeholder="Type notes or questions (not yet sent anywhere)..."
              className="w-full resize-none rounded-md bg-zinc-900 border border-zinc-700 px-2 py-1.5 text-xs text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </aside>
      </main>
    </div>
  );
}
