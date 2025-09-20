import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [vue(), vueJsx()],
  base: '/Bridge/', // stimmt mit Repo-Namen überein
  esbuild: {
    loader: { '.js': 'jsx' },
  },
})