import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AlQuranDB - Premium Quran Data",
  description: "Comprehensive collection of Quran translations in JSON, CSV, SQLite, XML, XLSX, and SQL formats. Built for developers.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full" suppressHydrationWarning>
      <body className={`${outfit.className} antialiased bg-slate-50 text-slate-900 min-h-screen flex flex-col`}>
        {children}
      </body>
    </html>
  );
}
