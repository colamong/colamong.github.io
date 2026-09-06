---
title: docstring 작성 가이드
date: 2026-08-22
category: AI
kind: long
blurb: 3~4문장부터 시작합니다.
featured: true
tags: [agent, tool-design, prompt]
series: 에이전트 도구 docstring
part: 2
---

[에이전트에서는 docstring이 코드다](/posts/docstring-is-code/)에서 docstring이 모델이 보는 인터페이스의 전부라고 썼습니다. 그럼 무엇을 어떻게 적어야 할까요? Anthropic 공식 문서에 답이 있습니다.

> **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance.
>
> — [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)

프롬프트 튜닝이나 모델 교체보다 알맞은 docstring 작성이 우선입니다.

## 설명을 네 가지로 분류

<figure>
<svg viewBox="0 0 560 240" role="img" aria-label="도구 설명의 네 가지와 각 항목을 누락했을 때 생기는 부작용" style="width:100%;height:auto">
  <g fill="none" stroke="currentColor" stroke-opacity="0.25">
    <rect x="8" y="34" width="252" height="42" rx="6"/>
    <rect x="8" y="86" width="252" height="42" rx="6"/>
    <rect x="8" y="138" width="252" height="42" rx="6"/>
    <rect x="8" y="190" width="252" height="42" rx="6"/>
    <rect x="308" y="34" width="244" height="198" rx="8"/>
  </g>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="14" y="24">설명에 들어갈 네 가지</text>
    <text x="314" y="24">누락시 부작용</text>
  </g>
  <g fill="currentColor" font-size="13">
    <text x="24" y="60">기능</text>
    <text x="24" y="112">호출 시점</text>
    <text x="24" y="164">미호출 시점</text>
    <text x="24" y="216">한계</text>
  </g>
  <g fill="currentColor" fill-opacity="0.65" font-size="12">
    <text x="324" y="60">도구 미탐색</text>
    <text x="324" y="112">오출 — 엉뚱한 자리에서 호출</text>
    <text x="324" y="164">중복 조회</text>
    <text x="324" y="216">빈 결과 후 환각</text>
  </g>
  <g stroke="currentColor" stroke-opacity="0.35" fill="none" stroke-dasharray="3 3">
    <path d="M260 55 H308"/>
    <path d="M260 107 H308"/>
    <path d="M260 159 H308"/>
    <path d="M260 211 H308"/>
  </g>
</svg>
<figcaption>네 가지 중 하나라도 적지 않으면 대응하는 문제가 발생합니다</figcaption>
</figure>

마지막 항목의 원문이 특히 구체적입니다 — such as what information the tool does **not** return.

**Anthropic 뿐만 아니라 OpenAI 문서 역시 같은 지점을 짚습니다.**

> Explicitly describe the purpose of the function and each parameter (and its format), and what the output represents. ... Use the system prompt to describe **when (and when not)** to use each function.
>
> — [Function calling](https://developers.openai.com/api/docs/guides/function-calling)

Anthropic 과 OpenAI 는 공통적으로 기능, 파라미터, 호출·미호출 시점으로 분류합니다. 남은 하나는 Anthropic 이 한계로, OpenAI 가 반환값으로 표현이 다르지만 출력에 대한 기대를 맞춰야 한다는 동일한 의미를 가집니다.

## 시작은 3~4문장으로

> Aim for at least **3–4 sentences** for each tool description, more if the tool is complex.

같은 문서가 `get_stock_price` 도구의 좋은 예와 부실한 예를 나란히 놓았습니다.

부실한 예(한 문장) — `Gets the stock price for a ticker.`

좋은 예(다섯 문장)

```text
Retrieves the current stock price for a given ticker symbol. The ticker
symbol must be a valid symbol for a publicly traded company on a major US
stock exchange like NYSE or NASDAQ. The tool will return the latest trade
price in USD. It should be used when the user asks about the current or
most recent price of a specific stock. It will not provide any other
information about the stock or company.
```

네 가지가 문장마다 배분돼 있습니다.

| 문장 | 담은 것 |
|---|---|
| 첫 문장 | 기능 — `Retrieves the current stock price` |
| 두세 번째 | 파라미터 제약과 반환 형식 |
| 네 번째 | 호출 시점 — `It should be used when...` |
| 마지막 | 한계 — `It will not provide any other information` |

부실한 예에는 `ticker` 파라미터에 `description` 조차 없습니다.

**길게 쓰라는 지침에는 트레이드오프가 존재합니다.** 도구 정의는 요청마다 입력 토큰으로 실려 비용이 발생합니다. 그래서 설명은 길게 쓰되 목록을 요청마다 바꾸지 않는 편이 낫습니다. 앞단이 고정되면 캐싱으로 재사용해 비용을 줄일 수 있기 때문입니다. 캐싱은 `cache_control` 로 켤 수 있습니다.

## 리뷰 체크리스트

- [ ] 3~4문장 이상인지
- [ ] 미호출 시점을 적었는지
- [ ] 한계를 적었는지
- [ ] 모든 파라미터에 `description` 이 있는지
- [ ] 인자를 바꾸고 설명을 그대로 두지 않았는지

## 출처

- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — 인용 지침과 예시
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 과금 항목
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling) — OpenAI 쪽 같은 지침
- [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — 심화
