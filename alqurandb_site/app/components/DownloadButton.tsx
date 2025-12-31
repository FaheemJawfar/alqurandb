import { JSX } from 'react';
import { FileJson, FileSpreadsheet, Database, FileCode, FileText } from 'lucide-react';

interface DownloadButtonProps {
    format: 'json' | 'csv' | 'sqlite' | 'xml' | 'xlsx';
    onClick: () => void;
}

const formatConfig = {
    json: {
        color: 'bg-white text-yellow-700 border-yellow-200 hover:border-yellow-400 hover:bg-yellow-50',
        icon: <FileJson size={14} strokeWidth={2.5} />,
        label: 'JSON'
    },
    csv: {
        color: 'bg-white text-green-700 border-green-200 hover:border-green-400 hover:bg-green-50',
        icon: <FileText size={14} strokeWidth={2.5} />,
        label: 'CSV'
    },
    sqlite: {
        color: 'bg-white text-blue-700 border-blue-200 hover:border-blue-400 hover:bg-blue-50',
        icon: <Database size={14} strokeWidth={2.5} />,
        label: 'SQLite'
    },
    xml: {
        color: 'bg-white text-orange-700 border-orange-200 hover:border-orange-400 hover:bg-orange-50',
        icon: <FileCode size={14} strokeWidth={2.5} />,
        label: 'XML'
    },
    xlsx: {
        color: 'bg-white text-emerald-700 border-emerald-200 hover:border-emerald-400 hover:bg-emerald-50',
        icon: <FileSpreadsheet size={14} strokeWidth={2.5} />,
        label: 'XLSX'
    },
};

export default function DownloadButton({ format, onClick }: DownloadButtonProps): JSX.Element {
    const config = formatConfig[format];

    return (
        <button
            onClick={(e) => {
                e.stopPropagation();
                onClick();
            }}
            className={`
        px-3 py-1.5 rounded-lg text-xs font-bold
        transition-all duration-200 uppercase tracking-wide
        border shadow-sm hover:shadow-md hover:-translate-y-0.5 active:translate-y-0
        flex items-center gap-2 cursor-pointer
        ${config.color}
      `}
            title={`Download ${config.label}`}
        >
            <span className="opacity-70">{config.icon}</span>
            {config.label}
        </button>
    );
}
