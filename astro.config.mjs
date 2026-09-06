import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 사용자 사이트라 base 는 루트다. 프로젝트 사이트로 옮기면 base 를 붙여야 한다.
export default defineConfig({
  site: 'https://colamong.github.io',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: true,
    },
  },
});
