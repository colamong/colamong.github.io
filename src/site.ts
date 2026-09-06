// 사이트 이름과 태그라인의 유일한 정본.
// 예전에 Base.astro·index.astro·rss.xml.js 세 곳에 흩어져 있어서
// 태그라인을 고칠 때 <title> 과 RSS 에 옛 문구가 남았다.
//
// 검색 결과와 링크 미리보기에 쓰는 설명도 태그라인을 그대로 쓴다.
// 따로 두면 관리할 문장이 하나 늘고, 늘어난 그 문장이 늘 군더더기가 된다.
export const SITE = {
  name: 'colamong',
  tagline: 'AI 백엔드 개발자',
} as const;
