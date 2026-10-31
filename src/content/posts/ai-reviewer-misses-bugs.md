---
title: 당신의 AI 리뷰어가 버그를 놓치는 이유
date: 2026-10-31
category: AI
kind: long
blurb: 놓친 결함, 없는 결함, 틀린 지적을 받아들인 AI 에이전트의 공통점.
featured: false
tags: [ai, review, verification]
series: AI 리뷰의 확인 범위
part: 1
---

기술 문서 2편에서 결함 2건이 더 나왔습니다.\
제가 AI 리뷰어에게 세 번 검토받고, 마지막에는 "발행 가능"이라는 답까지 받은 문서였는데도요.\
3회차 답변은 무엇을 확인했는지 근거 없이 한 줄로 끝났습니다.

다른 작업에서는 정상 코드를 결함으로 지적하거나, 제가 작업을 맡긴 AI 에이전트가 틀린 지적을 받아들이기도 했습니다.\
리뷰 기록을 살펴보니, 다음 세 지점에서 판정과 근거가 어긋났습니다.

| 문제 | 어긋난 지점 | 내 사례 |
|---|---|---|
| 놓친 결함 | 통과 판정과 실제 확인 범위 | "발행 가능" 판정 뒤 추가 결함 |
| 없는 결함의 지적 | 코드 판정과 저장소의 전제 | 올바른 정규식에 대한 수정 요구 |
| 받는 쪽의 흔들림 | 원본과 리뷰 주장 | 틀린 줄 번호를 따른 AI 에이전트 |

## 통과 판정과 실제 확인 범위

