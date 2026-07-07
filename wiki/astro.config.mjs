// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

// Project site (repo Vladoss1409/ModPack): https://vladoss1409.github.io/ModPack/
// In CI GITHUB_REPOSITORY is set automatically, so base becomes /ModPack/.
const repo = process.env.GITHUB_REPOSITORY?.split('/')[1] ?? 'ModPack';
const base =
  process.env.ASTRO_BASE ?? (repo.endsWith('.github.io') ? '/' : `/${repo}/`);

export default defineConfig({
  site: process.env.ASTRO_SITE ?? 'https://vladoss1409.github.io',
  base,
  output: 'static',
  integrations: [react(), tailwind({ applyBaseStyles: false })],
  build: {
    format: 'directory',
  },
});
