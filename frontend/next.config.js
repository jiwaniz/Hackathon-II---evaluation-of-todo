const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode
  reactStrictMode: true,

  // Empty turbopack config to silence warning while using webpack
  turbopack: {},

  // Configure webpack to handle @ alias
  webpack: (config) => {
    config.resolve.alias['@'] = path.resolve(__dirname);
    return config;
  },
};

module.exports = nextConfig;
