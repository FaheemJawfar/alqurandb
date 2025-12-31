'use client';

import { useEffect, useState, useRef } from 'react';
import Navbar from './components/Navbar';
import SearchHero from './components/SearchHero';
import TranslationCard from './components/TranslationCard';

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

  // Ref for keyboard shortcut
  const searchInputRef = useRef<HTMLInputElement>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    fetchTranslations();

    // Keyboard shortcut for search
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement !== searchInputRef.current) {
        e.preventDefault();
        // We need to focus the input which is inside the SearchHero component
        // Since we don't have direct ref access easily without forwarding refs, 
        // we'll use a selector query as a simple workaround for this global shortcut
        const input = document.querySelector('input[type="text"]') as HTMLInputElement;
        if (input) input.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
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

  return (
    <div className="bg-slate-50 min-h-screen pb-20">
      <Navbar />

      <main className="pt-16">
        <SearchHero
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          count={filteredTranslations.length}
        />

        <div className="container mx-auto px-4 mt-8">
          {/* Error */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-500 mb-8 max-w-2xl mx-auto text-center">
              <h4 className="font-bold mb-1">Error Loading Data</h4>
              <div>{error}</div>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div className="text-center py-20">
              <div className="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              <div className="mt-4 text-slate-400">Loading translations...</div>
            </div>
          )}

          {/* Grid */}
          {!loading && !error && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTranslations.map((translation) => (
                <TranslationCard
                  key={translation.id}
                  translation={translation}
                  onDownload={handleDownload}
                  onViewVerses={handleViewVerses}
                />
              ))}
            </div>
          )}

          {/* Empty */}
          {!loading && !error && filteredTranslations.length === 0 && (
            <div className="text-center py-20">
              <div className="bg-white border border-slate-200 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-slate-400"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" /><path d="M21 21l-6 -6" /></svg>
              </div>
              <p className="text-xl font-bold text-slate-800">No translations found</p>
              <p className="text-slate-500 mt-2">
                Try searching for a different language or translator
              </p>
            </div>
          )}
        </div>
      </main>

      {/* Verses Modal / Slide-over */}
      {showVerses && selectedTranslation && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
          <div
            className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
            onClick={() => setShowVerses(false)}
          ></div>

          <div className="relative w-full max-w-4xl max-h-[90vh] bg-white border border-slate-200 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-[fade-in_0.2s_ease-out]">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-slate-100 bg-white sticky top-0 z-10">
              <div>
                <h5 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                  <span className="w-8 h-8 rounded bg-blue-50 text-blue-600 flex items-center justify-center text-sm border border-blue-100">
                    {selectedTranslation.language.charAt(0)}
                  </span>
                  {selectedTranslation.language}
                </h5>
                <p className="text-sm text-slate-500 mt-1 pl-10">{selectedTranslation.translator}</p>
              </div>

              <div className="flex items-center gap-4">
                <select
                  className="bg-slate-50 border border-slate-200 text-slate-700 rounded-lg py-2 pl-3 pr-8 focus:ring-2 focus:ring-blue-500 cursor-pointer text-sm font-medium"
                  value={selectedSura}
                  onChange={(e) => handleSuraChange(Number(e.target.value))}
                >
                  {Array.from({ length: 114 }, (_, i) => i + 1).map((sura) => (
                    <option key={sura} value={sura}>
                      Sura {sura}
                    </option>
                  ))}
                </select>

                <button
                  type="button"
                  className="w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:text-red-500 hover:bg-red-50 flex items-center justify-center transition-colors"
                  onClick={() => setShowVerses(false)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg>
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="overflow-y-auto p-6 bg-slate-50">
              {versesLoading ? (
                <div className="text-center py-20">
                  <div className="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  <div className="mt-4 text-slate-500">Loading sacred texts...</div>
                </div>
              ) : (
                <div className="space-y-4">
                  {verses.map((verse) => (
                    <div key={`${verse.sura}:${verse.aya}`} className="group p-4 bg-white rounded-xl shadow-sm hover:shadow-md border border-slate-200/50 transition-all">
                      <div className="flex gap-4">
                        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center text-sm font-bold text-slate-500 group-hover:text-blue-600 group-hover:border-blue-200 transition-all">
                          {verse.aya}
                        </div>
                        <div className="flex-grow pt-2">
                          <p className="text-lg text-slate-700 leading-relaxed font-serif">
                            {verse.text}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
