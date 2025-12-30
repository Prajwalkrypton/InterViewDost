import { useNavigate } from "react-router-dom";

export function CodingDashboardPage() {
  const navigate = useNavigate();

  const questionCategories = [
    {
      name: "Arrays & Strings",
      description: "Master fundamentals like two pointers, sliding window, and hashing.",
      difficulty: "Beginner",
    },
    {
      name: "Linked Lists & Trees",
      description: "Practice pointer manipulation and recursive thinking.",
      difficulty: "Intermediate",
    },
    {
      name: "Dynamic Programming",
      description: "Tackle optimization problems with memoization and tabulation.",
      difficulty: "Advanced",
    },
  ];

  const quickSets = [
    { name: "Warmup (15 min)", items: 3 },
    { name: "Daily Set (45 min)", items: 5 },
    { name: "Mock Round (90 min)", items: 8 },
  ];

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <header className="w-full border-b border-zinc-800 px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Coding Prep Dashboard</h1>
          <p className="text-xs text-zinc-400">
            Sharpen your problem-solving before you hop into a mock interview.
          </p>
        </div>
        <button
          onClick={() => navigate("/interview")}
          className="text-xs px-3 py-1.5 rounded-md bg-indigo-600 hover:bg-indigo-500 font-medium"
        >
          Go to Interview Room
        </button>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-6 space-y-6">
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-xl p-4">
            <h2 className="text-lg font-semibold mb-2">Practice Tracks</h2>
            <p className="text-xs text-zinc-400 mb-4">
              Pick a topic to see curated questions (you can wire this up to a real
              question bank later).
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
              {questionCategories.map((cat) => (
                <div
                  key={cat.name}
                  className="bg-zinc-950/70 border border-zinc-800 rounded-lg p-3 flex flex-col gap-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{cat.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300">
                      {cat.difficulty}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-400">{cat.description}</p>
                  <button
                    className="mt-1 text-[11px] text-indigo-400 hover:text-indigo-300 underline text-left"
                    onClick={() => {}}
                  >
                    View questions (coming soon)
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 text-sm">
            <h2 className="text-lg font-semibold mb-2">Quick Practice Sets</h2>
            <p className="text-xs text-zinc-400 mb-3">
              Jump into a timed set when you have limited time.
            </p>
            <div className="space-y-2">
              {quickSets.map((set) => (
                <button
                  key={set.name}
                  className="w-full text-left px-3 py-2 rounded-lg bg-zinc-950/70 border border-zinc-800 hover:border-indigo-500 text-xs flex items-center justify-between"
                  onClick={() => {}}
                >
                  <div>
                    <div className="font-medium">{set.name}</div>
                    <div className="text-[11px] text-zinc-400">~{set.items} questions</div>
                  </div>
                  <span className="text-[11px] text-indigo-400">Start (stub)</span>
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 text-sm">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-semibold">Recent Activity</h2>
            <span className="text-[11px] text-zinc-500">Personal stats (coming soon)</span>
          </div>
          <p className="text-xs text-zinc-400">
            Later, this section can show solved questions, streaks, and weak areas
            based on your performance. For now, it is a static placeholder.
          </p>
        </section>
      </main>
    </div>
  );
}
