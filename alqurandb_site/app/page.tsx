export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 font-sans dark:bg-zinc-900">
      <main className="w-full max-w-6xl mx-auto px-8 py-16">
        {/* Hero Section */}
        <div className="flex flex-col items-center gap-6 text-center mb-16">
          <div className="space-y-4">
            <h1 className="text-6xl font-bold tracking-tight text-black dark:text-white">
              AlQuranDB
            </h1>
            <p className="text-2xl text-zinc-600 dark:text-zinc-400 max-w-3xl">
              Your comprehensive resource center for Quranic data, translations, and downloadable resources
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-center">
            <h3 className="text-4xl font-bold text-black dark:text-white mb-2">114</h3>
            <p className="text-zinc-600 dark:text-zinc-400 text-lg">Surahs</p>
          </div>
          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-center">
            <h3 className="text-4xl font-bold text-black dark:text-white mb-2">6,236</h3>
            <p className="text-zinc-600 dark:text-zinc-400 text-lg">Ayahs</p>
          </div>
          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-center">
            <h3 className="text-4xl font-bold text-black dark:text-white mb-2">Multiple</h3>
            <p className="text-zinc-600 dark:text-zinc-400 text-lg">Translations</p>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg">
            <div className="text-3xl mb-4">📥</div>
            <h2 className="text-2xl font-bold text-black dark:text-white mb-3">
              Download Resources
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-4">
              Access and download Quranic text, translations, and related resources in various formats.
            </p>
            <a
              href="/downloads"
              className="text-black dark:text-white font-medium hover:underline"
            >
              Browse Downloads →
            </a>
          </div>

          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg">
            <div className="text-3xl mb-4">🔌</div>
            <h2 className="text-2xl font-bold text-black dark:text-white mb-3">
              API Access
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-4">
              Integrate Quranic data and translations into your applications using our REST API.
            </p>
            <a
              href="/api-docs"
              className="text-black dark:text-white font-medium hover:underline"
            >
              View API Documentation →
            </a>
          </div>

          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg">
            <div className="text-3xl mb-4">🌐</div>
            <h2 className="text-2xl font-bold text-black dark:text-white mb-3">
              Multiple Translations
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-4">
              Access translations of the Quran in multiple languages for better understanding.
            </p>
            <a
              href="/translations"
              className="text-black dark:text-white font-medium hover:underline"
            >
              Explore Translations →
            </a>
          </div>

          <div className="p-8 bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg">
            <div className="text-3xl mb-4">📖</div>
            <h2 className="text-2xl font-bold text-black dark:text-white mb-3">
              Browse & Read
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 mb-4">
              Read and study the Quran online with easy navigation through Surahs and Ayahs.
            </p>
            <a
              href="/surahs"
              className="text-black dark:text-white font-medium hover:underline"
            >
              Browse Surahs →
            </a>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/downloads"
              className="px-8 py-4 bg-black dark:bg-white text-white dark:text-black rounded-lg font-medium text-lg hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors"
            >
              Download Resources
            </a>
            <a
              href="/api-docs"
              className="px-8 py-4 border border-black dark:border-white text-black dark:text-white rounded-lg font-medium text-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              API Documentation
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
