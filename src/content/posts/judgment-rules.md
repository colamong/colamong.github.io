---
title: 판단이 필요한 규칙을 지키게 하는 방법
date: 2026-09-30
category: AI
kind: long
blurb: 쪼개 보면 대부분은 스크립트로 검사할 수 있습니다.
featured: false
draft: false
tags: [agent, claude-code, hooks, llm-as-a-judge]
series: AI 에이전트 규칙 관리
part: 2
---

1부는 셸 명령으로 판정할 수 없는 규칙이 남는다는 문제로 끝났습니다.\
그런데 이런 규칙도 쪼개 보면 대부분은 스크립트로 검사할 수 있습니다.\
기계가 판정할 수 없는 나머지는 두 번째 모델에게 맡기고, 그 모델의 판정은 사람이 보정합니다.\
Anthropic과 OpenAI의 문서, GitLab·Datadog 문서팀의 사례가 이 순서를 뒷받침합니다.

<figure>
<svg viewBox="0 0 560 170" role="img" aria-label="명사형 규칙이 기계가 판정할 수 있는 끝맺음 검사와 판단이 필요한 오판·누락 사례로 나뉜다" style="width:100%;height:auto">
  <defs>
    <marker id="arw3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-opacity="0.35">
    <rect x="8" y="55" width="150" height="60" rx="6"/>
    <rect x="250" y="10" width="302" height="66" rx="6"/>
    <rect x="250" y="94" width="302" height="66" rx="6" stroke-dasharray="4 4"/>
  </g>
  <g fill="currentColor">
    <text x="22" y="82" font-size="13" font-weight="600">명사형 규칙</text>
    <text x="22" y="100" font-size="11" fill-opacity="0.55">소제목 25개</text>
    <text x="264" y="36" font-size="13" font-weight="600">끝맺음 검사</text>
    <text x="264" y="56" font-size="11" fill-opacity="0.55">실행 주체: 정규식 · 8개 적중</text>
    <text x="264" y="120" font-size="13" font-weight="600">오판·누락 사례</text>
    <text x="264" y="140" font-size="11" fill-opacity="0.55">판단이 필요 · 오판 1개, 누락 1개</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.55" marker-end="url(#arw3)">
    <path d="M158 78 L244 46"/>
    <path d="M158 92 L244 126"/>
  </g>
</svg>
<figcaption>같은 규칙 안에서도 기계가 판정할 수 있는 부분과 판단이 필요한 부분이 나뉩니다</figcaption>
</figure>

## 규칙의 두 부분

첫 단계는 규칙 하나를 기계가 검사할 수 있는 부분과 판단이 필요한 부분으로 나누는 것입니다.\
[GitLab 문서팀](https://docs.gitlab.com/development/documentation/testing/vale/)은 문체 린터 Vale의 규칙을 강제 등급으로 나눕니다.\
렌더링을 깨뜨리는 규칙은 오류로 두고, 일반 문체 규칙은 경고로 둡니다.\
주관적인 규칙은 일부러 자동화하지 않습니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">If the rule is too subjective, it cannot be adequately enforced and creates unnecessary additional warnings.</span><span class="quote-ko">규칙이 너무 주관적이면 제대로 강제할 수 없고, 불필요한 경고만 늘어납니다.</span></label>
</blockquote>

OpenAI도 [Codex 코드 리뷰 규칙](https://developers.openai.com/blog/custom-code-review-rules-for-codex)을 같은 기준으로 나눕니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">Keep formatting and other mechanical checks in CI.</span><span class="quote-ko">서식 검사처럼 기계적인 검사는 CI에 두세요.</span></label>
</blockquote>

## 정규식 한 줄의 실험

명사형 규칙에서 기계가 검사할 수 있는 부분은 소제목의 끝맺음입니다.\
소제목이 `~니다`·`~요`·`~나`·`~까` 등으로 끝나면 문장형으로 판정하는 정규식을 만들었습니다.\
이 블로그의 커밋 기록과 작성 중인 글에 있는 소제목 25개에 돌린 결과입니다.

| 항목 | 개수 | 예시 |
|---|---|---|
| 맞게 잡은 문장형 소제목 | 8 | `네 칸을 채웁니다` |
| 잘못 잡은 명사형 소제목 | 1 | `판단 기준은 하나` |
| 놓친 문장형 소제목 | 1 | `Docstring을 리뷰하자` |

정규식 한 줄로 문장형 소제목 9개 중 8개를 잡았습니다.\
반면 `하나`처럼 명사가 `~나`로 끝나면 문장형으로 잘못 판정합니다.\
`~자`로 끝나는 청유형은 목록에 없어서 놓쳤습니다.\
`~자`를 목록에 추가하면 놓친 경우는 줄일 수 있습니다.\
반면 `사용자`처럼 `~자`로 끝나는 명사도 잘못 잡게 됩니다.\
목록을 늘릴수록 잘못 잡는 경우도 함께 늘어납니다.\
이런 경우가 판단이 필요한 부분으로 넘어갑니다.

그렇다면 판단이 필요한 부분은 누가 판정해야 할까요?\
규칙을 따르는 모델에게 다시 맡기면 1부의 문제로 돌아갑니다.

## 판정을 맡는 두 번째 모델

규칙을 따르는 모델과 따로, 판정만 맡는 모델을 **LLM 심판**(LLM-as-a-judge)이라고 부릅니다.\
Claude Code에서는 [프롬프트 훅](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks)이 이 역할을 합니다.\
프롬프트 훅은 이벤트가 생기면 셸 명령 대신 모델에게 판정 질문을 보냅니다.\
Stop 훅에서 심판이 `"ok": false`를 돌려주면 에이전트는 작업을 끝내지 못하고, 판정 사유를 다음 지시로 받습니다.

같은 구조의 장치를 다른 곳도 제공합니다.

| 제공처 | 장치 | 판정 대상 |
|---|---|---|
| Anthropic | 프롬프트 훅 · `/goal` | 이벤트 조건 · 작업 완료 여부 |
| OpenAI | [Agents SDK 가드레일](https://openai.github.io/openai-agents-python/guardrails/) | 에이전트 입력·출력 |
| AWS | [Bedrock 모델 평가](https://aws.amazon.com/blogs/machine-learning/llm-as-a-judge-on-amazon-bedrock-model-evaluation/) | 지시 준수 · 문체와 톤 |

세 장치 모두 판정을 돌리는 시점은 설정으로 정하고, 판정 자체는 모델이 합니다.

## LLM 심판의 한계

LLM 심판의 판정도 흔들립니다.\
[MT-Bench 논문](https://arxiv.org/abs/2306.05685)은 강한 심판 모델이 사람 판정과 80% 넘게 일치한다고 보고했습니다.\
같은 논문은 답의 순서, 답의 길이, 자기 답을 선호하는 편향도 함께 보고했습니다.\
IBM Research가 참여한 [ICLR 2025 논문](https://research.ibm.com/publications/justice-or-prejudice-quantifying-biases-in-llm-as-a-judge)은 이런 편향을 12가지로 정리했습니다.

| 출처 | 한계를 줄이는 방법 |
|---|---|
| [OpenAI](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | 점수 대신 통과·실패로 판정하기 |
| [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 사람의 판정으로 심판을 보정하기 |
| Claude Code | 리뷰어에게 요구사항에 영향을 주는 결함만 보고하게 하기 |

[Claude Code 문서](https://code.claude.com/docs/en/best-practices)는 마지막 방법의 이유를 이렇게 설명합니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do.</span><span class="quote-ko">결함을 찾으라는 지시를 받은 리뷰어는 작업에 문제가 없어도 대개 무언가를 보고합니다. 그렇게 하라고 요청받았기 때문입니다.</span></label>
</blockquote>

## 3단계 배치

<figure>
<svg viewBox="0 0 560 178" role="img" aria-label="규칙 위반 후보가 결정적 검사, LLM 심판, 사람 검토를 차례로 거치고, 사람 검토 결과가 LLM 심판의 질문을 고치는 데 다시 쓰인다" style="width:100%;height:auto">
  <defs>
    <marker id="arw2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-opacity="0.35">
    <rect x="8" y="30" width="160" height="72" rx="6"/>
    <rect x="200" y="30" width="160" height="72" rx="6"/>
    <rect x="392" y="30" width="160" height="72" rx="6"/>
  </g>
  <g fill="currentColor">
    <text x="8" y="18" font-size="11" fill-opacity="0.55">1단계</text>
    <text x="200" y="18" font-size="11" fill-opacity="0.55">2단계</text>
    <text x="392" y="18" font-size="11" fill-opacity="0.55">3단계</text>
    <text x="20" y="56" font-size="13" font-weight="600">결정적 검사</text>
    <text x="20" y="76" font-size="11" fill-opacity="0.55">정규식 · 린터</text>
    <text x="20" y="92" font-size="11" fill-opacity="0.55">실행 주체: 스크립트</text>
    <text x="212" y="56" font-size="13" font-weight="600">LLM 심판</text>
    <text x="212" y="76" font-size="11" fill-opacity="0.55">프롬프트 훅</text>
    <text x="212" y="92" font-size="11" fill-opacity="0.55">실행 주체: 하네스</text>
    <text x="404" y="56" font-size="13" font-weight="600">사람 검토</text>
    <text x="404" y="76" font-size="11" fill-opacity="0.55">오판 사례 확인</text>
    <text x="404" y="92" font-size="11" fill-opacity="0.55">실행 주체: 사람</text>
    <text x="232" y="166" font-size="11" fill-opacity="0.55">심판 질문 보정</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.55" marker-end="url(#arw2)">
    <path d="M168 66 H194"/>
    <path d="M360 66 H386"/>
    <path d="M472 102 V140 H280 V108"/>
  </g>
</svg>
<figcaption>기계가 판정할 수 있는 부분부터 걸러 내고, 남은 판단만 다음 단계로 넘깁니다</figcaption>
</figure>

Anthropic은 [에이전트 평가 글](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)에서 이 순서를 권합니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">We recommend choosing deterministic graders where possible, LLM graders where necessary or for additional flexibility, and using human graders judiciously for additional validation.</span><span class="quote-ko">가능하면 결정적 채점기를 쓰고, 필요하거나 유연성이 더 필요할 때는 LLM 채점기를 쓰기를 권합니다. 추가 검증에는 사람 채점자를 신중하게 씁니다.</span></label>
</blockquote>

Datadog 문서팀은 [기여 안내서](https://github.com/DataDog/documentation/blob/master/CONTRIBUTING.md)에 같은 판단을 적어 두었습니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">AI tools may not follow the Datadog documentation style guide or Vale linting rules. Run <code>vale</code> on your changes and fix any issues before submitting.</span><span class="quote-ko">AI 도구는 Datadog 문서 스타일 가이드나 Vale 린트 규칙을 따르지 않을 수 있습니다. 제출하기 전에 변경 사항에 <code>vale</code>을 실행해 문제를 고치세요.</span></label>
</blockquote>

## 규칙을 적는 순서

새 규칙이 생기면 다음 순서로 규칙을 둘 자리를 정합니다.

1. **기계가 판정할 수 있는 부분을 찾습니다.** 명사형 규칙이라면 소제목의 끝맺음입니다.
2. **그 부분을 빌드 앞 검사 스크립트로 만듭니다.** 이 검사는 모델이 건너뛸 수 없습니다.
3. **스크립트가 판정할 수 없는 부분은 LLM 심판에게 맡깁니다.** 프롬프트 훅이 심판에게 판정 질문을 보냅니다.
4. **심판이 잘못 판정한 사례는 사람이 확인합니다.** 확인한 사례로 심판의 질문을 고칩니다.
5. **마지막으로 규칙의 의도와 예시를 문서에 적습니다.** 문서는 강제 장치가 아니라 모델이 처음부터 규칙에 맞게 쓰도록 돕는 안내입니다.

명사형 규칙은 이 순서를 거꾸로 밟았습니다.\
5단계인 문서부터 적었고, 1~4단계는 없었습니다.\
1단계부터 시작했다면 같은 날 3번 어긴 소제목 중 끝맺음 위반은 빌드에서 멈췄을 것입니다.

## 출처

- [Vale documentation tests](https://docs.gitlab.com/development/documentation/testing/vale/) — GitLab. Vale 규칙의 강제 등급
- [Custom Code Review rules for Codex](https://developers.openai.com/blog/custom-code-review-rules-for-codex) — OpenAI. 기계적 검사와 리뷰 규칙의 분리
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) — Anthropic. 프롬프트 훅과 `"ok"` 판정
- [Guardrails](https://openai.github.io/openai-agents-python/guardrails/) — OpenAI Agents SDK
- [LLM-as-a-judge on Amazon Bedrock Model Evaluation](https://aws.amazon.com/blogs/machine-learning/llm-as-a-judge-on-amazon-bedrock-model-evaluation/) — AWS, 2025-02-12
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) — Zheng 외, NeurIPS 2023
- [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://research.ibm.com/publications/justice-or-prejudice-quantifying-biases-in-llm-as-a-judge) — ICLR 2025
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — OpenAI
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) — Anthropic. 리뷰어의 과잉 지적
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic, 2026-01-09
- [Datadog documentation CONTRIBUTING.md](https://github.com/DataDog/documentation/blob/master/CONTRIBUTING.md) — Datadog
