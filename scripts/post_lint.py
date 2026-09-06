#!/usr/bin/env python3
"""글 편집 규칙 검사 — SVG 유무와 길이.

두 가지를 막는다.
  1. SVG 그림이 하나도 없는 글
  2. 3 스크롤을 넘는 글

길이는 글자수가 아니라 **화면 높이 추정**으로 잰다. 표와 그림은 글자 없이
높이를 먹으므로 글자수만 세면 어긋난다. 추정식은 실측 한 점으로 보정했다
(2026-09-05: docstring-is-code 본문 776자 + 표 1개 = 1784px = 1.98 스크롤).

draft: true 인 글은 건너뛴다. 쓰는 중인 글까지 막으면 초안을 못 둔다.

사용: python3 scripts/post_lint.py src/content
"""

import re
import sys
from pathlib import Path

VIEWPORT = 900          # 기준 뷰포트 높이(px)

# 갈래별 상한. 단일 상한(3.0)은 갈래를 구분하지 못했다 —
# 노트에는 과하게 관대하고 긴 글에는 빡빡했다. 2026-09-06 분리.
MAX_SCREENS = {'long': 4.0, 'note': 2.0, 'link': 1.0}
DEFAULT_MAX = 3.0

# 보정된 높이 모델 (px)
# 2026-09-06 재보정. 첫 상수는 26~35% 과대평가해서 상한 안쪽 글을 막았다.
# 실측 두 점으로 다시 맞췄고 오차 1% 안이다.
#   docstring-is-code       글자 1380 · h2 5 · 표행 6 · 그림 1 · 목록 3  → 2535px
#   docstring-writing-guide 글자 1924 · h2 7 · 표행 6 · 코드 31 · 그림 1 · 목록 10 → 4202px
FIXED = 150             # 머리말 + 제목 + 한 마디 + 꼬리
PER_CHAR = 1.1          # 본문 한 글자
PER_H2 = 60             # 소제목 한 개
PER_TABLE_ROW = 40      # 표 한 행
PER_CODE_LINE = 24      # 코드블록 한 줄
PER_SVG = 260           # 그림 한 개
PER_LIST_ITEM = 30      # 목록 한 항목


def split_front(text):
    if not text.startswith('---'):
        return {}, text
    _, front, body = text.split('---', 2)
    meta = {}
    for line in front.splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip().strip('"\'')
    return meta, body


def estimate_px(body):
    svg = len(re.findall(r'<svg\b', body))
    # SVG 안의 텍스트는 본문 글자수에서 뺀다
    prose_src = re.sub(r'<svg\b.*?</svg>', '', body, flags=re.S)

    code_lines = sum(len(b.splitlines()) for b in re.findall(r'```.*?```', prose_src, flags=re.S))
    prose_src = re.sub(r'```.*?```', '', prose_src, flags=re.S)

    h2 = len(re.findall(r'^##\s', prose_src, flags=re.M))
    table_rows = len(re.findall(r'^\|', prose_src, flags=re.M))
    list_items = len(re.findall(r'^\s*[-*]\s|^\s*\d+\.\s', prose_src, flags=re.M))

    prose_src = re.sub(r'^\|.*$', '', prose_src, flags=re.M)
    chars = len(re.sub(r'\s+', '', re.sub(r'[#>|`\-*\[\]()]', '', prose_src)))

    px = (FIXED + chars * PER_CHAR + h2 * PER_H2 + table_rows * PER_TABLE_ROW
          + code_lines * PER_CODE_LINE + svg * PER_SVG + list_items * PER_LIST_ITEM)
    return px, {'글자': chars, '소제목': h2, '표 행': table_rows,
                '코드 줄': code_lines, '그림': svg, '목록': list_items}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else 'src/content')
    if not root.exists():
        sys.exit(f"경로가 없다: {root}")

    files = sorted(root.rglob('*.md'))
    if not files:
        print('검사할 글이 없다.')
        return

    fails, skipped = [], 0
    for f in files:
        meta, body = split_front(f.read_text(encoding='utf-8'))
        if meta.get('draft', '').lower() == 'true':
            skipped += 1
            continue

        px, parts = estimate_px(body)
        screens = px / VIEWPORT
        svg = parts['그림']
        detail = ' · '.join(f'{k} {v}' for k, v in parts.items() if v)
        kind = meta.get('kind', 'note')
        cap = MAX_SCREENS.get(kind, DEFAULT_MAX)

        if svg < 1:
            fails.append((f, f'그림이 없다 — 글마다 SVG 를 하나 이상 넣는다 ({detail})'))
        elif screens > cap:
            over = px - VIEWPORT * cap
            fails.append((f, f'{screens:.1f} 스크롤 — {kind} 상한 {cap} 초과. '
                             f'약 {int(over / PER_CHAR)}자 줄이거나 두 편으로 나눈다 ({detail})'))
        else:
            print(f'  OK   {f.name}  {screens:.1f}/{cap} 스크롤({kind}) · 그림 {svg}개')

    if skipped:
        print(f'  (draft {skipped}편 건너뜀)')

    if fails:
        print(f'\n글 편집 규칙 위반 {len(fails)}건 — 발행 중단', file=sys.stderr)
        for f, why in fails:
            print(f'  FAIL {f}\n       {why}', file=sys.stderr)
        sys.exit(2)

    print(f'post_lint: {len(files) - skipped}편 통과')


if __name__ == '__main__':
    main()
