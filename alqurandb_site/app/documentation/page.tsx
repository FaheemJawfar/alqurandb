'use client';

import { useState } from 'react';
import Navbar from '../components/Navbar';
import { Copy, ExternalLink, Info, Download, Check, AlertCircle, FileText } from 'lucide-react';

export default function ApiDocs() {
  const [apiUrl, setApiUrl] = useState(
    process.env.NEXT_PUBLIC_API_URL || 'https://alqurandb.com/api'
  );

  const [copied, setCopied] = useState(false);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const endpoints = [
    {
      id: 'list-translations',
      method: 'GET',
      path: '/translations/',
      title: 'List All Translations',
      description: 'Get a list of all available Quran translations with metadata.',
      parameters: [],
      example: `${apiUrl}/translations/`,
      response: {
        total: 178,
        translations: [
          {
            id: "english_sahih",
            language: "English",
            translator: "Saheeh International",
            name_in_language: "Saheeh International",
            source: "tanzil"
          }
        ]
      }
    },
    {
      id: 'download-translation',
      method: 'GET',
      path: '/translations/download/{translation_id}/{filetype}',
      title: 'Download Translation',
      description: 'Download a complete translation in various file formats.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier (e.g., english_sahih)' },
        { name: 'filetype', type: 'string', required: true, description: 'File format: json, csv, sqlite, xml, xlsx, or sql' }
      ],
      example: `${apiUrl}/translations/download/english_sahih/json`,
      response: 'File download'
    },
    {
      id: 'get-verse',
      method: 'GET',
      path: '/translations/{translation_id}/{sura}/{aya}',
      title: 'Get Specific Verse',
      description: 'Retrieve a specific verse by translation ID, sura number, and aya number.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'sura', type: 'integer', required: true, description: 'Sura number (1-114)' },
        { name: 'aya', type: 'integer', required: true, description: 'Aya number' }
      ],
      example: `${apiUrl}/translations/english_sahih/1/1`,
      response: {
        translation_id: "english_sahih",
        sura: 1,
        aya: 1,
        text: "In the name of Allah, the Entirely Merciful, the Especially Merciful."
      }
    },
    {
      id: 'get-sura',
      method: 'GET',
      path: '/translations/{translation_id}/{sura}',
      title: 'Get All Verses from a Sura',
      description: 'Retrieve all verses from a specific sura in a translation.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'sura', type: 'integer', required: true, description: 'Sura number (1-114)' },
        { name: 'from_aya', type: 'integer', required: false, description: 'Starting aya number (optional)' },
        { name: 'to_aya', type: 'integer', required: false, description: 'Ending aya number (optional)' }
      ],
      example: `${apiUrl}/translations/english_sahih/1`,
      response: {
        translation_id: "english_sahih",
        sura: 1,
        total: 7,
        verses: [
          {
            sura: 1,
            aya: 1,
            text: "In the name of Allah, the Entirely Merciful, the Especially Merciful."
          }
        ]
      }
    },
    {
      id: 'get-verse-range',
      method: 'GET',
      path: '/translations/{translation_id}/{sura}?from_aya={from}&to_aya={to}',
      title: 'Get Verse Range',
      description: 'Retrieve a range of verses from a specific sura.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'sura', type: 'integer', required: true, description: 'Sura number (1-114)' },
        { name: 'from_aya', type: 'integer', required: true, description: 'Starting aya number' },
        { name: 'to_aya', type: 'integer', required: true, description: 'Ending aya number' }
      ],
      example: `${apiUrl}/translations/english_sahih/2?from_aya=1&to_aya=5`,
      response: {
        translation_id: "english_sahih",
        sura: 2,
        total: 5,
        verses: [
          {
            sura: 2,
            aya: 1,
            text: "Alif, Lam, Meem."
          }
        ]
      }
    },
    {
      id: 'get-quran-sura',
      method: 'GET',
      path: '/quran/{sura}',
      title: 'Get Quran Sura',
      description: 'Retrieve all verses of a specific sura in Arabic.',
      parameters: [
        { name: 'sura', type: 'integer', required: true, description: 'Sura number (1-114)' }
      ],
      example: `${apiUrl}/quran/1`,
      response: {
        sura: 1,
        total: 7,
        verses: [
          {
            sura: 1,
            aya: 1,
            text: "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ"
          }
        ]
      }
    },
    {
      id: 'get-quran-verse',
      method: 'GET',
      path: '/quran/{sura}/{aya}',
      title: 'Get Quran Verse',
      description: 'Retrieve a specific verse of the Quran in Arabic.',
      parameters: [
        { name: 'sura', type: 'integer', required: true, description: 'Sura number (1-114)' },
        { name: 'aya', type: 'integer', required: true, description: 'Aya number' }
      ],
      example: `${apiUrl}/quran/1/1`,
      response: {
        sura: 1,
        aya: 1,
        text: "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ"
      }
    }
  ];

  return (
    <div className="bg-slate-50 min-h-screen pb-20">
      <Navbar />

      <main className="pt-24 container mx-auto px-4 max-w-5xl">
        {/* Header */}
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-slate-900 mb-4 tracking-tight">API Documentation</h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            A simple, fast, and open RESTful API for accessing Quran translations and verses in multiple languages.
          </p>
        </div>

        {/* Getting Started */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
              <FileText size={24} strokeWidth={2} />
            </div>
            <h2 className="text-2xl font-bold text-slate-900">Getting Started</h2>
          </div>

          <p className="text-slate-600 mb-6 leading-relaxed">
            The AlQuranDB API provides programmatic access to Quran translations.
            All endpoints return JSON responses and support CORS for browser-based applications.
          </p>

          <div className="mb-8">
            <label className="block text-sm font-semibold text-slate-700 mb-2">Base URL</label>
            <div className="flex gap-2">
              <div className="flex-grow relative">
                <input
                  type="text"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 font-mono text-sm text-slate-700 focus:ring-2 focus:ring-blue-500 outline-none"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                />
              </div>
              <button
                onClick={() => handleCopy(apiUrl)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors flex items-center gap-2 cursor-pointer shadow-sm active:translate-y-0.5"
              >
                {copied ? <Check size={18} /> : <Copy size={18} />}
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              You can change this URL to point to your own deployment.
            </p>
          </div>

          <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-2 border-blue-200 rounded-xl p-6 shadow-md">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white flex-shrink-0">
                <Info size={22} strokeWidth={2.5} />
              </div>
              <div className="flex-grow">
                <h4 className="font-bold text-blue-900 text-lg mb-2">🚀 Interactive API Documentation</h4>
                <p className="text-sm text-blue-800 mb-4 leading-relaxed">
                  FastAPI provides auto-generated interactive API documentation where you can test endpoints directly in your browser:
                </p>
                <div className="flex flex-wrap gap-3">
                  <a
                    href="/docs"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold px-5 py-2.5 rounded-lg shadow-md hover:shadow-lg transition-all active:translate-y-0.5"
                  >
                    <ExternalLink size={18} />
                    Swagger UI
                  </a>
                  <a
                    href="/redoc"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold px-5 py-2.5 rounded-lg shadow-md hover:shadow-lg transition-all active:translate-y-0.5"
                  >
                    <ExternalLink size={18} />
                    ReDoc
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Endpoints */}
        <div className="space-y-8">
          <h2 className="text-2xl font-bold text-slate-900 border-b border-slate-200 pb-4">API Endpoints</h2>

          {endpoints.map((endpoint) => (
            <div key={endpoint.id} className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="border-b border-slate-100 bg-slate-50/50 p-6 flex items-start justify-between flex-wrap gap-4">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wide">
                      {endpoint.method}
                    </span>
                    <h3 className="text-lg font-bold text-slate-900">{endpoint.title}</h3>
                  </div>
                  <p className="text-slate-600 text-sm">{endpoint.description}</p>
                </div>
              </div>

              <div className="p-6">
                {/* Path */}
                <div className="mb-6">
                  <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Endpoint Path</label>
                  <div className="bg-slate-900 text-slate-100 rounded-lg p-3 font-mono text-sm border border-slate-800 flex items-center justify-between gap-3 group">
                    <div className="overflow-x-auto whitespace-nowrap scrollbar-hide">
                      <span className="text-slate-500 select-none">{apiUrl}</span>
                      <span className="text-blue-400 font-bold">{endpoint.path}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => window.open(endpoint.example, '_blank')}
                        className="text-slate-400 hover:text-white transition-colors cursor-pointer flex items-center gap-1.5 px-3 py-1.5 rounded-md hover:bg-slate-800"
                        title="Try this endpoint"
                      >
                        <ExternalLink size={16} />
                        <span className="text-xs font-semibold">Try it</span>
                      </button>
                      <button
                        onClick={() => handleCopy(`${apiUrl}${endpoint.path}`)}
                        className="text-slate-400 hover:text-white transition-colors cursor-pointer p-1.5 rounded-md hover:bg-slate-800"
                        title="Copy endpoint URL"
                      >
                        <Copy size={18} />
                      </button>
                    </div>
                  </div>
                </div>

                {/* Parameters */}
                {endpoint.parameters.length > 0 && (
                  <div className="mb-6">
                    <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Parameters</label>
                    <div className="overflow-x-auto rounded-lg border border-slate-200">
                      <table className="w-full text-sm text-left">
                        <thead className="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200">
                          <tr>
                            <th className="px-4 py-3 w-1/4">Name</th>
                            <th className="px-4 py-3 w-1/6">Type</th>
                            <th className="px-4 py-3 w-1/6">Required</th>
                            <th className="px-4 py-3">Description</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {endpoint.parameters.map((param, idx) => (
                            <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                              <td className="px-4 py-3 font-mono text-blue-600">{param.name}</td>
                              <td className="px-4 py-3"><span className="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-xs">{param.type}</span></td>
                              <td className="px-4 py-3">
                                {param.required ? (
                                  <span className="text-red-600 font-medium text-xs bg-red-50 px-2 py-0.5 rounded border border-red-100">Required</span>
                                ) : (
                                  <span className="text-slate-500 text-xs bg-slate-100 px-2 py-0.5 rounded">Optional</span>
                                )}
                              </td>
                              <td className="px-4 py-3 text-slate-600">{param.description}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Example Response */}
                <div>
                  <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Example Response</label>
                  {typeof endpoint.response === 'object' ? (
                    <div className="bg-slate-900 rounded-lg shadow-inner overflow-hidden border border-slate-800">
                      <div className="flex items-center justify-between px-4 py-2 bg-slate-800/50 border-b border-slate-700/50">
                        <span className="text-xs text-slate-400 font-mono">JSON</span>
                      </div>
                      <pre className="p-4 overflow-x-auto text-sm font-mono text-emerald-400">
                        <code>{JSON.stringify(endpoint.response, null, 2)}</code>
                      </pre>
                    </div>
                  ) : (
                    <div className="bg-blue-50 text-blue-800 p-4 rounded-lg flex items-center gap-3 border border-blue-100">
                      <Download size={18} />
                      <span className="font-medium">{endpoint.response}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {/* Error Codes */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="border-b border-slate-100 bg-slate-50/50 p-6">
              <div className="flex items-center gap-3">
                <AlertCircle className="text-red-500" size={24} />
                <h3 className="text-xl font-bold text-slate-900">Error Responses</h3>
              </div>
            </div>
            <div className="p-6">
              <p className="text-slate-600 mb-4 text-sm">The API uses standard HTTP status codes for error responses.</p>
              <div className="overflow-x-auto rounded-lg border border-slate-200">
                <table className="w-full text-sm text-left">
                  <thead className="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="px-4 py-3 w-24">Status</th>
                      <th className="px-4 py-3 w-1/3">Description</th>
                      <th className="px-4 py-3">Example</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {[
                      { code: 200, color: 'text-green-600 bg-green-50 border-green-100', desc: 'Success - Request completed successfully', example: 'Verse data returned' },
                      { code: 404, color: 'text-red-600 bg-red-50 border-red-100', desc: 'Not Found - Resource does not exist', example: JSON.stringify({ detail: "Verse not found" }) },
                      { code: 422, color: 'text-orange-600 bg-orange-50 border-orange-100', desc: 'Validation Error - Invalid parameters', example: JSON.stringify({ detail: "Sura must be 1-114" }) },
                      { code: 500, color: 'text-red-600 bg-red-50 border-red-100', desc: 'Internal Server Error', example: JSON.stringify({ detail: "Server error" }) }
                    ].map((err, i) => (
                      <tr key={i} className="hover:bg-slate-50/50">
                        <td className="px-4 py-3">
                          <span className={`font-mono font-bold text-xs px-2 py-1 rounded border ${err.color}`}>{err.code}</span>
                        </td>
                        <td className="px-4 py-3 text-slate-700 font-medium">{err.desc}</td>
                        <td className="px-4 py-3 font-mono text-slate-500 text-xs truncate max-w-xs">{err.example}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
