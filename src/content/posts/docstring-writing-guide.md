---
title: 도구 설명에는 못 하는 일까지 적습니다
date: 2026-08-22
category: AI
kind: long
blurb: 공식 지침은 3~4문장부터 시작하라고 합니다.
featured: true
tags: [agent, tool-design, prompt]
---

[에이전트에서는 docstring이 코드다](/posts/docstring-is-code/)에서 docstring이 모델이 보는 인터페이스의 전부라고 썼습니다. 그럼 무엇을 어떻게 적어야 하는가. Anthropic 공식 문서에 답이 있습니다.

> **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance.
>
> — [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)

프롬프트 튜닝이나 모델 교체보다 앞에 놓고 있습니다.

## 네 칸을 채웁니다

<figure>
<svg viewBox="0 0 560 240" role="img" aria-label="도구 설명의 네 칸과 각 칸을 비웠을 때 생기는 실패" style="width:100%;height:auto">
  <g fill="none" stroke="currentColor" stroke-opacity="0.25">
    <rect x="8" y="34" width="252" height="42" rx="6"/>
    <rect x="8" y="86" width="252" height="42" rx="6"/>
    <rect x="8" y="138" width="252" height="42" rx="6"/>
    <rect x="8" y="190" width="252" height="42" rx="6"/>
    <rect x="308" y="34" width="244" height="198" rx="8"/>
  </g>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="14" y="24">설명에 들어갈 네 칸</text>
    <text x="314" y="24">비우면 생기는 일</text>
  </g>
  <g fill="currentColor" font-size="13">
    <text x="24" y="60">무엇을 하나</text>
    <text x="24" y="112">언제 부르나</text>
    <text x="24" y="164">언제 안 부르나</text>
    <text x="24" y="216">무엇을 못 하나</text>
  </g>
  <g fill="currentColor" fill-opacity="0.65" font-size="12">
    <text x="324" y="60">도구를 못 찾습니다</text>
    <text x="324" y="112">엉뚱한 자리에서 부릅니다</text>
    <text x="324" y="164">같은 조회를 반복합니다</text>
    <text x="324" y="216">빈 결과를 받고 지어냅니다</text>
  </g>
  <g stroke="currentColor" stroke-opacity="0.35" fill="none" stroke-dasharray="3 3">
    <path d="M260 55 H308"/>
    <path d="M260 107 H308"/>
    <path d="M260 159 H308"/>
    <path d="M260 211 H308"/>
  </g>
</svg>
<figcaption>네 칸 중 하나를 비우면 대응하는 실패가 옵니다</figcaption>
</figure>

공식 문서가 꼽는 항목과 원문을 나란히 둡니다. 마지막 항목의 표현이 특히 구체적입니다.

| 항목 | 원문 |
|---|---|
| 무엇을 하나 | What the tool does |
| 언제 부르나 | When it should be used (and when it shouldn't) |
| 인자의 뜻과 영향 | What each parameter means and how it affects the tool's behavior |
| 한계 | ...such as what information the tool does **not** return |

## 3~4문장부터 시작합니다

감으로 정하지 않아도 됩니다. 지침에 수치가 있습니다.

> Aim for at least **3–4 sentences** for each tool description, more if the tool is complex.

같은 문서가 좋은 예와 부실한 예를 나란히 놓았습니다. `get_stock_price` 도구의 `description` 만 뽑아 비교하면 차이가 분명합니다.

부실한 예 — 한 문장입니다.

```text
Gets the stock price for a ticker.
```

좋은 예 — 다섯 문장입니다.

```text
Retrieves the current stock price for a given ticker symbol. The ticker
symbol must be a valid symbol for a publicly traded company on a major US
stock exchange like NYSE or NASDAQ. The tool will return the latest trade
price in USD. It should be used when the user asks about the current or
most recent price of a specific stock. It will not provide any other
information about the stock or company.
```

마지막 문장을 보세요. `It will not provide any other information` — 못 하는 일을 명시했습니다. 부실한 예에는 `ticker` 파라미터에 `description` 조차 없습니다.

**길게 쓰라는 지침에는 대가가 붙습니다.** 도구 정의는 요청마다 입력 토큰으로 실려 갑니다. 그래서 설명은 길게 쓰되 도구 목록을 요청마다 바꾸지 않는 편이 낫습니다. 목록이 고정이면 프롬프트 캐싱이 그 구간을 재사용합니다.

## 리뷰 체크리스트

- [ ] 3~4문장 이상인가
- [ ] 언제 **안** 부르는지가 있나
- [ ] 못 하는 일이 있나
- [ ] 모든 파라미터에 `description` 이 있나
- [ ] 인자를 바꿨는데 설명이 그대로는 아닌가

## 출처

- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — 인용한 지침, 좋은 예·부실한 예
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 과금에 포함되는 항목
- [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — 도구 통합·네이밍 심화
