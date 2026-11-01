---
title: AI 리뷰 요청과 결과 확인의 5가지 기준
date: 2026-11-01
category: AI
kind: long
blurb: 확인 범위와 전제를 요청에 담고, 돌아온 판정을 원본과 대조하는 방법.
featured: false
tags: [ai, review, verification]
series: AI 리뷰의 확인 범위
part: 2
---

[1부](/posts/ai-reviewer-misses-bugs/)에서는 리뷰 자료와 실제 사용 경로의 차이, 빠진 전제, 원본 대조 없이 수용한 지적을 살펴봤습니다.\
AI 리뷰어가 받은 자료를 바탕으로 판단하므로, 이 기준에는 보낼 자료와 돌아온 판정의 확인 방법을 함께 담았습니다.

1부의 사례를 바탕으로, 요청할 때 쓸 기준 2가지와 결과를 확인할 때 쓸 기준 3가지를 정리했습니다.\
실제로 적용한 방법과 아직 제안 단계인 방법을 구분해 적었습니다.

<figure>
<svg viewBox="0 0 640 170" role="img" aria-labelledby="review-checks-title review-checks-desc" style="width:100%;height:auto">
  <title id="review-checks-title">리뷰 요청과 결과 대조의 흐름</title>
  <desc id="review-checks-desc">실제 경로와 전제를 리뷰 요청에 넣고 항목별 근거를 받는다. 추가 리뷰에는 관점을 나누고, 수정 전 원본과 대조해 수용 또는 기각한다.</desc>
  <defs>
    <marker id="review-checks-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-opacity="0.5">
    <rect x="8" y="16" width="188" height="72" rx="6"/>
    <rect x="226" y="16" width="188" height="72" rx="6"/>
    <rect x="444" y="16" width="188" height="72" rx="6"/>
  </g>
  <g fill="none" stroke="currentColor" marker-end="url(#review-checks-arrow)">
    <path d="M198 52H220"/>
    <path d="M416 52H438"/>
  </g>
  <g fill="currentColor" font-size="14" text-anchor="middle">
    <text x="102" y="45" font-weight="600">리뷰 요청</text>
    <text x="102" y="69">실제 경로 · 전제</text>
    <text x="320" y="45" font-weight="600">항목별 판정</text>
    <text x="320" y="69">확인 근거 · 미확인 범위</text>
    <text x="538" y="45" font-weight="600">수용 · 기각</text>
    <text x="538" y="69">원본과의 대조</text>
    <text x="320" y="126">추가 리뷰의 관점 분담</text>
    <text x="320" y="153" font-size="13">충돌한 지적의 원본 대조</text>
  </g>
</svg>
<figcaption>요청에서 수정까지 어떤 근거를 남겨야 할까요?</figcaption>
</figure>

## 1. 실제 사용 경로를 담은 확인 범위

<a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="AI 리뷰어는 CSS 값을 근거 문서와 대조했고, 값은 대부분 맞았습니다. 그런데 그 값을 가져온 파일은 지금 화면이 불러오지 않는 파일이었습니다.">1부의 CSS 사례</a>에서 AI 리뷰어는 근거 문서에 적힌 파일이 실제 화면에 쓰이는지 확인하지 않았습니다.\
이를 확인하려면 진입 HTML이 어떤 CSS를 불러오는지부터 따라가야 했습니다.\
코드 리뷰에서도 변경 파일이 실제로 호출되는지 확인하려면 진입점과 호출 경로를 대조해야 합니다.\
다음처럼 리뷰 요청에 파일 목록과 실제 사용 경로를 함께 적을 수 있습니다.

> 변경 파일을 확인하고, 실제 진입점에서 변경 코드가 호출되는 경로도 대조해 주세요.\
> 호출 관계를 확인한 파일과 확인하지 못한 구간을 함께 적어 주세요.

확인 근거로 적힌 파일이 요청한 경로와 다르다면, 그 결과만으로는 실제 사용 경로를 확인했다고 보기 어렵습니다.

## 2. 판정에 필요한 전제 문서

실제 사용 경로를 확인할 코드와 함께, 그 동작이 옳은지 판단할 규칙도 보내야 합니다.\
<a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="이 AI 리뷰어는 제가 동봉한 자료만 읽을 수 있었는데, 저는 검사 규칙과 스크립트만 보내고 저장소 규칙 문서를 빠뜨렸습니다.">1부의 정규식 사례</a>에서는 제가 저장소 규칙 문서를 보내지 않았습니다.\
그 문서를 함께 보냈다면 AI 리뷰어가 실제 배포 방식을 확인하고 판정할 수 있었을 겁니다.

[GitHub의 저장소 사용자 지정 지침](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)은 Copilot이 프로젝트를 이해할 때 참고할 맥락을 제공합니다.\
이 지침은 Copilot 코드 리뷰에 기본으로 활성화됩니다.\
제가 자료를 직접 골라 보낼 때는 판정을 바꿀 수 있는 규칙이 빠지지 않았는지도 살펴보려 합니다.

