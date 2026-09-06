import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 사용자 사이트라 base 는 루트다. 프로젝트 사이트로 옮기면 base 를 붙여야 한다.
//
// 바깥 링크를 새 창으로 여는 처리는 여기서 하지 않는다.
// Astro 7 의 기본 마크다운 처리기는 Sätteri 라, rehypePlugins 를 쓰려면
// @astrojs/markdown-remark 를 깔아 처리기를 레거시 unified 로 되돌려야 한다.
// 링크 속성 하나 때문에 렌더링 파이프라인 전체를 바꾸는 것은 위험이 더 크다.
// 대신 Base.astro 의 짧은 스크립트가 맡는다.
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
