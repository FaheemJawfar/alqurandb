export default function TranslationsPage() {
  const translations = [
    {
      language: "English",
      translators: [
        { name: "Sahih International", available: true },
        { name: "Yusuf Ali", available: true },
        { name: "Pickthall", available: true },
        { name: "Dr. Mustafa Khattab", available: true }
      ]
    },
    {
      language: "Urdu",
      translators: [
        { name: "Maududi", available: true },
        { name: "Muhammad Junagarhi", available: true },
        { name: "Fateh Muhammad Jalandhry", available: true }
      ]
    },
    {
      language: "Arabic",
      translators: [
        { name: "Tafsir Ibn Kathir", available: false },
        { name: "Tafsir Al-Jalalayn", available: false }
      ]
    },
    {
      language: "French",
      translators: [
        { name: "Muhammad Hamidullah", available: false }
      ]
    },
    {
      language: "Spanish",
      translators: [
        { name: "Julio Cortes", available: false }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 py-16 px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-black dark:text-white mb-4">
            Translations
          </h1>
          <p className="text-xl text-zinc-600 dark:text-zinc-400 max-w-3xl">
            Access Quranic translations in multiple languages from renowned scholars and translators.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {translations.map((translation, index) => (
            <div
              key={index}
              className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700"
            >
              <h2 className="text-2xl font-bold text-black dark:text-white mb-4">
                {translation.language}
              </h2>
              <ul className="space-y-3">
                {translation.translators.map((translator, tIndex) => (
                  <li
                    key={tIndex}
                    className="flex items-center justify-between"
                  >
                    <span className="text-zinc-700 dark:text-zinc-300">
                      {translator.name}
                    </span>
                    {translator.available ? (
                      <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-sm rounded-full">
                        Available
                      </span>
                    ) : (
                      <span className="px-3 py-1 bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-400 text-sm rounded-full">
                        Coming Soon
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg p-8">
          <h3 className="text-xl font-bold text-black dark:text-white mb-2">
            Access via API
          </h3>
          <p className="text-zinc-700 dark:text-zinc-300 mb-4">
            All available translations can be accessed programmatically through our REST API.
          </p>
          <div className="bg-zinc-900 dark:bg-zinc-950 rounded-lg p-4 mb-4 overflow-x-auto">
            <code className="text-green-400 text-sm">
              GET /api/v1/ayah/{`{surah_number}`}/{`{ayah_number}`}?translation=sahih
            </code>
          </div>
          <a
            href="/api-docs"
            className="inline-block px-6 py-3 bg-black dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors"
          >
            View API Documentation
          </a>
        </div>
      </div>
    </div>
  );
}
