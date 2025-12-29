'use client';

import { useState } from 'react';

export default function ApiDocs() {
  const [apiUrl, setApiUrl] = useState('http://localhost:8000/api/v1');
  const [selectedEndpoint, setSelectedEndpoint] = useState<string | null>(null);

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
        total: 114,
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
        { name: 'filetype', type: 'string', required: true, description: 'File format: json, csv, sqlite, xml, or xlsx' }
      ],
      example: `${apiUrl}/translations/download/english_sahih/json`,
      response: 'File download'
    },
    {
      id: 'get-verse',
      method: 'GET',
      path: '/translations/{translation_id}/{surah}/{ayah}',
      title: 'Get Specific Verse',
      description: 'Retrieve a specific verse by translation ID, surah number, and ayah number.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'surah', type: 'integer', required: true, description: 'Surah number (1-114)' },
        { name: 'ayah', type: 'integer', required: true, description: 'Ayah number' }
      ],
      example: `${apiUrl}/translations/english_sahih/1/1`,
      response: {
        translation_id: "english_sahih",
        surah: 1,
        ayah: 1,
        text: "In the name of Allah, the Entirely Merciful, the Especially Merciful."
      }
    },
    {
      id: 'get-surah',
      method: 'GET',
      path: '/translations/{translation_id}/{surah}',
      title: 'Get All Verses from a Surah',
      description: 'Retrieve all verses from a specific surah in a translation.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'surah', type: 'integer', required: true, description: 'Surah number (1-114)' },
        { name: 'from_ayah', type: 'integer', required: false, description: 'Starting ayah number (optional)' },
        { name: 'to_ayah', type: 'integer', required: false, description: 'Ending ayah number (optional)' }
      ],
      example: `${apiUrl}/translations/english_sahih/1`,
      response: {
        translation_id: "english_sahih",
        surah: 1,
        total: 7,
        verses: [
          {
            translation_id: "english_sahih",
            surah: 1,
            ayah: 1,
            text: "In the name of Allah, the Entirely Merciful, the Especially Merciful."
          }
        ]
      }
    },
    {
      id: 'get-verse-range',
      method: 'GET',
      path: '/translations/{translation_id}/{surah}?from_ayah={from}&to_ayah={to}',
      title: 'Get Verse Range',
      description: 'Retrieve a range of verses from a specific surah.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' },
        { name: 'surah', type: 'integer', required: true, description: 'Surah number (1-114)' },
        { name: 'from_ayah', type: 'integer', required: true, description: 'Starting ayah number' },
        { name: 'to_ayah', type: 'integer', required: true, description: 'Ending ayah number' }
      ],
      example: `${apiUrl}/translations/english_sahih/2?from_ayah=1&to_ayah=5`,
      response: {
        translation_id: "english_sahih",
        surah: 2,
        total: 5,
        verses: [
          {
            translation_id: "english_sahih",
            surah: 2,
            ayah: 1,
            text: "Alif, Lam, Meem."
          }
        ]
      }
    },
    {
      id: 'get-all-verses',
      method: 'GET',
      path: '/translations/{translation_id}',
      title: 'Get All Verses from Translation',
      description: 'Retrieve all 6236 verses from a complete translation.',
      parameters: [
        { name: 'translation_id', type: 'string', required: true, description: 'Translation identifier' }
      ],
      example: `${apiUrl}/translations/english_sahih`,
      response: {
        translation_id: "english_sahih",
        surah: null,
        total: 6236,
        verses: [
          {
            translation_id: "english_sahih",
            surah: 1,
            ayah: 1,
            text: "In the name of Allah, the Entirely Merciful, the Especially Merciful."
          }
        ]
      }
    }
  ];

  return (
    <div className="page-body">
      <div className="container-xl">
        {/* Header */}
        <div className="page-header d-print-none mb-4">
          <div className="row align-items-center">
            <div className="col">
              <h2 className="page-title">API Documentation</h2>
              <div className="text-muted mt-1">
                RESTful API for accessing Quran translations and verses
              </div>
            </div>
          </div>
        </div>

        {/* Introduction */}
        <div className="row mb-3">
          <div className="col-12">
            <div className="card">
              <div className="card-body">
                <h3 className="card-title">Getting Started</h3>
                <p className="text-muted">
                  The AlQuranDB API provides programmatic access to Quran translations and verses.
                  All endpoints return JSON responses and support CORS for browser-based applications.
                </p>

                <div className="mb-3">
                  <label className="form-label">Base URL</label>
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control font-monospace"
                      value={apiUrl}
                      onChange={(e) => setApiUrl(e.target.value)}
                    />
                    <button className="btn btn-primary" onClick={() => {
                      navigator.clipboard.writeText(apiUrl);
                    }}>
                      <i className="ti ti-copy"></i> Copy
                    </button>
                  </div>
                  <small className="form-hint">
                    Change this to your API server URL
                  </small>
                </div>

                <div className="alert alert-info mb-0">
                  <h4 className="alert-title">
                    <i className="ti ti-info-circle"></i> Interactive Documentation
                  </h4>
                  <div>
                    FastAPI provides interactive API documentation at:
                    <ul className="mb-0 mt-2">
                      <li><a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-decoration-underline">Swagger UI: /docs</a></li>
                      <li><a href="http://localhost:8000/redoc" target="_blank" rel="noreferrer" className="text-decoration-underline">ReDoc: /redoc</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Endpoints */}
        <div className="row">
          <div className="col-12">
            <h3 className="mb-3">API Endpoints</h3>

            {endpoints.map((endpoint) => (
              <div key={endpoint.id} className="card mb-3">
                <div className="card-header">
                  <h3 className="card-title">
                    <span className="badge bg-primary me-2">{endpoint.method}</span>
                    {endpoint.title}
                  </h3>
                </div>
                <div className="card-body">
                  <p className="text-muted">{endpoint.description}</p>

                  {/* Path */}
                  <div className="mb-3">
                    <label className="form-label">Endpoint Path</label>
                    <div className="input-group">
                      <span className="input-group-text font-monospace">{apiUrl}</span>
                      <input
                        type="text"
                        className="form-control font-monospace bg-light"
                        value={endpoint.path}
                        readOnly
                      />
                    </div>
                  </div>

                  {/* Parameters */}
                  {endpoint.parameters.length > 0 && (
                    <div className="mb-3">
                      <label className="form-label">Parameters</label>
                      <div className="table-responsive">
                        <table className="table table-sm table-bordered">
                          <thead>
                            <tr>
                              <th>Name</th>
                              <th>Type</th>
                              <th>Required</th>
                              <th>Description</th>
                            </tr>
                          </thead>
                          <tbody>
                            {endpoint.parameters.map((param, idx) => (
                              <tr key={idx}>
                                <td className="font-monospace">{param.name}</td>
                                <td><span className="badge bg-secondary">{param.type}</span></td>
                                <td>
                                  {param.required ? (
                                    <span className="badge bg-danger">Required</span>
                                  ) : (
                                    <span className="badge bg-secondary">Optional</span>
                                  )}
                                </td>
                                <td className="text-muted">{param.description}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Example */}
                  <div className="mb-3">
                    <label className="form-label">Example Request</label>
                    <div className="input-group">
                      <input
                        type="text"
                        className="form-control font-monospace bg-light"
                        value={endpoint.example}
                        readOnly
                      />
                      <button
                        className="btn btn-primary"
                        onClick={() => {
                          navigator.clipboard.writeText(endpoint.example);
                        }}
                      >
                        <i className="ti ti-copy"></i> Copy
                      </button>
                      <button
                        className="btn btn-success"
                        onClick={() => window.open(endpoint.example, '_blank')}
                      >
                        <i className="ti ti-external-link"></i> Try
                      </button>
                    </div>
                  </div>

                  {/* Response */}
                  {typeof endpoint.response === 'object' && (
                    <div>
                      <label className="form-label">Example Response</label>
                      <div className="card card-sm bg-dark text-white">
                        <div className="card-body">
                          <pre className="mb-0" style={{ fontSize: '0.875rem' }}>
                            <code>{JSON.stringify(endpoint.response, null, 2)}</code>
                          </pre>
                        </div>
                      </div>
                    </div>
                  )}
                  {typeof endpoint.response === 'string' && (
                    <div>
                      <label className="form-label">Response</label>
                      <div className="alert alert-info mb-0">
                        <i className="ti ti-download"></i> {endpoint.response}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Error Responses */}
        <div className="row mb-3">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Error Responses</h3>
              </div>
              <div className="card-body">
                <p className="text-muted">The API uses standard HTTP status codes for error responses:</p>

                <div className="table-responsive">
                  <table className="table table-bordered">
                    <thead>
                      <tr>
                        <th>Status Code</th>
                        <th>Description</th>
                        <th>Example</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td><span className="badge bg-success">200</span></td>
                        <td>Success - Request completed successfully</td>
                        <td className="font-monospace text-muted">Verse data returned</td>
                      </tr>
                      <tr>
                        <td><span className="badge bg-danger">404</span></td>
                        <td>Not Found - Translation, surah, or verse not found</td>
                        <td className="font-monospace text-muted">
                          {JSON.stringify({ detail: "Verse 1:8 not found in translation 'english_sahih'" })}
                        </td>
                      </tr>
                      <tr>
                        <td><span className="badge bg-danger">422</span></td>
                        <td>Validation Error - Invalid parameters</td>
                        <td className="font-monospace text-muted">
                          {JSON.stringify({ detail: "Surah number must be between 1 and 114" })}
                        </td>
                      </tr>
                      <tr>
                        <td><span className="badge bg-danger">500</span></td>
                        <td>Internal Server Error</td>
                        <td className="font-monospace text-muted">
                          {JSON.stringify({ detail: "Internal server error" })}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Code Examples */}
        <div className="row mb-3">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Code Examples</h3>
              </div>
              <div className="card-body">
                <ul className="nav nav-tabs mb-3" role="tablist">
                  <li className="nav-item">
                    <a className="nav-link active" data-bs-toggle="tab" href="#javascript">JavaScript</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" data-bs-toggle="tab" href="#python">Python</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link" data-bs-toggle="tab" href="#curl">cURL</a>
                  </li>
                </ul>

                <div className="tab-content">
                  <div className="tab-pane active" id="javascript">
                    <div className="card card-sm bg-dark text-white">
                      <div className="card-body">
                        <pre className="mb-0" style={{ fontSize: '0.875rem' }}>
                          <code>{`// Fetch all translations
const response = await fetch('${apiUrl}/translations/');
const data = await response.json();
console.log(data.translations);

// Get a specific verse
const verse = await fetch('${apiUrl}/translations/english_sahih/1/1');
const verseData = await verse.json();
console.log(verseData.text);

// Get all verses from a surah
const surah = await fetch('${apiUrl}/translations/english_sahih/1');
const surahData = await surah.json();
console.log(\`Total verses: \${surahData.total}\`);`}</code>
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div className="tab-pane" id="python">
                    <div className="card card-sm bg-dark text-white">
                      <div className="card-body">
                        <pre className="mb-0" style={{ fontSize: '0.875rem' }}>
                          <code>{`import requests

# Fetch all translations
response = requests.get('${apiUrl}/translations/')
data = response.json()
print(data['translations'])

# Get a specific verse
verse = requests.get('${apiUrl}/translations/english_sahih/1/1')
verse_data = verse.json()
print(verse_data['text'])

# Get all verses from a surah
surah = requests.get('${apiUrl}/translations/english_sahih/1')
surah_data = surah.json()
print(f"Total verses: {surah_data['total']}")`}</code>
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div className="tab-pane" id="curl">
                    <div className="card card-sm bg-dark text-white">
                      <div className="card-body">
                        <pre className="mb-0" style={{ fontSize: '0.875rem' }}>
                          <code>{`# Fetch all translations
curl ${apiUrl}/translations/

# Get a specific verse
curl ${apiUrl}/translations/english_sahih/1/1

# Get all verses from a surah
curl ${apiUrl}/translations/english_sahih/1

# Get verse range
curl "${apiUrl}/translations/english_sahih/2?from_ayah=1&to_ayah=5"

# Download translation as JSON
curl -O ${apiUrl}/translations/download/english_sahih/json`}</code>
                        </pre>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
