#!/usr/bin/env python3
"""기밀 검사 — 사내 내용이 공개 저장소로 나가는 것을 막는다.

**금칙어 목록은 이 저장소에 두지 않는다.** 저장소가 공개라서, 목록에 사내
프로젝트명과 테이블 접두를 적는 순간 목록 자체가 유출 경로가 된다.
목록은 저장소 밖에 두고 경로로만 읽는다.

  기본 경로: ~/playground/orc/_local/blog-denylist.txt
  덮어쓰기:  BLOG_DENYLIST=/다른/경로 python3 scripts/secret_lint.py src/content

목록 파일 형식 — 한 줄에 하나. `#` 로 시작하면 주석. `re:` 로 시작하면 정규식.

  # 사내 시스템
  A-RMS
  re:T_[A-Z]+_[A-Z_]+

목록이 없으면 **검사를 건너뛰고 경고만** 남긴다. 목록이 없는 환경(CI 등)에서
빌드를 막지 않기 위해서다. 대신 로컬 발행 게이트가 유일한 방어선이 된다.

사용: python3 scripts/secret_lint.py src/content
"""

import os
import re
import sys
from pathlib import Path

DEFAULT_LIST = Path.home() / 'playground' / 'orc' / '_local' / 'blog-denylist.txt'

# 목록과 무관하게 항상 막는 것 — 형태만 봐도 새어 나가면 안 되는 값
ALWAYS = [
    (re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b'), 'AWS 액세스 키'),
    (re.compile(r'\bghp_[A-Za-z0-9]{36}\b'), 'GitHub 토큰'),
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'), '개인 키'),
    (re.compile(r'\b\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}\b'), '내부 주소와 포트'),
    (re.compile(r'\b[\w.+-]+@(?!example\.)[\w-]+\.[\w.]+\b'), '이메일 주소'),
]


def load_denylist():
    path = Path(os.environ.get('BLOG_DENYLIST', DEFAULT_LIST))
    if not path.exists():
        return None, path
    rules = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('re:'):
            rules.append((re.compile(line[3:], re.I), f'패턴 {line[3:]}'))
        else:
            rules.append((re.compile(re.escape(line), re.I), f'금칙어 {line}'))
    return rules, path


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else 'src/content')
    if not root.exists():
        sys.exit(f'경로가 없다: {root}')

    deny, deny_path = load_denylist()
    if deny is None:
        print(f'secret_lint: 금칙어 목록이 없어 건너뛴다 ({deny_path})', file=sys.stderr)
        print('  로컬에서 발행하기 전에 목록을 만든다. 지금은 형식 검사만 돈다.', file=sys.stderr)
        deny = []

    rules = ALWAYS + deny
    hits = []
    files = sorted(root.rglob('*.md'))

    for f in files:
        text = f.read_text(encoding='utf-8')
        for i, line in enumerate(text.splitlines(), 1):
            for pattern, label in rules:
                m = pattern.search(line)
                if m:
                    # 어디가 걸렸는지만 보여주고 값 전체는 찍지 않는다
                    found = m.group(0)
                    masked = found[:2] + '…' + found[-2:] if len(found) > 6 else found
                    hits.append((f, i, label, masked))

    if hits:
        print(f'\n기밀 검사 실패 {len(hits)}건 — 발행 중단', file=sys.stderr)
        for f, line, label, masked in hits:
            print(f'  {f}:{line}  {label}  →  {masked}', file=sys.stderr)
        sys.exit(2)

    print(f'secret_lint: {len(files)}편 통과 (규칙 {len(rules)}개)')


if __name__ == '__main__':
    main()
