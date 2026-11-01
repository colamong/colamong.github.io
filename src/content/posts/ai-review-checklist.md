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

[1부](/posts/ai-reviewer-misses-bugs/)에서는 AI 리뷰어가 결함을 놓치거나 정상 코드를 결함으로 지적하고, AI 에이전트가 틀린 지적을 받아들인 사례를 살펴봤습니다.\
이 3가지 문제는 리뷰를 요청할 때와 결과를 받을 때 각각 대비할 수 있습니다.

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

<a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="AI 리뷰어는 CSS 값을 근거 문서와 대조했고, 값은 대부분 맞았습니다. 그런데 그 값을 가져온 파일은 지금 화면이 불러오지 않는 파일이었습니다.">1부의 CSS 사례</a>에서 AI 리뷰어는 근거 파일이 실제 화면에 쓰이는지 확인하지 않았습니다.\
따라서 프롬프트나 PR 설명에는 파일 목록에 더해 진입점에서 변경 코드까지의 경로를 적는 편이 좋겠습니다.\
다음은 그 방식을 코드 리뷰에 적용한 요청 예시입니다.

> 변경 파일을 확인하고, 실제 진입점에서 변경 코드가 호출되는 경로도 대조해 주세요.\
> 호출 관계를 확인한 파일과 확인하지 못한 구간을 함께 적어 주세요.

이렇게 요청하면 리뷰가 확인하는 범위가 넓어집니다.\
돌아온 결과를 요청한 경로와 비교하면, AI 리뷰어가 어디까지 확인했는지도 알 수 있습니다.\
AI 리뷰어가 호출 관계를 확인하지 못한 구간은 미확인으로 따로 적게 합니다.

## 2. 판정에 필요한 전제 문서

<a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="이 AI 리뷰어는 제가 동봉한 자료만 읽을 수 있었는데, 저는 검사 규칙과 스크립트만 보내고 저장소 규칙 문서를 빠뜨렸습니다.">1부의 정규식 사례</a>는 제가 저장소 규칙 문서를 빠뜨려서 생긴 오판이었습니다.\
빠뜨린 저장소 규칙 문서를 함께 보냈다면, AI 리뷰어가 그 규칙을 보고 판정할 수 있었을 겁니다.

[GitHub의 저장소 사용자 지정 지침](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)도 프로젝트 이해에 필요한 맥락을 제공하는 용도입니다.\
이 지침은 Copilot 코드 리뷰에 기본으로 활성화됩니다.\
제가 자료를 따로 구성해 보내는 경우에도, 판정을 바꿀 수 있는 규칙이 포함됐는지 확인해야 합니다.

| 자료 | 포함 기준 |
|---|---|
| 요구사항 | 정상 동작과 오류 동작의 구분 |
| 저장소 규칙 | 배포 방식·명명 규칙처럼 일반적인 예상과 다른 전제 |
| 관련 코드 | 변경 코드의 입력·출력을 결정하는 주변 동작 |

자료만 읽는 AI 리뷰어에게는 필요한 원문을 동봉하고, 파일에 접근할 수 있다면 확인할 문서와 관련 절을 지정하는 방식으로 요청할 수 있습니다.

## 3. 통과 항목에도 필요한 확인 내역

1부의 기술 문서 리뷰에서 근거 없는 "발행 가능" 답변을 받은 뒤, 저는 요청에 "각 항목을 무엇으로 확인했는지 한 줄씩 적어 달라"는 문장을 넣었습니다.\
그러자 근거가 붙은 답변이 돌아왔습니다.\
다음 요청에서는 결함 목록뿐 아니라 통과한 항목도 아래 표의 4칸으로 받으려 합니다.

| 항목 | 판정 | 확인 근거 | 미확인 범위 |
|---|---|---|---|
| 리뷰 요청의 검토 항목 | 통과·결함·미확인 | 대조한 원문 위치와 확인 결과 | 자료나 접근 권한 부족 등 |

근거가 붙었다고 판정이 맞는 것은 아닙니다.\
제가 그 근거를 열어 요청 범위와 실제 확인 내역이 일치하는지 살펴볼 수 있게 되는 겁니다.\
근거 없는 통과에는 확인 내역을 다시 요청하고, 자료가 부족한 항목은 통과와 구별해 남깁니다.

## 4. 추가 리뷰의 관점 분담

같은 기술 문서를 다른 AI 리뷰어에게도 맡기자, 앞선 리뷰에 없던 결함 2건을 더 찾았습니다.\
하나는 본문의 전제와 그림의 수치가 맞지 않는 문제였고, 다른 하나는 사례 절의 결론이 사례보다 앞서 나간 문제였습니다.\
이 문서에서 저는 AI 리뷰어 2곳에 관점을 나누어 맡겼습니다.\
한쪽에는 문장과 작성 규칙을 맡겼습니다.\
다른 쪽에는 독자가 이해하기 어려운 대목과 사실관계 확인을 맡겼습니다.

[SWR-Bench](https://arxiv.org/html/2509.01494v2)에서는 같은 모델이 같은 PR을 10번 따로 리뷰한 결과를 합치자, F1 점수가 한 번만 리뷰했을 때보다 상대적으로 최대 43.67% 높아졌습니다.\
관점을 나눈 리뷰는 아니지만, 리뷰 한 번의 결과를 그대로 믿기보다 여러 결과를 모아 걸러 내는 편이 낫다는 근거로 볼 수 있습니다.

추가 리뷰를 요청한다면 앞선 리뷰의 확인 내역을 보고, 덜 다룬 관점을 지정할 수 있습니다.\
결과가 충돌할 때는 같은 주장에 동의한 AI 리뷰어 수로 판단하기보다, 각 주장의 근거를 원본과 대조해야 합니다.

## 5. 수정 전 지적별 원본 대조

1부에서 AI 에이전트는 원본을 열어 두고도 <a class="xref" href="/posts/ai-reviewer-misses-bugs/" data-quote="제가 작업을 맡긴 AI 에이전트는 원본 CSS 파일을 열어 두고도, 값의 위치를 실제 140줄이 아닌 AI 리뷰어가 주장한 141줄로 받아들였습니다.">틀린 줄 번호를 따랐습니다</a>.\
정규식 지적은 제가 저장소 규칙 원문과 대조해 기각했습니다.\
[GitHub 공식 문서](https://docs.github.com/en/copilot/responsible-use/code-review)도 리뷰 코멘트를 검증하라고 권고합니다.\
제 작업에서는 수정 전에 다음 3가지를 확인해야 합니다.

| 대조 대상 | 확인 내용 | 판단 근거 |
|---|---|---|
| 위치·값 | 원본의 줄과 실제 값 | 원본 파일 |
| 결함의 전제 | 지적한 조건의 실제 적용 여부 | 요구사항·저장소 규칙 |
| 문제 동작 | 그 조건에서의 결과 | 관련 코드·필요한 경우 재현 결과 |

수정을 AI 에이전트에게 맡길 때도 지적별 수용·기각 이유와 원본 위치를 먼저 남기도록 요청할 수 있습니다.\
원본과 주장이 어긋나면 그 항목의 수정을 보류하고, 어느 조건이 다른지부터 확인합니다.

## 출처

- [GitHub 저장소 사용자 지정 지침](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) — 프로젝트 맥락 제공
- [SWR-Bench](https://arxiv.org/html/2509.01494v2) — 2025년, 여러 리뷰의 통합 실험
- [GitHub Copilot 책임 있는 사용 문서](https://docs.github.com/en/copilot/responsible-use/code-review) — 리뷰 코멘트 검증
