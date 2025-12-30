export function CommunityDashboardPage() {
  const threads = [
    {
      title: "How did your last SDE interview go?",
      author: "Anonymous",
      replies: 8,
      tag: "Experience",
    },
    {
      title: "Best resources for system design prep?",
      author: "Arjun",
      replies: 14,
      tag: "Resources",
    },
    {
      title: "Share your most unexpected interview question",
      author: "Neha",
      replies: 5,
      tag: "Fun",
    },
  ];

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <header className="w-full border-b border-zinc-800 px-6 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Community Hub</h1>
          <p className="text-xs text-zinc-400">
            Connect with other candidates, share experiences, and learn together.
          </p>
        </div>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-6 grid grid-cols-1 lg:grid-cols-3 gap-6 text-sm">
        <section className="lg:col-span-2 bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex flex-col gap-3">
          <div className="flex items-center justify-between mb-1">
            <h2 className="text-lg font-semibold">Recent Discussions</h2>
            <button className="text-[11px] px-2 py-1 rounded-md bg-indigo-600 hover:bg-indigo-500 font-medium">
              New Post (stub)
            </button>
          </div>
          <p className="text-xs text-zinc-400 mb-2">
            This is a lightweight social space. You can later hook this into a real
            backend (Supabase, Firestore, etc.) for persistent threads.
          </p>

          <div className="space-y-2">
            {threads.map((t) => (
              <div
                key={t.title}
                className="bg-zinc-950/70 border border-zinc-800 rounded-lg p-3 flex flex-col gap-1"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-medium text-sm">{t.title}</h3>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300">
                    {t.tag}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-500">
                  Started by {t.author} • {t.replies} replies
                </p>
                <button className="mt-1 text-[11px] text-indigo-400 hover:text-indigo-300 underline text-left">
                  Open thread (stub)
                </button>
              </div>
            ))}
          </div>
        </section>

        <aside className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex flex-col gap-3">
          <div>
            <h2 className="text-sm font-semibold mb-1">Channels</h2>
            <ul className="text-xs text-zinc-300 space-y-1">
              <li># general-interviews</li>
              <li># coding-rounds</li>
              <li># system-design</li>
              <li># off-campus</li>
            </ul>
          </div>

          <div>
            <h2 className="text-sm font-semibold mb-1">Tips of the day</h2>
            <p className="text-xs text-zinc-400">
              • After each mock interview, write down 3 things you did well and 3 things to improve.
              <br />• Practice out loud, not just in your head.
            </p>
          </div>

          <div>
            <h2 className="text-sm font-semibold mb-1">Coming soon</h2>
            <p className="text-xs text-zinc-400">
              Live rooms, peer mock interviews, and profile sharing are easy next steps.
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
}
