import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Evolution of Todo",
  description: "A modern, full-stack todo application with authentication and persistence",
  keywords: ["todo", "task management", "productivity"],
  authors: [{ name: "Evolution of Todo Team" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={inter.variable}
      suppressHydrationWarning
      data-new-gr-c-s-check-loaded=""
      data-gr-ext-installed=""
    >
      <body
        className="min-h-screen bg-gray-50 font-sans antialiased"
        suppressHydrationWarning
        data-new-gr-c-s-check-loaded=""
        data-gr-ext-installed=""
      >
        {/* Main content */}
        <main className="flex min-h-screen flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
