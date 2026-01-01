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
  footnotes?: string;
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
  const [bismillah, setBismillah] = useState('');

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

  function handleDownload(translationId: string, fileType: 'json' | 'csv' | 'sqlite' | 'xml' | 'xlsx' | 'sql') {
    const downloadUrl = `${API_BASE_URL}/translations/download/${translationId}/${fileType}`;
    window.open(downloadUrl, '_blank');
  }

  async function handleViewVerses(translation: Translation) {
    setSelectedTranslation(translation);
    setShowVerses(true);
    setSelectedSura(1);
    fetchBismillah(translation.id);
    await fetchVerses(translation.id, 1);
  }

  async function fetchBismillah(translationId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/translations/${translationId}/1`);
      if (response.ok) {
        const data: VersesResponse = await response.json();
        if (data.verses.length > 0) {
          setBismillah(data.verses[0].text);
        }
      }
    } catch (err) {
      console.error('Error fetching Bismillah:', err);
    }
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
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 sm:py-12">
          <div
            className="absolute inset-0 bg-slate-900/60 backdrop-blur-md transition-opacity duration-300"
            onClick={() => setShowVerses(false)}
          ></div>

          <div className="relative w-full max-w-5xl h-full max-h-[90vh] bg-white border border-slate-200 rounded-3xl shadow-[0_32px_64px_-16px_rgba(0,0,0,0.2)] flex flex-col overflow-hidden animate-[modal_0.3s_cubic-bezier(0.16,1,0.3,1)]">
            {/* Modal Header - Glassmorphism */}
            <div className="flex items-center justify-between p-6 px-8 border-b border-slate-100 bg-white/80 backdrop-blur-md sticky top-0 z-20">
              <div className="flex items-center gap-5 min-w-0">
                <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center shadow-lg shadow-blue-500/20 text-xl font-black">
                  {selectedTranslation.language.charAt(0).toUpperCase()}
                </div>
                <div className="min-w-0">
                  <h5 className="text-lg sm:text-xl font-black text-slate-900 truncate">
                    {selectedTranslation.language}
                  </h5>
                  <div className="flex items-center gap-2 mt-0.5">
                    <p className="text-xs font-bold text-slate-500 truncate">{selectedTranslation.translator}</p>
                    <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                    <p className="text-[9px] uppercase tracking-widest font-black text-blue-500">{selectedTranslation.source}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                {/* Previous Sura Button */}
                <button
                  onClick={() => selectedSura > 1 && handleSuraChange(selectedSura - 1)}
                  disabled={selectedSura <= 1}
                  className="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-50 border border-slate-200 text-slate-500 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-600 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-slate-50 disabled:hover:border-slate-200 disabled:hover:text-slate-500 transition-all"
                  title="Previous Sura"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6" /></svg>
                </button>

                <div className="relative group/select">
                  <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none text-blue-500 group-hover/select:translate-y-0.5 transition-transform">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></svg>
                  </div>
                  <select
                    className="appearance-none bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-900 rounded-xl py-2 pl-4 pr-10 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 cursor-pointer text-[13px] font-black transition-all outline-none"
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

                {/* Next Sura Button */}
                <button
                  onClick={() => selectedSura < 114 && handleSuraChange(selectedSura + 1)}
                  disabled={selectedSura >= 114}
                  className="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-50 border border-slate-200 text-slate-500 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-600 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-slate-50 disabled:hover:border-slate-200 disabled:hover:text-slate-500 transition-all"
                  title="Next Sura"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6" /></svg>
                </button>
              </div>

              <button
                type="button"
                className="w-9 h-9 rounded-xl bg-slate-50 text-slate-400 hover:text-red-500 hover:bg-red-50 hover:border-red-100 border border-transparent flex items-center justify-center transition-all duration-200"
                onClick={() => setShowVerses(false)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="overflow-y-auto p-0 bg-slate-50/50 flex-grow scroll-smooth">
              {versesLoading ? (
                <div className="flex flex-col items-center justify-center py-40">
                  <div className="relative">
                    <div className="w-12 h-12 border-4 border-blue-500/10 rounded-full"></div>
                    <div className="absolute top-0 w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                  <div className="mt-6 text-slate-400 font-bold uppercase tracking-widest text-[10px]">Fetching Sacred Data</div>
                </div>
              ) : (
                <div className="p-4 sm:p-5 space-y-4">
                  {/* Bismillah Section if Sura is not 1 or 9 */}
                  {selectedSura !== 1 && selectedSura !== 9 && (
                    <div className="text-center py-3 mb-4 font-serif italic text-slate-600 text-base">
                      {bismillah || "In the Name of Allah, the Most Gracious, the Most Merciful"}
                    </div>
                  )}

                  {verses.map((verse) => {
                    // Simple parsing for footnotes to display them nicely
                    const parseFootnotes = (text?: string) => {
                      if (!text) return [];
                      const pattern = /\[(\d+)\]\s*(.*?)(?=\s*\[\d+\]|$)/gs;
                      const matches = Array.from(text.matchAll(pattern));
                      return matches.map(m => ({ id: m[1], text: m[2].trim() }));
                    };

                    const footnotesList = parseFootnotes(verse.footnotes);

                    return (
                      <div key={`${verse.sura}:${verse.aya}`} className="group relative bg-white rounded-2xl p-3 sm:p-4 border border-slate-200/60 shadow-sm hover:shadow-xl hover:shadow-blue-500/5 hover:border-blue-200 transition-all duration-300">
                        <div className="flex flex-col sm:flex-row gap-3">
                          {/* Aya Number Bubble */}
                          <div className="flex-shrink-0 pt-1">
                            <div className="w-10 h-10 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center group-hover:bg-blue-50 group-hover:border-blue-200 transition-all duration-300 shadow-sm">
                              <span className="text-sm font-black text-slate-400 group-hover:text-blue-600 transition-colors leading-none">{verse.aya}</span>
                            </div>
                          </div>

                          {/* Verse Text Area */}
                          <div className="flex-grow">
                            <p className="text-base sm:text-lg text-slate-800 leading-relaxed font-medium tracking-tight">
                              {verse.text.split(/(\[\d+\])/).map((part, i) => {
                                if (part.match(/\[\d+\]/)) {
                                  return (
                                    <span key={i} className="inline-flex items-center justify-center px-1 py-0.5 mx-0.5 bg-blue-50 text-blue-600 rounded text-[10px] font-black align-top mt-1 hover:bg-blue-500 hover:text-white transition-colors cursor-help border border-blue-100">
                                      {part.replace('[', '').replace(']', '')}
                                    </span>
                                  );
                                }
                                return part;
                              })}
                            </p>

                            {/* Footnotes Display */}
                            {footnotesList.length > 0 && (
                              <div className="mt-3 pt-3 border-t border-slate-100 space-y-2">
                                <div className="flex items-center gap-2 text-[9px] font-black uppercase tracking-widest text-slate-400 mb-1">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M12 8h.01" /><path d="M11 12h1v4h1" /><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z" /></svg>
                                  Footnotes
                                </div>
                                {footnotesList.map((note) => (
                                  <div key={note.id} className="flex gap-2.5 items-start bg-slate-50/50 p-2 rounded-lg border border-slate-100 hover:bg-blue-50/30 hover:border-blue-100 transition-colors">
                                    <span className="flex-shrink-0 w-4 h-4 rounded-md bg-blue-100 text-blue-700 text-[9px] font-black flex items-center justify-center border border-blue-200 mt-0.5">
                                      {note.id}
                                    </span>
                                    <p className="text-sm text-slate-600 leading-relaxed font-normal italic">
                                      {note.text}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>

                          {/* Actions column */}
                          <div className="sm:flex-shrink-0 sm:w-8 flex sm:flex-col items-center justify-start gap-1 border-t sm:border-t-0 sm:border-l border-slate-100 pt-3 sm:pt-0 sm:pl-3">
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(`${verse.text} (Al-Quran ${verse.sura}:${verse.aya})`);
                                // Could add a toast here
                              }}
                              className="w-8 h-8 rounded-xl hover:bg-blue-50 text-slate-400 hover:text-blue-600 flex items-center justify-center transition-all cursor-pointer"
                              title="Copy Verse"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M8 4v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7.242a2 2 0 0 0-.602-1.43L16.083 2.57A2 2 0 0 0 14.653 2H10a2 2 0 0 0-2 2Z" /><path d="M16 18v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2" /></svg>
                            </button>
                            <button
                              className="w-8 h-8 rounded-xl hover:bg-slate-100 text-slate-300 flex items-center justify-center transition-all cursor-not-allowed"
                              title="Play Audio (Coming Soon)"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M7 4v16l13-8z" /></svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Modal Footer - Stats */}
            {!versesLoading && verses.length > 0 && (
              <div className="p-4 px-8 border-t border-slate-100 bg-white flex justify-between items-center">
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  Showing {verses.length} verses from Sura {selectedSura}
                </p>
                <div className="flex gap-2">
                  <div className="px-3 py-1 bg-slate-50 rounded-full border border-slate-200 text-[10px] font-bold text-slate-500">
                    Sura: {selectedSura}
                  </div>
                  <div className="px-3 py-1 bg-slate-50 rounded-full border border-slate-200 text-[10px] font-bold text-slate-500">
                    Total: {verses.length}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
