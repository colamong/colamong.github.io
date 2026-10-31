---
title: AI 리뷰어를 속이는 잘못된 근거
date: 2026-10-31
category: AI
kind: long
blurb: 값은 맞았지만, 그 파일은 쓰이지 않았습니다.
featured: false
tags: [ai, review, css, verification]
series: AI 리뷰의 확인 범위
part: 2
---

한 사내 웹 서비스의 기능 소개 페이지를 AI 에이전트가 작업자 모델에게 만들게 했습니다.\
첫 AI 리뷰에서는 완료 조건 5개가 모두 PASS를 받았습니다.\
그런데 색과 폰트의 근거로 쓴 CSS 중에는 현재 화면에서 로드하지 않는 파일이 있었습니다.\
근거 문서에 파일명과 줄 번호, 값까지 적혀 있었는데도요.

## 근거 문서와 실제 로딩 경로

작업을 지시하고 결과를 검토하는 에이전트를 여기서는 오케스트레이터라고 부르겠습니다.\
비공개 저장소를 직접 쓸 수 없어, 2024년 8월 시점의 공개 미러에서 색과 폰트를 확인했습니다.\
확인한 파일·줄·값은 `css-mapping.md`에 남겼습니다.\
완료 조건에는 기존 화면의 CSS를 확인한 근거와 디자인·색감의 통일성이 포함돼 있었습니다.

오케스트레이터는 리뷰 요청서의 원본 목록에 `common.css`, `index.css`, `override.css`, 색 팔레트 JS를 적었습니다.\
첫 리뷰는 근거 문서의 값이 원본과 대부분 일치한다고 판단했습니다.\
글자 대비가 부족한 곳도 찾아냈습니다.\
산출물의 결함을 잡아낸 리뷰였지만, 근거 파일이 화면에서 실제로 로드되는지는 다루지 않았습니다.

같은 요청서를 다른 회사 모델(Codex)에 넘긴 다음 리뷰에서는 앞의 두 완료 조건이 FAIL로 바뀌었습니다.\
이 리뷰는 진입 HTML인 `template.html`의 `<link>` 목록을 근거 문서와 비교했습니다.\
화면이 로드하는 순서는 `normalize.css`, 테마인 `application.min.css`, `override.css`였습니다.\
`index.css`는 현재 `index.html`에서 로드되지 않았고, 백업인 `index.backup.html`에서만 로드되고 있었습니다.

근거 문서의 주요 값은 파일에 실제로 있었습니다.\
다만 지금 화면에 적용되지 않는 파일의 값이었습니다.\
파일에서 값을 찾는 대조와 그 파일이 화면에 쓰이는지 확인하는 대조는 서로 다른 확인이었던 겁니다.

<figure>
<svg viewBox="0 0 640 232" role="img" aria-labelledby="review-css-title review-css-desc" style="width:100%;height:auto">
  <title id="review-css-title">현재 화면과 백업의 CSS 로딩 경로</title>
  <desc id="review-css-desc">현재 화면의 template.html은 normalize.css, application.min.css, override.css를 순서대로 로드한다. override.css는 common.css를 import한다. index.css는 index.backup.html에서만 로드된다.</desc>
  <defs>
    <marker id="review-css-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor"/>
    </marker>
  </defs>
  <g fill="currentColor" font-size="13" font-weight="600">
    <text x="12" y="20">현재 화면</text>
    <text x="12" y="180">백업</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.4">
    <rect x="12" y="62" width="166" height="38" rx="6"/>
    <rect x="232" y="30" width="192" height="104" rx="6"/>
    <rect x="484" y="94" width="144" height="38" rx="6"/>
    <rect x="12" y="190" width="166" height="32" rx="6"/>
    <rect x="232" y="190" width="192" height="32" rx="6"/>
  </g>
  <g fill="currentColor" font-family="ui-monospace, monospace" font-size="13">
    <text x="26" y="86">template.html</text>
    <text x="246" y="54">normalize.css</text>
    <text x="246" y="86">application.min.css</text>
    <text x="246" y="118">override.css</text>
    <text x="500" y="118">common.css</text>
    <text x="26" y="211">index.backup.html</text>
    <text x="246" y="211">index.css</text>
  </g>
  <g fill="none" stroke="currentColor" marker-end="url(#review-css-arrow)">
    <path d="M180 81H226"/>
    <path d="M426 113H478"/>
    <path d="M180 206H226"/>
  </g>
  <g fill="currentColor" font-size="11" text-anchor="middle">
    <text x="204" y="67">link</text>
    <text x="454" y="96">@import</text>
  </g>
</svg>
<figcaption>현재 화면은 어떤 CSS를 불러오고, 그 CSS는 다시 어떤 파일을 불러올까요?</figcaption>
</figure>

## 재검증에서 드러난 폰트와 배경

오케스트레이터는 테마 CSS인 `application.css`를 기준으로 팔레트를 다시 썼습니다.\
그러자 재검증에서 새 문제가 나왔습니다.\
`override.css`의 첫 줄에 `common.css`를 불러오는 `@import`가 있었습니다.

`common.css`의 20줄은 `html, body`에 `"Nanum Gothic" !important`를 지정했습니다.\
24줄은 `body`에 `radial-gradient` 배경을 지정했습니다.\
근거 문서에 적힌 본문 폰트 미지정과 단색 배경 설명은 이 선언들을 반영하지 않은 상태였습니다.\
HTML에 직접 연결된 CSS를 확인한 뒤에도, 그 CSS가 불러오는 파일까지 따라가야 했습니다.\
여러 CSS 선언 중 실제로 적용되는 값을 정하는 cascade 확인이 남아 있었던 겁니다.

`common.css`는 다음 리뷰의 첫 요청서에도 들어 있었습니다.\
하지만 그 리뷰의 첫 결과에는 이 지적이 없었습니다.\
오케스트레이터도 파일을 열어 봤지만 `@import` 관계를 따라가지 않았습니다.\
파일이 목록에 있고 한 번 열어 봤다는 사실만으로는 로딩 관계까지 확인했다고 볼 수 없었습니다.

폰트와 배경을 최종 적용값으로 고친 뒤, 사용자는 확인 범위를 공개 미러의 `template.html` 직접 링크와 `override.css`의 `@import`까지로 한정했습니다.\
그 범위에서 CSS 확인 근거 조건이 PASS를 받아 작업을 마쳤습니다.\
비공개 저장소의 현재 화면까지 검증한 결과는 아닙니다.

## 리뷰 요청의 확인 범위

이 사례만으로 모델 회사별 리뷰 능력을 일반화할 수는 없습니다.\
첫 리뷰가 왜 진입 HTML을 보지 않았는지, 다음 리뷰가 왜 처음에 `@import`를 놓쳤는지도 확인하지 못했습니다.\
확인한 차이는 진입 HTML의 로딩 목록을 대조했을 때 근거 파일의 오류가 드러났다는 점입니다.

이런 CSS 리뷰를 요청할 때는 근거 파일 목록과 함께 화면의 진입 HTML을 지정할 수 있습니다.\
`<link>`에서 시작해 `@import`까지 따라가고, 그 범위에서 폰트와 배경의 최종 적용값을 확인하도록 요청하는 겁니다.\
리뷰 결과에도 파일의 값이 맞는지와 실제로 로드되는지를 각각 남기면 확인 범위를 구별할 수 있습니다.
