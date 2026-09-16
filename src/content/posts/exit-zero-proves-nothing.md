---
title: 에러가 없다고 문제가 없는 건 아니다
date: 2026-09-16
category: Develop
kind: note
blurb: 종료 코드 0은 아무것도 증명하지 않습니다.
featured: true
tags: [debugging, observability]
series: 빈 결과 읽기
part: 1
---

배치가 종료 코드 0으로 끝났고 에러 로그가 없습니다. 통과했다고 봐도 될까요.

아닙니다. 종료 코드 0과 빈 로그만으로는 2가지를 구분할 수 없습니다.

- 할 일을 다 하고 성공했다
- 조건이 잘못돼 전부 건너뛰었다

둘 다 로그가 비어 있고 종료 코드가 0입니다.

<figure>
<svg viewBox="0 0 560 262" role="img" aria-label="건수를 남기지 않으면 전부 처리한 실행과 아무것도 안 한 실행이 같은 신호로 합쳐지고, 건수를 남기면 둘이 갈라진다" style="width:100%;height:auto">
  <defs>
    <marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="8" y="14">건수 없음</text>
    <text x="8" y="146">건수 있음</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.25">
    <rect x="8" y="24" width="150" height="40" rx="6"/>
    <rect x="8" y="72" width="150" height="40" rx="6"/>
    <rect x="250" y="48" width="180" height="40" rx="6"/>
    <rect x="8" y="156" width="150" height="40" rx="6"/>
    <rect x="8" y="204" width="150" height="40" rx="6"/>
    <rect x="250" y="156" width="180" height="40" rx="6"/>
    <rect x="250" y="204" width="180" height="40" rx="6"/>
  </g>
  <g fill="currentColor" font-size="13">
    <text x="22" y="49">전부 처리</text>
    <text x="22" y="97">전부 건너뜀</text>
    <text x="264" y="73">exit 0 · 로그 없음</text>
    <text x="22" y="181">전부 처리</text>
    <text x="22" y="229">전부 건너뜀</text>
    <text x="264" y="181">처리 500 · 건너뜀 0</text>
    <text x="264" y="229">처리 0 · 건너뜀 500</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.55" marker-end="url(#tip)">
    <path d="M166 44 H206 V68 H244"/>
    <path d="M166 92 H206 V68 H244"/>
    <path d="M166 176 H244"/>
    <path d="M166 224 H244"/>
  </g>
  <g fill="currentColor" fill-opacity="0.45" font-size="12">
    <text x="440" y="72">같은 신호</text>
    <text x="440" y="204">다른 신호</text>
  </g>
</svg>
<figcaption>건수 하나가 두 실행을 갈라놓습니다</figcaption>
</figure>

## 건수로 남기기

"처리했다"가 아니라 "몇 건 처리했다"를 남깁니다. 0건이면 그게 정상인지 아닌지를 판단할 수 있습니다.

대상이 0건이어도 정상인 날은 많습니다. 그래도 **0건이 며칠째 이어지는지**는 봐야 합니다. 어제도 0건, 오늘도 0건이면 대상을 고르는 조건이 잘못됐을 가능성이 큽니다.

## 조용한 건너뜀

실패하면 알림이 옵니다. 크래시가 나면 스택 트레이스가 남습니다. 하지만 조건에 맞지 않아 건너뛴 작업은 성공으로 분류됩니다. 종료 코드는 0이고 알림도 없습니다.

며칠 뒤 데이터가 비어 있는 걸 사람이 발견합니다. 그때는 어느 날부터 비었는지 되짚어야 합니다.

건너뜀도 집계합니다. 처리·건너뜀·실패 건수를 모두 남기면, 건너뜀 수가 갑자기 늘어난 날을 찾을 수 있습니다.

## 성공으로 위장한 실패

겪은 일입니다. 한 작업이 응답에 상태값을 넣지 않았습니다. 상태값이 빈 문자열이면 실패 목록에 들어가지 않았고, 집계는 그 실행을 성공으로 셌습니다. 실패 건이 집계에서 빠진 게 아닙니다. **성공 건으로 집계됐습니다.**

2주치 실행 로그 76건의 상태값은 모두 빈 문자열이었습니다. 그동안 실패율은 0%로 보였습니다. 알림은 한 번도 안 왔습니다.

건수를 남겨도 끝이 아닙니다. 0건이 진짜 0건인지는 아직 모릅니다.
