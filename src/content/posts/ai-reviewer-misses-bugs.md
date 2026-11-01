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

리뷰를 마친 기술 문서 2편에서 결함 2건이 더 나왔습니다.\
제가 AI 리뷰어에게 3번 검토받고, 마지막에는 "발행 가능"이라는 답까지 받은 문서였는데도요.\
3회차 답변은 근거 없이 한 줄로 끝났습니다.

다른 작업에서는 AI 리뷰어가 정상 코드를 결함으로 지적했습니다.\
제가 작업을 맡긴 AI 에이전트가 틀린 지적을 받아들이기도 했습니다.\
AI 리뷰어는 건네받은 자료 안에서만 판단하므로, 통과 판정만으로 확인이 충분했다고 볼 수는 없습니다.\
리뷰 기록에서는 다음 3가지 문제가 드러났습니다.

<figure>
<svg viewBox="0 0 640 170" role="img" aria-labelledby="review-gaps-title review-gaps-desc" style="width:100%;height:auto">
  <title id="review-gaps-title">판정과 근거가 어긋나는 3가지 지점</title>
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

## 통과 판정과 실제 확인 범위

AI 리뷰어가 결함 몇 개를 찾아냈다고 해서 나머지 결함까지 다 찾은 것은 아닙니다.\
[2026년 4월의 코드 리뷰 비교 연구](https://arxiv.org/abs/2606.15689)는 모델 5개에게 합성 버그 100건과 실제 버그 수정 PR 50건을 리뷰하게 했습니다.\
점수는 F1로 매겼습니다.\
F1은 지적이 얼마나 정확한지와 실제 결함을 얼마나 찾아냈는지를 함께 반영한 값입니다.\
합성 버그에서는 가장 잘한 모델이 0.847을 받았는데, 실제 PR에서는 가장 잘한 모델도 0.066에 그쳤습니다.\
성능 관련 버그는 어느 모델도 거의 찾아내지 못했습니다.\
일부러 심어 둔 버그를 잘 찾는다고 해서 실제 PR의 버그도 잘 찾는 건 아닌 겁니다.\
[GitHub 공식 문서](https://docs.github.com/en/copilot/responsible-use/code-review)도 Copilot이 코드에 있는 문제를 모두 찾지는 못할 수 있다고 적어 두었습니다.

제 기술 문서 리뷰도 앞선 2차례에는 줄 번호까지 짚었지만, 마지막에는 통과 근거가 빠졌습니다.\
그 한 줄로는 어느 항목을 무엇과 대조했는지, 뒤에 나온 결함이 왜 빠졌는지 알 수 없습니다.\
이 상태에서 "발행 가능"을 문서 전체의 검증 완료로 받아들이면, 확인했는지 알 수 없는 부분까지 검증이 끝났다고 믿게 됩니다.

한 사내 웹 서비스의 페이지 작업에서는 결함을 다른 방식으로 놓쳤습니다.\
AI 리뷰어는 CSS 값을 근거 문서와 대조했고, 값은 대부분 맞았습니다.\
그런데 그 값을 가져온 파일은 지금 화면이 불러오지 않는 파일이었습니다.\
다른 AI 리뷰어가 진입 HTML이 불러오는 파일 목록을 확인하고서야 이 차이가 드러났습니다.

## 없는 결함과 빠진 전제

AI 리뷰어는 저장소가 따로 정해 둔 전제를 모르면, 정상 코드도 결함으로 지적할 수 있습니다.\
코드만 보면 빠진 것처럼 보여도, 저장소 규칙으로는 그렇게 쓰는 게 맞는 경우가 있으니까요.

[2026년 7월의 CodeRabbit 현장 연구](https://arxiv.org/abs/2607.03316)는 GitHub 저장소 239개의 PR 10,191건에서 리뷰와 개발자 피드백 31,073쌍을 살펴봤습니다.\
개발자가 거절한 리뷰는 56.3%였습니다.\
개발자는 오탐이거나 중복되거나 범위를 벗어난 제안을 거절했습니다.\
개발자의 의도나 코딩 관행과 맞지 않는 제안도 거절했습니다.\
거절한 리뷰가 모두 없는 결함을 지적한 것은 아닙니다.\
다만 코드로는 그럴듯해도 저장소의 의도와 관행에 맞지 않는 지적을 현장의 개발자도 거절한 겁니다.

사내 문서 검사 스크립트를 리뷰받을 때도 저장소 규칙과 맞지 않는 지적이 나왔습니다.\
이 AI 리뷰어는 제가 동봉한 자료만 읽을 수 있었는데, 저는 검사 규칙과 스크립트만 보내고 저장소 규칙 문서를 빠뜨렸습니다.\
AI 리뷰어는 배포 환경별 자원 이름을 검사하는 정규식이 환경 하나를 빠뜨렸다고 지적했습니다.

빠진 문서에는 그 환경이 별도 인프라가 아닌 코드 브랜치라고 적혀 있었습니다.\
이 환경은 기존 인프라에 배포되므로 자원 이름도 그대로 씁니다.\
정규식에 그 환경의 이름이 없는 게 맞았던 겁니다.

지적 7건을 원문과 대조하자 이 1건은 오판이었고, 나머지 6건은 실제 결함이었습니다.\
오판한 1건만 제가 넘기지 않은 문서가 있어야 판정할 수 있었습니다.

## 틀린 지적의 수용과 원본 대조

앞의 페이지 작업에서 제가 작업을 맡긴 AI 에이전트는 원본 CSS 파일을 열어 두고도, 값의 위치를 실제 140줄이 아닌 AI 리뷰어가 주장한 141줄로 받아들였습니다.\
원본이 바로 앞에 있었는데도 리뷰의 주장을 따른 겁니다.

리뷰 코멘트를 읽는 일과 그 코멘트가 기술적으로 맞는지 가려내는 일은 다릅니다.\
[2026년 9월의 CRJudgeBench 연구](https://arxiv.org/abs/2609.37216)는 실제 PR을 바탕으로 전문가가 검증한 리뷰 코멘트 1,199건으로, AI가 맞는 코멘트와 틀린 코멘트를 구분하는지 시험했습니다.\
최신 범용 LLM도 그럴듯하지만 틀린 코멘트를 가려내기 어려워했습니다.\
리뷰를 받아 코드를 고치는 쪽이 AI 에이전트라면, 이 판단도 그 에이전트가 해야 합니다.

[GitHub 공식 문서](https://docs.github.com/en/copilot/responsible-use/code-review)도 Copilot이 실제로는 없는 결함을 지적할 수 있으니, 코멘트를 검토한 뒤에 조치하라고 안내합니다.\
리뷰가 틀렸더라도 고치기 전에 원본과 다시 대조하면 걸러낼 수 있습니다.

2부에서는 이 3가지를 확인할 수 있도록 리뷰 요청과 결과 대조 방법을 정리합니다.

## 출처

- [Bigger Isn't Always Better: A Comparative Evaluation of LLMs for Automated Code Review](https://arxiv.org/abs/2606.15689) — 2026년 4월, 합성 버그·실제 PR 비교와 성능 관련 버그의 재현율
- [Is Agentic Code Review Helpful? Mining Developers' Feedback to CodeRabbit Reviews in the Wild](https://arxiv.org/abs/2607.03316) — 2026년 7월, CodeRabbit 리뷰에 대한 개발자 피드백과 거절 이유
- [CRJudgeBench: Can AI Detect Plausible but Invalid Code Reviews?](https://arxiv.org/abs/2609.37216) — 2026년 9월, 리뷰 코멘트의 기술적 타당성 판별
- [GitHub Copilot 책임 있는 사용 문서](https://docs.github.com/en/copilot/responsible-use/code-review) — 리뷰의 놓침·오탐과 결과 검증
