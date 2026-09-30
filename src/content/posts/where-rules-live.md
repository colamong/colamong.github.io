---
title: AI가 규칙을 어기는 이유
date: 2026-09-19
category: AI
kind: long
blurb: 문서에 적는 것과 훅에 거는 것은 다릅니다.
featured: false
draft: false
tags: [agent, claude-code, hooks]
series: AI 에이전트 규칙 관리
part: 1
---

AI 에이전트에게 규칙을 지키게 하려면 규칙의 내용보다 **규칙을 두는 위치**를 먼저 정해야 합니다.\
같은 문장이라도 어디에 두느냐에 따라 강제력이 달라집니다.

<figure>
<svg viewBox="0 0 560 334" role="img" aria-label="하네스 안에 모델이 읽는 글(인스트럭션, 메모리, 스킬, 서브에이전트 정의)과 하네스 설정(권한 규칙, 훅)이 있고, 빌드 스크립트는 하네스 밖에 있다" style="width:100%;height:auto">
  <g fill="currentColor">
    <rect x="8" y="8" width="544" height="252" rx="8" fill="none" stroke="currentColor" stroke-opacity="0.45"/>
    <text x="20" y="30" font-size="13" font-weight="600">하네스 (Claude Code)</text>
    <rect x="20" y="44" width="320" height="204" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.25"/>
    <text x="32" y="64" font-size="12" font-weight="600">모델이 읽는 글</text>
    <text x="32" y="86" font-size="11" fill-opacity="0.55">세션 시작부터</text>
    <text x="32" y="168" font-size="11" fill-opacity="0.55">부를 때만</text>
    <text x="32" y="240" font-size="11" fill-opacity="0.55">실행 주체: 모델</text>
    <rect x="32" y="94" width="142" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="44" y="116" font-size="13">인스트럭션</text>
    <text x="44" y="134" font-size="11" fill-opacity="0.55" font-family="ui-monospace, monospace">CLAUDE.md · rules/</text>
    <rect x="186" y="94" width="142" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="198" y="116" font-size="13">메모리</text>
    <text x="198" y="134" font-size="11" fill-opacity="0.55" font-family="ui-monospace, monospace">memory/</text>
    <rect x="32" y="176" width="142" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="44" y="198" font-size="13">스킬</text>
    <text x="44" y="216" font-size="11" fill-opacity="0.55" font-family="ui-monospace, monospace">.claude/skills/</text>
    <rect x="186" y="176" width="142" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="198" y="198" font-size="13">서브에이전트 정의</text>
    <text x="198" y="216" font-size="11" fill-opacity="0.55" font-family="ui-monospace, monospace">.claude/agents/</text>
    <rect x="352" y="44" width="188" height="204" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.25"/>
    <text x="364" y="64" font-size="12" font-weight="600">하네스 설정</text>
    <text x="364" y="84" font-size="11" fill-opacity="0.55" font-family="ui-monospace, monospace">settings.json</text>
    <text x="364" y="240" font-size="11" fill-opacity="0.55">실행 주체: 하네스</text>
    <rect x="364" y="94" width="164" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="376" y="116" font-size="13">권한 규칙</text>
    <text x="376" y="134" font-size="11" fill-opacity="0.55" >도구 호출마다</text>
    <rect x="364" y="176" width="164" height="52" rx="6" fill="none" stroke="currentColor" stroke-opacity="0.35"/>
    <text x="376" y="198" font-size="13">훅</text>
    <text x="376" y="216" font-size="11" fill-opacity="0.55" >이벤트마다</text>
    <rect x="8" y="276" width="544" height="50" rx="8" fill="none" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="4 4"/>
    <text x="20" y="297" font-size="12" font-weight="600">하네스 밖</text>
    <text x="20" y="315" font-size="11" fill-opacity="0.55">빌드 스크립트 · <tspan font-family="ui-monospace, monospace">npm prebuild</tspan> · 실행 주체: npm</text>
  </g>
</svg>
<figcaption>하네스 안에는 모델이 읽는 글과 하네스 설정이 함께 있습니다</figcaption>
</figure>

## 3번 어긴 규칙

블로그 글을 다듬는 에이전트에게 규칙을 하나 줬습니다.\
소제목을 명사형으로 쓰라는 규칙입니다.\
명사형은 문장을 서술어가 아니라 명사로 끝맺는 방식입니다.\
예를 들어 `규칙을 세 번 어겼습니다` 대신 `세 번 어긴 규칙`으로 씁니다.\
이 글에서는 이 규칙을 **명사형 규칙**이라고 부르겠습니다.\
에이전트 정의 파일에 예시 표까지 붙여서 적었습니다.

같은 날 규칙을 3번 어겼습니다.\
확인해봤지만 규칙은 정상적으로 파일 안에 있었습니다.

같은 저장소에는 검사가 2개 더 있습니다.\
기밀 단어 검사와 길이 검사입니다.\
이 두 검사는 어길 수 없습니다.\
빌드 직전에 자동으로 실행되기 때문에 **건너뛸 방법이 없습니다.**\
검사에 걸리면 빌드가 종료 코드 2로 멈추고 결과물도 갱신되지 않습니다.

규칙 3개 모두 내용은 명확했습니다.\
차이는 규칙을 둔 위치에서 생겼습니다.

## 하네스와 그 안의 장치

