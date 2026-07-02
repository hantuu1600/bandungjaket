// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    // Pre-bundle heavy dependencies so dev server doesn't recompile them each request
    optimizeDeps: {
      include: ['chart.js/auto', '@lucide/astro'],
    },
    build: {
      // Increase chunk size limit to reduce unnecessary code splitting
      chunkSizeWarningLimit: 600,
    }
  }
});