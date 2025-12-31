'use client';

import { useEffect, useState } from 'react';

interface Translation {
  id: string;
  language: string;
  translator: string;
  name_in_language: string;
  source: string;
}

interface TranslationsResponse {
  total: number;
  translations: Translation[];
}

interface Verse {
  translation_id: string;
  sura: number;
  aya: number;
  text: string;
}

interface VersesResponse {
  translation_id: string;
  sura: number | null;
  total: number;
  verses: Verse[];
}

export default function Home() {
  const [translations, setTranslations] = useState<Translation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [showVerses, setShowVerses] = useState(false);
  const [selectedTranslation, setSelectedTranslation] = useState<Translation | null>(null);
  const [selectedSura, setSelectedSura] = useState<number>(1);
  const [verses, setVerses] = useState<Verse[]>([]);
  const [versesLoading, setVersesLoading] = useState(false);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    fetchTranslations();
  }, []);

  async function fetchTranslations() {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/translations/`);

      if (!response.ok) {
        throw new Error('Failed to fetch translations');
      }

      const data: TranslationsResponse = await response.json();
      setTranslations(data.translations);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }

  function handleDownload(translationId: string, fileType: 'json' | 'csv' | 'sqlite' | 'xml' | 'xlsx') {
    const downloadUrl = `${API_BASE_URL}/translations/download/${translationId}/${fileType}`;
    window.open(downloadUrl, '_blank');
  }

  async function handleViewVerses(translation: Translation) {
    setSelectedTranslation(translation);
    setShowVerses(true);
    setSelectedSura(1);
    await fetchVerses(translation.id, 1);
  }

  async function fetchVerses(translationId: string, sura: number) {
    try {
      setVersesLoading(true);
      const response = await fetch(`${API_BASE_URL}/translations/${translationId}/${sura}`);

      if (!response.ok) {
        throw new Error('Failed to fetch verses');
      }

      const data: VersesResponse = await response.json();
      setVerses(data.verses);
    } catch (err) {
      console.error('Error fetching verses:', err);
      setVerses([]);
    } finally {
      setVersesLoading(false);
    }
  }

  async function handleSuraChange(sura: number) {
    setSelectedSura(sura);
    if (selectedTranslation) {
      await fetchVerses(selectedTranslation.id, sura);
    }
  }

  const filteredTranslations = translations.filter(
    (translation) =>
      translation.language.toLowerCase().includes(searchTerm.toLowerCase()) ||
      translation.translator.toLowerCase().includes(searchTerm.toLowerCase()) ||
      translation.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const uniqueLanguages = new Set(filteredTranslations.map(t => t.language));

  return (
    <div className="page-body">
      <div className="container-xl">
        {/* Header */}
        <div className="page-header d-print-none mb-3">
          <div className="row align-items-center">
            <div className="col">
              <h2 className="page-title">Quran Translations</h2>
              <div className="text-muted mt-1">
                Download {translations.length} translations in {uniqueLanguages.size} languages
              </div>
            </div>
          </div>
        </div>

        {/* API Info Card */}
        <div className="row mb-3">
          <div className="col-12">
            <div className="card bg-primary-lt">
              <div className="card-body">
                <div className="row align-items-center">
                  <div className="col">
                    <h3 className="card-title mb-1">
                      <i className="ti ti-code me-2"></i>
                      Developer API Available
                    </h3>
                    <p className="text-muted mb-0">
                      Access Quran translations programmatically with our RESTful API. Get verses by sura, aya, or download complete translations.
                    </p>
                  </div>
                  <div className="col-auto">
                    <a href="/documentation" className="btn btn-primary">
                      <i className="ti ti-book me-1"></i>
                      View API Docs
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Search */}
        <div className="row mb-3">
          <div className="col-md-6">
            <div className="input-icon">
              <span className="input-icon-addon">
                <i className="ti ti-search"></i>
              </span>
              <input
                type="text"
                className="form-control"
                placeholder="Search translations..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-6">
            <div className="text-muted text-end">
              {!loading && `Showing ${filteredTranslations.length} of ${translations.length} translations`}
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="alert alert-danger">
            <h4 className="alert-title">Error</h4>
            <div>{error}</div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="text-center py-5">
            <div className="spinner-border" role="status"></div>
            <div className="mt-2">Loading translations...</div>
          </div>
        )}

        {/* Table */}
        {!loading && !error && (
          <div className="card">
            <div className="table-responsive">
              <table className="table table-vcenter card-table table-striped">
                <thead>
                  <tr>
                    <th style={{ width: '150px' }}>Language</th>
                    <th style={{ width: '250px' }}>Translator</th>
                    <th style={{ width: '200px' }}>Native Name</th>
                    <th style={{ width: '400px' }}>Downloads</th>
                    <th style={{ width: '120px' }}>Actions</th>
                    <th style={{ width: '100px' }}>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTranslations.map((translation) => (
                    <tr key={translation.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          <span className="avatar avatar-sm me-2" style={{ backgroundColor: '#206bc4', color: 'white' }}>
                            {translation.language.charAt(0)}
                          </span>
                          <strong>{translation.language}</strong>
                        </div>
                      </td>
                      <td>
                        <div>{translation.translator}</div>
                        <div className="text-muted small">{translation.id}</div>
                      </td>
                      <td className="text-muted">{translation.name_in_language}</td>
                      <td>
                        <div className="btn-list">
                          <button
                            onClick={() => handleDownload(translation.id, 'json')}
                            className="btn btn-sm btn-primary"
                            title="Download as JSON"
                          >
                            <i className="ti ti-download me-1"></i>
                            JSON
                          </button>
                          <button
                            onClick={() => handleDownload(translation.id, 'csv')}
                            className="btn btn-sm btn-success"
                            title="Download as CSV"
                          >
                            <i className="ti ti-download me-1"></i>
                            CSV
                          </button>
                          <button
                            onClick={() => handleDownload(translation.id, 'sqlite')}
                            className="btn btn-sm btn-secondary"
                            title="Download as SQLite database"
                          >
                            <i className="ti ti-database me-1"></i>
                            SQLite
                          </button>
                          <button
                            onClick={() => handleDownload(translation.id, 'xml')}
                            className="btn btn-sm btn-info"
                            title="Download as XML"
                          >
                            <i className="ti ti-file-code me-1"></i>
                            XML
                          </button>
                          <button
                            onClick={() => handleDownload(translation.id, 'xlsx')}
                            className="btn btn-sm btn-warning"
                            title="Download as Excel"
                          >
                            <i className="ti ti-file-spreadsheet me-1"></i>
                            Excel
                          </button>
                        </div>
                      </td>
                      <td>
                        <button
                          onClick={() => handleViewVerses(translation)}
                          className="btn btn-sm btn-ghost-primary"
                          title="View verses"
                        >
                          <i className="ti ti-book-2 me-1"></i>
                          View
                        </button>
                      </td>
                      <td>
                        <span className="text-muted small">{translation.source}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Empty */}
        {!loading && !error && filteredTranslations.length === 0 && (
          <div className="empty">
            <div className="empty-icon">
              <i className="ti ti-file-search"></i>
            </div>
            <p className="empty-title">No translations found</p>
            <p className="empty-subtitle text-muted">
              Try a different search term
            </p>
          </div>
        )}

        {/* Verses Modal */}
        {showVerses && selectedTranslation && (
          <div className="modal modal-blur fade show" style={{ display: 'block' }}>
            <div className="modal-dialog modal-lg modal-dialog-scrollable">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">{selectedTranslation.language} - {selectedTranslation.translator}</h5>
                  <button type="button" className="btn-close" onClick={() => setShowVerses(false)}></button>
                </div>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Select Sura</label>
                    <select
                      className="form-select"
                      value={selectedSura}
                      onChange={(e) => handleSuraChange(Number(e.target.value))}
                    >
                      {Array.from({ length: 114 }, (_, i) => i + 1).map((sura) => (
                        <option key={sura} value={sura}>
                          Sura {sura}
                        </option>
                      ))}
                    </select>
                  </div>

                  {versesLoading ? (
                    <div className="text-center py-5">
                      <div className="spinner-border" role="status"></div>
                      <div className="mt-2">Loading verses...</div>
                    </div>
                  ) : (
                    <div className="list-group list-group-flush">
                      {verses.map((verse) => (
                        <div key={`${verse.sura}:${verse.aya}`} className="list-group-item">
                          <div className="row align-items-start">
                            <div className="col-auto">
                              <span className="badge bg-primary">{verse.aya}</span>
                            </div>
                            <div className="col">
                              <p className="mb-0">{verse.text}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowVerses(false)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        {showVerses && <div className="modal-backdrop fade show"></div>}
      </div>
    </div>
  );
}
