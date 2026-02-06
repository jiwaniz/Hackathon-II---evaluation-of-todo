const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
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

  // Webpack configuration for path aliases
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    };
    return config;
  },
};

module.exports = nextConfig;
