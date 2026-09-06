import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** 대분류 셋. 늘리지 않는다 — 글이 적을 때 서랍을 늘리면 칸마다 한 편씩 들어가 비어 보인다. */
export const CATEGORIES = ['AI', 'Backend·System', 'Develop'] as const;

/** 글 유형 셋. 기본값은 note — 분류 판단이 마찰이 되면 아무것도 안 쓰게 된다. */
export const KINDS = ['long', 'note', 'link'] as const;

export const KIND_LABEL: Record<(typeof KINDS)[number], string> = {
  long: '긴 글',
  note: '노트',
  link: '링크',
};

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    // 파일명형 제목을 막는다. `RAG-vs-CAG` 같은 제목은 검색에서 공식 문서에 밀린다.
    title: z
      .string()
      .min(6)
      .max(60)
      .refine((t) => /\s/.test(t), '제목에 공백이 없습니다 — 파일명형 제목은 쓰지 않습니다'),
    date: z.coerce.date(),
    category: z.enum(CATEGORIES),
    kind: z.enum(KINDS).default('note'),
    // 목록에 붙는 한 마디. 요약이 아니라 한 마디다.
    blurb: z.string().max(60),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    // kind: 'link' 일 때 원문 주소
    href: z.string().url().optional(),
  }),
});

export const collections = { posts };