| 자료 | 포함 기준 |
|---|---|
| 요구사항 | 정상 동작과 오류 동작의 구분 |
| 저장소 규칙 | 배포 방식이나 명명 규칙처럼 일반적인 예상과 다른 전제 |
| 관련 코드 | 변경 코드의 입력과 출력을 결정하는 주변 동작 |

자료만 읽는 AI 리뷰어에게는 필요한 원문을 동봉해야 합니다.\
파일에 접근할 수 있는 AI 리뷰어에게는 확인할 문서와 관련 절을 지정할 수 있습니다.

## 3. 통과 항목에도 필요한 확인 내역

경로와 전제를 보내도, 답변에 확인 내역이 없으면 AI 리뷰어가 무엇을 대조했는지 알 수 없습니다.\
저는 1부의 기술 문서 리뷰에서 근거 없는 "발행 가능" 답변을 받은 뒤, 요청에 "각 항목을 무엇으로 확인했는지 한 줄씩 적어 달라"는 문장을 넣었습니다.\
그러자 근거가 붙은 답변이 돌아왔습니다.\
다음 요청에서는 결함 목록뿐 아니라 통과한 항목도 표의 4칸으로 받으려 합니다.

| 항목 | 판정 | 확인 근거 | 미확인 범위 |
|---|---|---|---|
| 리뷰 요청의 검토 항목 | 통과 / 결함 / 미확인 | 대조한 원문 위치와 확인 결과 | 자료나 접근 권한 부족 등 |

이 표의 근거로 적힌 원문을 열어 보면 요청한 범위까지 확인했는지 대조할 수 있습니다.\
근거 없는 통과에는 확인 내역을 다시 요청하고, 자료가 부족한 항목은 미확인으로 구별할 수 있습니다.

## 4. 추가 리뷰의 관점 분담

확인 내역을 보고도 덜 다룬 관점이 남는다면, 추가 리뷰에 그 관점을 지정할 수 있습니다.\
여러 리뷰를 합치는 효과를 살핀 [SWR-Bench](https://arxiv.org/html/2509.01494v2) 실험에서는 같은 모델이 같은 PR을 10번 따로 리뷰했습니다.\
그 결과를 합쳤을 때 F1 점수는 한 번만 리뷰했을 때보다 상대적으로 최대 43.67% 높아졌습니다.\
관점을 나누었을 때의 개선율은 이 실험으로 알 수 없습니다.

제 기술 문서에서는 다른 AI 리뷰어가 앞선 리뷰에 없던 결함 2건을 더 찾았습니다.\
하나는 본문의 전제와 그림의 수치가 맞지 않는 문제였습니다.\
다른 하나는 사례 절의 결론이 사례보다 앞서 나간 문제였습니다.

이 문서에서 저는 AI 리뷰어 2곳에 관점을 나누어 맡겼습니다.\
한쪽에는 문장과 작성 규칙을, 다른 쪽에는 독자가 이해하기 어려운 대목과 사실관계 확인을 맡겼습니다.

추가 리뷰의 지적도 원본 대조를 거쳐야 합니다.\
결과가 충돌하면 각 주장의 근거를 확인해야 하므로, 같은 주장에 동의한 AI 리뷰어 수만으로 결정할 수는 없습니다.

## 5. 수정 전 지적별 원본 대조

1부에서 AI 에이전트는 원본을 열어 두고도 <a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="제가 작업을 맡긴 AI 에이전트는 원본 CSS 파일을 열어 두고도, 값의 위치를 실제 140줄이 아닌 AI 리뷰어가 주장한 141줄로 받아들였습니다.">틀린 줄 번호를 따랐습니다</a>.\
정규식 지적은 제가 저장소 규칙 원문과 대조해 기각했습니다.\
[GitHub 공식 문서](https://docs.github.com/en/copilot/responsible-use/code-review)도 리뷰 코멘트를 검증하라고 권고합니다.\
수정 전에는 다음 3가지를 대조하려 합니다.

| 대조 대상 | 확인 내용 | 판단 근거 |
|---|---|---|
| 위치와 값 | 원본의 줄과 실제 값 | 원본 파일 |
| 결함의 전제 | 지적한 조건의 실제 적용 여부 | 요구사항과 저장소 규칙 |
| 문제 동작 | 그 조건에서의 결과 | 관련 코드와 필요한 경우 재현 결과 |

수정을 AI 에이전트에게 맡길 때도 각 지적을 받아들이거나 기각한 이유와 대조한 원본 위치를 먼저 남기도록 요청할 수 있습니다.\
원본과 주장이 어긋나는 항목은 수정을 보류하고, 어느 조건이 다른지부터 확인하겠습니다.

## 출처

- [GitHub 저장소 사용자 지정 지침](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) — 프로젝트 맥락 제공
- [SWR-Bench](https://arxiv.org/html/2509.01494v2) — 2025년, 여러 리뷰의 통합 실험
- [GitHub Copilot 책임 있는 사용 문서](https://docs.github.com/en/copilot/responsible-use/code-review) — 리뷰 코멘트 검증
