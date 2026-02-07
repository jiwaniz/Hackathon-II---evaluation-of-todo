/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode
  reactStrictMode: true,

  // Disable ESLint during build (run separately)
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Disable TypeScript checks during build (run separately)
  typescript: {
    ignoreBuildErrors: true,
  },
};

module.exports = nextConfig;
