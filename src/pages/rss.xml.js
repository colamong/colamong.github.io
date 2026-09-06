import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('posts', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
  );

  return rss({
    title: 'colamong',
    description: '에이전트를 실제로 굴리면서 남기는 기록',
    site: context.site,
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.blurb,
      pubDate: p.data.date,
      categories: [p.data.category],
      link: p.data.kind === 'link' && p.data.href ? p.data.href : `/posts/${p.id}/`,
    })),
  });
}
