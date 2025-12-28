export default function ApiDocsPage() {
  const endpoints = [
    {
      method: "GET",
      path: "/quran/",
      description: "Get general information about the Quran",
      response: `{
  "total_surahs": 114,
  "total_ayahs": 6236,
  "message": "AlQuran Database"
}`
    },
    {
      method: "GET",
      path: "/surah/",
      description: "Get list of all Surahs",
      response: `{
  "message": "List of all surahs"
}`
    },
    {
      method: "GET",
      path: "/surah/{surah_number}",
      description: "Get details of a specific Surah",
      params: ["surah_number: integer (1-114)"],
      response: `{
  "surah_number": 1,
  "message": "Surah details"
}`
    },
    {
      method: "GET",
      path: "/ayah/{surah_number}/{ayah_number}",
      description: "Get a specific Ayah",
      params: [
        "surah_number: integer (1-114)",
        "ayah_number: integer"
      ],
      query: ["translation: string (optional) - e.g., 'sahih', 'yusufali', 'pickthall'"],
      response: `{
  "surah_number": 1,
  "ayah_number": 1,
  "message": "Ayah details"
}`
    },
    {
      method: "GET",
      path: "/translations/",
      description: "Get list of available translations",
      response: `{
  "translations": [...]
}`
    }
  ];

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 py-16 px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-black dark:text-white mb-4">
            API Documentation
          </h1>
          <p className="text-xl text-zinc-600 dark:text-zinc-400 max-w-3xl mb-6">
            Integrate Quranic data and translations into your applications using our REST API.
          </p>

          <div className="bg-white dark:bg-zinc-800 rounded-lg p-6 border border-zinc-200 dark:border-zinc-700">
            <h3 className="text-lg font-bold text-black dark:text-white mb-2">
              Base URL
            </h3>
            <div className="bg-zinc-900 dark:bg-zinc-950 rounded-lg p-4">
              <code className="text-green-400">
                http://localhost:8000/api/v1
              </code>
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <h2 className="text-3xl font-bold text-black dark:text-white">
            Endpoints
          </h2>

          {endpoints.map((endpoint, index) => (
            <div
              key={index}
              className="bg-white dark:bg-zinc-800 rounded-lg p-8 border border-zinc-200 dark:border-zinc-700"
            >
              <div className="flex items-start gap-4 mb-4">
                <span className={`px-3 py-1 rounded font-mono text-sm font-bold ${
                  endpoint.method === 'GET'
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
                    : 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                }`}>
                  {endpoint.method}
                </span>
                <code className="text-lg font-mono text-black dark:text-white">
                  {endpoint.path}
                </code>
              </div>

              <p className="text-zinc-600 dark:text-zinc-400 mb-4">
                {endpoint.description}
              </p>

              {endpoint.params && (
                <div className="mb-4">
                  <h4 className="font-bold text-black dark:text-white mb-2">
                    Path Parameters:
                  </h4>
                  <ul className="list-disc list-inside space-y-1 text-zinc-600 dark:text-zinc-400">
                    {endpoint.params.map((param, pIndex) => (
                      <li key={pIndex}>
                        <code className="text-sm bg-zinc-100 dark:bg-zinc-700 px-2 py-1 rounded">
                          {param}
                        </code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {endpoint.query && (
                <div className="mb-4">
                  <h4 className="font-bold text-black dark:text-white mb-2">
                    Query Parameters:
                  </h4>
                  <ul className="list-disc list-inside space-y-1 text-zinc-600 dark:text-zinc-400">
                    {endpoint.query.map((param, qIndex) => (
                      <li key={qIndex}>
                        <code className="text-sm bg-zinc-100 dark:bg-zinc-700 px-2 py-1 rounded">
                          {param}
                        </code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div>
                <h4 className="font-bold text-black dark:text-white mb-2">
                  Response:
                </h4>
                <div className="bg-zinc-900 dark:bg-zinc-950 rounded-lg p-4 overflow-x-auto">
                  <pre className="text-green-400 text-sm">
                    {endpoint.response}
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded-lg p-8">
          <h3 className="text-xl font-bold text-black dark:text-white mb-2">
            Interactive Documentation
          </h3>
          <p className="text-zinc-700 dark:text-zinc-300 mb-4">
            Explore and test the API using our interactive Swagger UI documentation.
          </p>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-6 py-3 bg-black dark:bg-white text-white dark:text-black rounded-lg font-medium hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors"
          >
            Open Swagger UI
          </a>
        </div>
      </div>
    </div>
  );
}
