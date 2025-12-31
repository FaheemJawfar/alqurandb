import { JSX } from 'react';
import DownloadButton from './DownloadButton';

interface Translation {
    id: string;
    language: string;
    translator: string;
    name_in_language: string;
    source: string;
}

interface TranslationCardProps {
    translation: Translation;
    onDownload: (id: string, type: 'json' | 'csv' | 'sqlite' | 'xml' | 'xlsx' | 'sql') => void;
    onViewVerses: (translation: Translation) => void;
}

export default function TranslationCard({ translation, onDownload, onViewVerses }: TranslationCardProps): JSX.Element {
    return (
        <div
            className="group relative bg-white border border-slate-200 hover:border-blue-400 rounded-xl p-5 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/5 flex flex-col h-full"
        >
            <div className="flex gap-4 mb-6">
                {/* Left Column: Icon */}
                <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-lg font-bold text-blue-600 group-hover:scale-110 transition-transform shadow-sm border border-blue-100">
                        {translation.language.charAt(0).toUpperCase()}
                    </div>
                </div>

                {/* Right Column: Content */}
                <div className="flex flex-col flex-grow min-w-0">
                    <div className="flex justify-between items-start mb-4">
                        <div className="min-w-0">
                            <h3 className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors truncate">
                                {translation.language}
                            </h3>
                            <p className="text-xs text-slate-500 font-medium truncate">{translation.name_in_language}</p>
                        </div>
                        <button
                            onClick={() => onViewVerses(translation)}
                            className="flex-shrink-0 px-4 py-2 rounded-lg text-xs font-bold text-blue-700 bg-blue-50 border border-blue-200 hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-all cursor-pointer flex items-center gap-2 shadow-sm ml-2"
                        >
                            View <span className="hidden sm:inline">Verses</span> <span className="group-hover:translate-x-0.5 transition-transform">→</span>
                        </button>
                    </div>

                    <div>
                        <p className="text-sm text-slate-700 font-semibold line-clamp-2" title={translation.translator}>
                            {translation.translator}
                        </p>
                        <p className="text-xs text-slate-500 mt-1 truncate">
                            Source: {translation.source}
                        </p>
                    </div>
                </div>
            </div>

            <div className="mt-auto pt-4 border-t border-slate-100 overflow-x-auto no-scrollbar">
                <div className="flex flex-nowrap gap-1.5 pb-1">
                    <DownloadButton format="json" onClick={() => onDownload(translation.id, 'json')} />
                    <DownloadButton format="csv" onClick={() => onDownload(translation.id, 'csv')} />
                    <DownloadButton format="sqlite" onClick={() => onDownload(translation.id, 'sqlite')} />
                    <DownloadButton format="xml" onClick={() => onDownload(translation.id, 'xml')} />
                    <DownloadButton format="xlsx" onClick={() => onDownload(translation.id, 'xlsx')} />
                    <DownloadButton format="sql" onClick={() => onDownload(translation.id, 'sql')} />
                </div>
            </div>
        </div>
    );
}
