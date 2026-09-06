# colamong 블로그

Astro 기반 개인 기술블로그. 독자는 한국 채용 면접관과 검색으로 들어오는 한국 개발자입니다.

설계 근거는 볼트 `02_Projects/blog/Decisions/ADR-001_블로그_원안_Astro_대분류셋_시안C.md`. **규약을 바꾸려면 ADR 부터 고칩니다.**

## 하네스

| 이름 | 종류 | 담당 |
|---|---|---|
| `astro-expert` | 에이전트 | 레이아웃·스타일·스키마·빌드 설정 |
| `post-editor` | 에이전트 | 볼트 노트 → 글 초안. 저장은 하지 않음 |
| `/blog-post` | 스킬 | 초안 받기 → 저장 → 검사 → 빌드 |
| `scripts/secret_lint.py` | 스크립트 | 기밀 검사 |
| `scripts/post_lint.py` | 스크립트 | 그림·길이 검사 |

판단이 필요한 일만 에이전트가 합니다. 기밀 검사와 길이 계산은 결정적이라 스크립트입니다.

## 고정 규약

| 항목 | 값 |
|---|---|
| 대분류 | `AI` / `Backend·System` / `Develop` **셋 고정** |
| 글 유형 | `long` / `note` / `link`. 기본값 `note` |
| 제목 | 질문형 또는 결론형. 파일명형(`RAG-vs-CAG`) 금지 |
| 그림 | 글마다 인라인 SVG 하나 이상. `currentColor` 로 그립니다 |
| 길이 | 3 스크롤 이하 |
| 디자인 | 시안 C — 액센트는 대분류 라벨에만, 모노와 자간은 영문·숫자에만 |
| 폰트 | Pretendard 자체 호스팅. 외부 CDN 요청 0건 |

## 발행 게이트

`npm run build` 가 `prebuild` 로 검사 둘을 먼저 돌립니다. 걸리면 빌드가 종료 코드 2 로 멈추고 `dist/` 가 갱신되지 않습니다.

**금칙어 목록은 이 저장소에 두지 않습니다.** 저장소가 공개라서, 사내 프로젝트명과 테이블 접두를 여기 적으면 목록 자체가 유출 경로가 됩니다. 목록은 `~/playground/orc/_local/blog-denylist.txt` 에 두고 스크립트가 경로로 읽습니다. 없으면 검사를 건너뛰고 경고만 남기므로, **통과가 안전을 뜻하지 않습니다.**

## 명령

```bash
npm run dev       # 검사 없이 초안 보기
npm run lint      # 검사만
npm run build     # 검사 + 빌드
npm run preview   # 빌드 결과 보기 (http://localhost:4321)
```

## 하지 않을 것

- 사용자 확인 없이 `push`
- 검사를 끄거나 `prebuild` 를 떼기
- 대분류를 넷 이상으로 늘리기
- 썸네일 이미지 만들기 — 글마다 이미지를 만들면 발행 마찰이 커집니다
- 색 리터럴을 CSS 나 SVG 에 박기 — 다크 모드에서 깨집니다
- 볼트 원본 노트 수정

## 배포

GitHub Pages, `build_type=legacy`(브랜치 배포). Astro 산출물을 올리는 방법이 아직 안 정해졌습니다 — `dist/` 커밋과 Actions 방식 변경 중 택해야 합니다. 볼트 ADR-001 §7 참조.
