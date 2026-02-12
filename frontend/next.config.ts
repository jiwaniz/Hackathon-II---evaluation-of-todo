import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Proxy /api/* and /health to the FastAPI backend (port 8000).
  // The browser only has access to port 7860 (the HF Space port).
  // Next.js rewrites run server-side, so localhost:8000 is reachable.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
      {
        source: "/health",
        destination: "http://localhost:8000/health",
      },
    ];
  },
};

export default nextConfig;
