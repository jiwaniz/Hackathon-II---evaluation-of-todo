import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Disable ESLint during build (run separately in CI)
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Disable TypeScript checks during build (run separately in CI)
  typescript: {
    ignoreBuildErrors: true,
  },

  // Disable SWC minification to reduce memory usage
  swcMinify: false,
};

export default nextConfig;
