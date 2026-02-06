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

  // Optimize build for low memory environments
  experimental: {
    workerThreads: false,
    cpus: 1,
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Path aliases
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    };

    // Reduce memory usage
    config.optimization = {
      ...config.optimization,
      minimize: false, // Disable minification to save memory
    };

    // Limit parallel processing to reduce memory
    config.parallelism = 1;

    return config;
  },
};

module.exports = nextConfig;
