import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI News Dashboard",
  description: "Daily curated AI news from around the world",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
