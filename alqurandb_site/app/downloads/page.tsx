export default function DownloadsPage() {
  const resources = [
    {
      title: "Complete Quran - Arabic Text",
      description: "Full Arabic text of the Quran in UTF-8 encoding",
      formats: ["JSON", "XML", "CSV", "TXT"],
      size: "~2.5 MB"
    },
    {
      title: "English Translation",
      description: "Multiple English translations including Sahih International, Yusuf Ali, and Pickthall",
      formats: ["JSON", "XML", "CSV"],
      size: "~5 MB"
    },
    {
      title: "Urdu Translation",
      description: "Popular Urdu translations of the Holy Quran",
      formats: ["JSON", "XML"],
      size: "~6 MB"
    },
    {
      title: "Surah Metadata",
      description: "Information about all 114 Surahs including names, revelation place, and verse counts",
      formats: ["JSON", "CSV"],
      size: "~50 KB"
    },
    {
      title: "Audio Recitations",
      description: "Links to audio recitations by famous reciters",
      formats: ["JSON"],
      size: "~100 KB"
    }
  ];

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 py-16 px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-black dark:text-white mb-4">
            Download Resources
          </h1>
          <p className="text-xl text-zinc-600 dark:text-zinc-400 max-w-3xl">
            Access and download Quranic data in various formats for your projects, research, or personal use.
          </p>
        </div>

        <div className="space-y-6">
          {resources.map((resource, index) => (
            <div
              key={index}
              className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700"
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-black dark:text-white mb-2">
                    {resource.title}
                  </h2>
                  <p className="text-zinc-600 dark:text-zinc-400 mb-4">
                    {resource.description}
                  </p>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-zinc-500 dark:text-zinc-500">
                      Size: {resource.size}
                    </span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  {resource.formats.map((format) => (
                    <button
                      key={format}
                      className="px-4 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors"
                    >
                      Download {format}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-8">
          <h3 className="text-xl font-bold text-black dark:text-white mb-2">
            Need programmatic access?
          </h3>
          <p className="text-zinc-700 dark:text-zinc-300 mb-4">
            Use our REST API to integrate Quranic data directly into your applications.
          </p>
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
