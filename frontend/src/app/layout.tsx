// DAST Platform — Root Layout

import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'DAST Platform — Dynamic Application Security Testing',
  description: 'Professional-grade DAST platform with Nuclei, OWASP ZAP, and custom fuzzing engines. Real-time vulnerability scanning and reporting.',
  keywords: ['DAST', 'security', 'vulnerability', 'scanner', 'penetration testing'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`} suppressHydrationWarning>
      <body className="antialiased" suppressHydrationWarning>
        <div className="animated-bg" />
        <div style={{ position: 'relative', zIndex: 1 }}>
          {children}
        </div>
      </body>
    </html>
  );
}
