const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchQuranInfo() {
  const response = await fetch(`${API_BASE_URL}/quran/`);
  if (!response.ok) {
    throw new Error('Failed to fetch Quran info');
  }
  return response.json();
}

export async function fetchAllSurahs() {
  const response = await fetch(`${API_BASE_URL}/surah/`);
  if (!response.ok) {
    throw new Error('Failed to fetch surahs');
  }
  return response.json();
}

export async function fetchSurah(surahNumber: number) {
  const response = await fetch(`${API_BASE_URL}/surah/${surahNumber}`);
  if (!response.ok) {
    throw new Error('Failed to fetch surah');
  }
  return response.json();
}

export async function fetchAyah(surahNumber: number, ayahNumber: number) {
  const response = await fetch(`${API_BASE_URL}/ayah/${surahNumber}/${ayahNumber}`);
  if (!response.ok) {
    throw new Error('Failed to fetch ayah');
  }
  return response.json();
}
