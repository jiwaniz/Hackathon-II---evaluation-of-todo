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

  // Use webpack explicitly (more stable than Turbopack for production)
  webpack: (config) => {
    // Disable minification to save memory
    config.optimization.minimize = false;
    return config;
  },
};

module.exports = nextConfig;