**하네스**는 모델을 감싸서 실행하는 프로그램입니다.\
Claude Code가 하네스이고, 모델은 하네스 안에서 호출되는 구성 요소입니다.\
하네스는 2가지 일을 합니다.\
모델이 읽을 글을 입력으로 넣어 주고, 모델이 요청한 도구 호출을 대신 실행합니다.

하네스 안의 장치도 이 2가지 일에 따라 나뉩니다.\
모델이 **읽는** 장치와 하네스가 **직접 실행하는** 장치입니다.

| 장치 | 정체 | 실행 주체 | 실리는 시점 |
|---|---|---|---|
| 인스트럭션 | `CLAUDE.md`·규칙 파일의 지시문 | 모델 | 세션 시작부터 |
| 메모리 | 지난 세션이 남긴 메모 | 모델 | 세션 시작부터 |
| 스킬 | 특정 작업의 절차 문서 | 모델 | 모델이 부를 때 |
| 서브에이전트 정의 | 하위 에이전트용 지시문 | 모델 | 그 에이전트를 띄울 때 |
| 권한 규칙 | 도구 호출의 허용·거부 목록 | 하네스 | 도구 호출마다 |
| 훅 | 이벤트에 걸어 둔 실행 설정 (기본은 셸 명령) | 하네스 | 이벤트마다 |

실행 주체가 모델인 장치는 이름은 다르지만 본질이 같습니다.\
**모두 모델이 읽는 글**입니다.\
글을 따를지는 모델이 판단하기 때문에 모델은 이 규칙을 건너뛸 수 있습니다.\
반면 실행 주체가 하네스인 장치는 모델의 판단과 관계없이 하네스가 실행합니다.

실행 주체가 모델인 장치 사이에도 강제력 차이가 있습니다.\
인스트럭션과 메모리는 세션 내내 입력에 포함됩니다.\
반면 스킬과 서브에이전트 정의는 **입력에 넣을지부터 모델이 판단합니다.**\
이 스킬이 지금 필요한지, 이 에이전트를 호출할지를 모델이 먼저 결정하기 때문입니다.

명사형 규칙은 서브에이전트 정의에 적혀 있었습니다.\
이 규칙이 지켜지려면 모델이 두 번 판단해야 합니다.\
먼저 이 에이전트를 부를지 판단하고, 부른 뒤에는 규칙을 따를지 판단합니다.\
그래서 강제력이 가장 약한 장치입니다.

훅은 트레이드오프가 존재합니다.\
발동 시점이 고정되어 예외를 둘 수 없습니다.\
형식 검사처럼 결과가 정해진 규칙은 훅으로 옮길 수 있습니다.\
반면 문장이 읽기 좋은지는 셸 명령으로 판정할 수 없습니다.\
그래서 이런 규칙은 지금까지 스킬이나 서브에이전트 정의 같은 문서에 남겨 왔습니다.

## 판단 기준은 하나

규칙을 어디에 둘지는 질문 하나로 정할 수 있습니다.\
"내가 잊어버려도 실행되어야 하는 규칙인가?"입니다.\
답이 '예'이면 훅에, '아니요'이면 스킬에 둡니다.\
[Claude Code 공식 문서](https://code.claude.com/docs/en/features-overview)도 같은 기준을 제시합니다.

<blockquote class="quote-tr">
<p class="quote-en">If a rule must hold every time, make it a hook rather than a prompt instruction.</p>
<details><summary><span class="to-ko">한국어로 보기</span><span class="to-en">원문 보기</span></summary><p>규칙이 매번 지켜져야 한다면 프롬프트 지시문이 아니라 훅으로 만드세요.</p></details>
</blockquote>

명사형 규칙은 이 질문에 '예'였습니다.\
그런데 강제력이 가장 약한 서브에이전트 정의에 있었습니다.\
그렇다고 셸 명령 훅으로 옮기기도 어렵습니다.\
소제목이 명사형인지는 문법을 따져야 판정할 수 있기 때문입니다.

결국 **훅에 둬야 하지만 셸 명령으로는 판정할 수 없는 규칙**이 남습니다.\
지금은 이런 규칙을 발행 전 확인 목록에 올려 두고 사람이 직접 확인합니다.\
그런데 이 글을 다듬는 동안에도 규칙 문서에 금지 예시로 적힌 문장이 초안에 그대로 들어갔습니다.\
사람의 확인도 결국 잊힐 수 있습니다.

Claude Code에는 이런 경우를 위한 훅도 있습니다.\
셸 명령 대신 모델에게 판정을 맡기는 [프롬프트 훅](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks)입니다.\
하지만 판정을 다시 모델에게 맡기면 규칙이 지켜진다고 할 수 있을까요?\
2부에서는 OpenAI·AWS·IBM의 문서와 문서팀의 사례를 따라 이런 규칙을 관리하는 방법을 정리합니다.

## 출처

- [Extend Claude Code](https://code.claude.com/docs/en/features-overview) — 기능별 강제력 비교, "If a rule must hold every time" 인용
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — `CLAUDE.md`·`.claude/rules/`·자동 메모리가 세션 시작에 실리는 방식
- [Extend Claude with skills](https://code.claude.com/docs/en/skills) — 스킬 설명과 본문이 실리는 시점
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents) — 서브에이전트 정의가 시스템 프롬프트가 되는 방식
- [Configure permissions](https://code.claude.com/docs/en/permissions) — 권한 규칙을 하네스가 판정하는 방식
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) — 훅 등록, 종료 코드 2 차단, 프롬프트 훅
- [npm scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts) — `pre` 스크립트가 자동으로 먼저 실행되는 규칙
