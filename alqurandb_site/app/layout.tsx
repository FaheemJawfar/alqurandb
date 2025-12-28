import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AlQuranDB - Quran Translations Downloads",
  description: "Download Quran translations in JSON and CSV formats",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta20/dist/css/tabler.min.css"
        />
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"
        />
      </head>
      <body className="antialiased">
        <div className="page">
          {/* Header */}
          <header className="navbar navbar-expand-md d-print-none">
            <div className="container-xl">
              <button
                className="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbar-menu"
              >
                <span className="navbar-toggler-icon"></span>
              </button>
              <h1 className="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
                <a href="/">
                  AlQuranDB
                </a>
              </h1>
              <div className="navbar-nav flex-row order-md-last">
                <div className="nav-item d-none d-md-flex me-3">
                  <div className="btn-list">
                    <a
                      href="https://github.com/FaheemJawfar/alqurandb"
                      className="btn"
                      target="_blank"
                      rel="noreferrer"
                    >
                      <i className="ti ti-brand-github"></i>
                      Source code
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Page wrapper */}
          <div className="page-wrapper">
            {children}
          </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta20/dist/js/tabler.min.js"></script>
      </body>
    </html>
  );
}
