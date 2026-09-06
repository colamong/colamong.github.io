import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE } from '../site';

export async function GET(context) {
  const posts = (await getCollection('posts', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
  );

  return rss({
    title: SITE.name,
    description: SITE.tagline,
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