AI 리뷰어가 결함을 찾아냈다고 해서 나머지 결함까지 모두 찾았다는 뜻은 아닙니다.\
[SWR-Bench](https://arxiv.org/html/2509.01494v2)는 실제 GitHub PR 1,000건으로 코드 리뷰 성능을 평가했습니다.\
표 8의 PR-Review 구성에서 가장 높은 재현율은 35.93%였습니다.\
재현율은 정답으로 정리된 결함 가운데 리뷰가 찾아낸 비율입니다.

제 기술 문서 리뷰도 앞선 두 차례에는 줄 번호까지 짚었지만, 마지막에는 통과 근거가 빠졌습니다.\
그 한 줄로는 어느 항목을 무엇과 대조했는지, 뒤에 나온 결함이 왜 빠졌는지 알 수 없습니다.\
이 상태에서 "발행 가능"을 문서 전체의 검증 완료로 받아들이면, 실제 확인 범위보다 판정의 의미를 넓히게 됩니다.

한 사내 웹 서비스의 페이지 작업에서도 AI 리뷰어는 CSS 값과 근거 문서를 대조했지만, 주요 값의 출처가 현재 화면에 로드되지 않는 파일이라는 점을 놓쳤습니다.\
다음 AI 리뷰어가 진입 HTML의 파일 목록을 대조하자 그 차이가 드러났습니다.

## 없는 결함과 빠진 전제

[SWR-Bench의 오탐 분석](https://arxiv.org/html/2509.01494v2)에서는 맥락 이해 부족이 48%로 가장 큰 비중을 차지했습니다.\
주변 코드가 정한 논리를 무시한 채 규칙을 적용하는 경우입니다.

제가 사내 문서 검사 스크립트를 리뷰받을 때는 검사 규칙과 스크립트만 자료로 보냈습니다.\
동봉한 자료만 읽을 수 있는 AI 리뷰어에게 저장소 규칙 문서를 빠뜨린 겁니다.\
AI 리뷰어는 자원 이름 정규식이 다른 환경 하나를 놓친다고 지적했습니다.

빠진 문서에는 그 환경이 별도 인프라가 아닌 코드 브랜치이며, 기존 인프라에 배포되어 자원 이름도 기존 것을 쓴다고 적혀 있었습니다.\
따로 자원 이름을 만들 필요가 없으니 정규식도 옳았습니다.\
이 오판은 제가 판정에 필요한 전제를 전달하지 않은 데서 생겼습니다.

지적 7건을 원문과 대조하자 이 1건은 오판이었고, 나머지 6건은 실제 결함이었습니다.\
같은 결과 안에서도 항목마다 필요한 전제와 정답이 달랐습니다.

## 받는 쪽의 흔들림과 원본 대조

리뷰가 틀려도 받는 쪽에서 원본과 대조하면 걸러낼 수 있습니다.\
앞의 페이지 작업에서 제가 작업을 맡긴 AI 에이전트는 원본을 출력해 놓고도, 올바른 140줄 대신 AI 리뷰어가 주장한 141줄을 따랐습니다.

이런 흔들림과 관련해 참고할 연구가 있습니다.\
[2023년 동조 성향 연구](https://arxiv.org/abs/2310.13548)에서는 사용자가 "확실해?"라고 되묻자 AI가 처음 답을 바꾼 비율이 모델별로 32~86%였습니다.\
이는 당시 모델의 측정치이며, 지금 모델의 오류율이나 제 사례의 내부 원인을 뜻하지는 않습니다.\
다만 AI가 원본을 읽었다는 사실만으로, 뒤에 들어온 반박을 올바르게 판단하리라 기대하기는 어렵습니다.

제 사례에서 확인되는 문제는 원본과 리뷰가 어긋났는데도 리뷰 쪽 주장을 채택했다는 점입니다.\
[GitHub 공식 문서](https://docs.github.com/en/copilot/responsible-use/code-review)도 AI 리뷰에 없는 결함이 포함될 수 있으며, 코멘트를 검토한 뒤 조치해야 한다고 설명합니다.

<figure>
<svg viewBox="0 0 640 170" role="img" aria-labelledby="review-gaps-title review-gaps-desc" style="width:100%;height:auto">
  <title id="review-gaps-title">판정과 근거가 어긋나는 세 지점</title>
  <desc id="review-gaps-desc">요청 자료의 전제 누락은 없는 결함의 지적으로, 확인 범위 누락은 결함의 놓침으로, 원본 대조 누락은 틀린 지적의 수용으로 이어질 수 있다.</desc>
  <defs>
    <marker id="review-gaps-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-opacity="0.5">
    <rect x="8" y="12" width="188" height="72" rx="6"/>
    <rect x="226" y="12" width="188" height="72" rx="6"/>
    <rect x="444" y="12" width="188" height="72" rx="6"/>
  </g>
  <g fill="none" stroke="currentColor" marker-end="url(#review-gaps-arrow)">
    <path d="M198 48H220"/>
    <path d="M416 48H438"/>
  </g>
  <g fill="currentColor" text-anchor="middle" font-size="14">
    <text x="102" y="41" font-weight="600">리뷰 요청 자료</text>
    <text x="102" y="65">판정에 필요한 전제</text>
    <text x="320" y="41" font-weight="600">AI 리뷰어의 판정</text>
    <text x="320" y="65">확인 범위</text>
    <text x="538" y="41" font-weight="600">나 · AI 에이전트</text>
    <text x="538" y="65">원본과의 대조</text>
    <text x="102" y="115">없는 결함의 지적</text>
    <text x="320" y="115">놓친 결함</text>
    <text x="538" y="115">틀린 지적의 수용</text>
    <text x="320" y="153" font-size="13">각 단계의 근거와 판정 사이의 불일치</text>
  </g>
</svg>
<figcaption>어느 단계에서 판정과 근거가 어긋났을까요?</figcaption>
</figure>

2부에서는 이 세 지점을 확인할 수 있도록 리뷰 요청서와 결과 대조 방법을 정리합니다.

## 출처

- [SWR-Bench](https://arxiv.org/html/2509.01494v2) — 코드 리뷰의 재현율과 오탐 분석, 표 7·8
- [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548) — 2023년 모델의 반박 이후 응답 변화, §3.2·부록 A.4
- [GitHub Copilot 책임 있는 사용 문서](https://docs.github.com/en/copilot/responsible-use/code-review) — 리뷰의 놓침·오탐과 결과 검증
