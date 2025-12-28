export default function AboutPage() {
  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 py-16 px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold text-black dark:text-white mb-8">
          About AlQuranDB
        </h1>

        <div className="space-y-6">
          <div className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700">
            <h2 className="text-2xl font-bold text-black dark:text-white mb-4">
              Our Mission
            </h2>
            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed mb-4">
              AlQuranDB is a comprehensive resource center dedicated to making the Holy Quran accessible to everyone
              through modern technology. We provide Quranic data, translations, and downloadable resources for
              developers, researchers, students, and anyone seeking to understand the Quran.
            </p>
            <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">
              Our goal is to facilitate the study, understanding, and dissemination of Quranic knowledge through
              easy-to-use digital tools and resources.
            </p>
          </div>

          <div className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700">
            <h2 className="text-2xl font-bold text-black dark:text-white mb-4">
              What We Offer
            </h2>
            <ul className="space-y-3 text-zinc-700 dark:text-zinc-300">
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>Complete Quranic text in Arabic with proper Unicode encoding</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>Multiple translations in various languages from renowned scholars</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>Downloadable resources in multiple formats (JSON, XML, CSV, TXT)</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>RESTful API for easy integration into applications</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>Comprehensive metadata about Surahs and Ayahs</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>Free and open access to all resources</span>
              </li>
            </ul>
          </div>

          <div className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700">
            <h2 className="text-2xl font-bold text-black dark:text-white mb-4">
              Who Can Benefit
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h3 className="font-bold text-black dark:text-white mb-2">Developers</h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">
                  Integrate Quranic data into your apps, websites, and projects using our API
                </p>
              </div>
              <div>
                <h3 className="font-bold text-black dark:text-white mb-2">Researchers</h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">
                  Access structured Quranic data for academic research and analysis
                </p>
              </div>
              <div>
                <h3 className="font-bold text-black dark:text-white mb-2">Students</h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">
                  Study the Quran with easy access to translations and verses
                </p>
              </div>
              <div>
                <h3 className="font-bold text-black dark:text-white mb-2">Organizations</h3>
                <p className="text-zinc-600 dark:text-zinc-400 text-sm">
                  Use our resources for educational and community projects
                </p>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-950 dark:to-blue-950 border border-green-200 dark:border-green-800 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-black dark:text-white mb-4">
              Get Started
            </h2>
            <p className="text-zinc-700 dark:text-zinc-300 mb-6">
              Ready to explore? Download our resources or start using the API today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="/downloads"
                className="px-6 py-3 bg-black dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors text-center"
              >
                Browse Downloads
              </a>
              <a
                href="/api-docs"
                className="px-6 py-3 border border-black dark:border-white text-black dark:text-white rounded-lg font-medium hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-center"
              >
                API Documentation
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
