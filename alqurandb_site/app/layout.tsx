import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import Script from "next/script";
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
        <Script id="statcounter-config" strategy="afterInteractive">
          {`
            var sc_project=13083427; 
            var sc_invisible=1; 
            var sc_security="f3b0de30"; 
          `}
        </Script>
        <Script
          src="https://www.statcounter.com/counter/counter.js"
          strategy="afterInteractive"
          async
        />
      </body>
    </html>
  );
}
