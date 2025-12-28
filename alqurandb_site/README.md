# AlQuranDB Site

Next.js frontend for AlQuranDB project.

## Features

- Browse all Surahs of the Holy Quran
- View Ayahs and their translations
- Responsive design with dark mode support
- TypeScript for type safety
- Tailwind CSS for styling

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update the `.env.local` file with your API URL (default: `http://localhost:8000/api/v1`)

4. Run the development server:
```bash
npm run dev
```

The site will be available at `http://localhost:3000`

## Project Structure

```
alqurandb_site/
├── app/
│   ├── about/
│   │   └── page.tsx
│   ├── surahs/
│   │   └── page.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── lib/
│   └── api.ts
└── public/
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
