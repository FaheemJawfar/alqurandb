import { JSX } from 'react';

interface SearchHeroProps {
    searchTerm: string;
    setSearchTerm: (term: string) => void;
    count: number;
}

export default function SearchHero({ searchTerm, setSearchTerm, count }: SearchHeroProps): JSX.Element {
    return (
        <div className="relative py-24 px-4 flex flex-col items-center justify-center text-center overflow-hidden">
            {/* Background glow effects */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-100 rounded-full blur-[120px] pointer-events-none opacity-60"></div>

            <div className="relative z-10 max-w-3xl w-full">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100 text-blue-600 text-xs font-semibold mb-8 animate-[fade-in_0.7s_ease-out] shadow-sm">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                    </span>
                    Open Source Quran Database
                </div>

                <h1 className="text-5xl md:text-7xl font-bold text-slate-900 tracking-tight mb-6 animate-[slide-up_0.8s_ease-out] leading-tight">
                    Quran Data for <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Everyone</span>
                </h1>

                <p className="text-xl text-slate-600 mb-10 max-w-xl mx-auto leading-relaxed animate-[slide-up_1s_ease-out]">
                    Comprehensive collection of Quran translations in JSON, CSV, SQLite, XML, XLSX, and SQL.
                    Freely available for research, reading, and development.
                </p>

                <div className="relative max-w-xl mx-auto group animate-[slide-up_1.2s_ease-out]">
                    <div className="absolute inset-0 bg-blue-500 rounded-xl blur-lg opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
                    <div className="relative bg-white border border-slate-200 rounded-xl shadow-xl flex items-center p-2 focus-within:border-blue-500/50 focus-within:ring-4 focus-within:ring-blue-500/10 transition-all">
                        <div className="pl-4 text-slate-400">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" /><path d="M21 21l-6 -6" /></svg>
                        </div>
                        <input
                            type="text"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            placeholder="Search by language, translator... (e.g. 'English')"
                            className="w-full bg-transparent border-none text-slate-900 placeholder-slate-400 focus:ring-0 px-4 py-3 outline-none text-lg"
                        />
                        <div className="hidden sm:flex pr-2">
                            <kbd className="hidden sm:inline-block px-3 py-1 bg-slate-100 border border-slate-200 rounded-md text-xs text-slate-500 font-sans font-medium">
                                /
                            </kbd>
                        </div>
                    </div>
                </div>

                <div className="mt-8 flex items-center justify-center gap-2 text-sm text-slate-500 animate-[fade-in_1.5s_ease-out]">
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    {count} translations available for instant download
                </div>
            </div>
        </div>
    );
}
