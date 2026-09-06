---
title: 에이전트에서는 docstring이 코드다
date: 2026-08-21
category: AI
kind: long
blurb: 주석이 아니라 인터페이스입니다.
featured: true
tags: [agent, tool-design, prompt]
series: 에이전트 도구 docstring
part: 1
---

일반 코드에서 docstring은 사람을 위한 설명입니다. 프로그램에 영향을 주지 않습니다. 그래서 바쁘면 생략하고, 시그니처만 봐도 알 만하면 한 줄로 끝내는 경우가 많습니다.

하지만 에이전트가 부르는 도구에서는 다릅니다. **docstring이 모델이 보는 인터페이스의 전부입니다.**

<figure>
<svg viewBox="0 0 560 250" role="img" aria-label="저장소에는 함수 본문이 있지만 모델에게는 이름과 스키마와 docstring만 전달된다" style="width:100%;height:auto">
  <defs>
    <marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-opacity="0.25">
    <rect x="8" y="30" width="210" height="200" rx="8"/>
    <rect x="342" y="30" width="210" height="150" rx="8"/>
  </g>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="14" y="20">저장소에 있는 것</text>
    <text x="348" y="20">모델이 받는 것</text>
  </g>
  <g fill="currentColor" font-size="13">
    <text x="26" y="62">이름</text>
    <text x="26" y="102">파라미터 스키마</text>
    <text x="26" y="142">docstring</text>
    <text x="360" y="62">이름</text>
    <text x="360" y="102">파라미터 스키마</text>
    <text x="360" y="142">docstring</text>
  </g>
  <g fill="currentColor" fill-opacity="0.4">
    <text x="26" y="196" font-size="13">함수 본문</text>
    <text x="26" y="215" font-size="11">여기서 멈춥니다</text>
  </g>
  <g stroke="currentColor" stroke-opacity="0.2">
    <line x1="20" y1="76" x2="206" y2="76"/>
    <line x1="20" y1="116" x2="206" y2="116"/>
    <line x1="20" y1="166" x2="206" y2="166"/>
    <line x1="354" y1="76" x2="540" y2="76"/>
    <line x1="354" y1="116" x2="540" y2="116"/>
  </g>
  <g stroke="currentColor" stroke-opacity="0.55" fill="none" marker-end="url(#tip)">
    <path d="M232 57 H332"/>
    <path d="M232 97 H332"/>
    <path d="M232 137 H332"/>
  </g>
  <path d="M232 192 h56" stroke="currentColor" stroke-opacity="0.3" stroke-dasharray="4 4" fill="none"/>
  <text x="296" y="197" fill="currentColor" fill-opacity="0.45" font-size="15">✕</text>
</svg>
<figcaption>함수 본문은 모델에게 가지 않습니다</figcaption>
</figure>

## Model 과 docstring

API 필드 이름은 `description` 입니다. Python SDK 는 함수의 docstring 을 그 필드에 그대로 넣고, `Args:` 절을 파라미터 설명으로 씁니다.

도구를 등록하면 모델에게 전달되는 것은 이름과 파라미터 스키마와 이 설명뿐입니다. 함수 본문은 안 갑니다. 즉 모델 입장에서 이 도구가 무엇을 하는지 알 방법은 docstring 하나뿐입니다.

공식 문서도 같은 말을 합니다. [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) 첫 문단은 이렇게 시작합니다.

> Claude determines when to call a tool based on the user's request and **the tool's description**.

구현을 아무리 정확히 짜도, docstring이 "데이터를 조회합니다" 수준이면 모델은 언제 이 도구를 불러야 하는지 알 수 없습니다. 부르지 않거나, 엉뚱한 자리에서 부를 수 있습니다.

## 조용한 실패

이 문제가 고약한 건 에러가 안 난다는 점입니다. 도구를 안 부르면 모델은 그냥 아는 대로 답합니다. 로그에는 실패가 남지 않습니다. 사용자만 "왜 이건 안 찾아보지" 하고 불편을 느낍니다.

그래서 도구를 추가한 뒤에는 모델이 그 도구를 실제로 불렀는지를 따로 확인해야 합니다. 호출 로그에 도구 이름이 안 보이면 구현이 아니라 설명을 의심해야 합니다.

## 무엇을 적어야 하나

시그니처가 이미 말하는 것은 빼고, 시그니처가 말 못 하는 것을 적습니다.

| 적을 것 | 예 |
|---|---|
| 언제 부르는가 | 사용자가 특정 기간의 수치를 물을 때 |
| 언제 안 부르는가 | 이미 앞 턴에서 같은 기간을 조회했으면 |
| 무엇을 못 하는가 | 미래 날짜는 빈 결과가 돌아온다 |
| 인자의 실제 형식 | 날짜는 `YYYY-MM-DD`, 시간대는 KST 고정 |

"무엇을 못 하는가"가 특히 중요합니다. 모델은 도구가 만능이라고 가정하고 부릅니다. 한계를 안 적으면 빈 결과를 받고 나서 스스로 지어냅니다.

네 항목을 실제로 어떻게 쓰는지는 [docstring 작성 가이드](/posts/docstring-writing-guide/)에서 공식 지침과 예시로 다뤘습니다.

## Docstring을 리뷰하자

코드 리뷰에서 docstring은 보통 "있으면 좋고" 항목입니다. 에이전트 도구에서는 시그니처 변경과 같은 급으로 봅니다. 인자를 하나 추가하고 docstring을 안 고치면, 모델은 새 인자를 인식하지 못하고 계속 예전 방식을 유지합니다.

동작이 바뀌었는데 설명이 그대로면 그건 깨진 인터페이스입니다.

## 출처

- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 도구 호출 판단이 description 에 달려 있다는 서술, 전달되는 필드 구성
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — `name`·`description`·`input_schema` 정의와 작성 지침
- [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic 엔지니어링 블로그. 도구 통합·네이밍·응답 설계
