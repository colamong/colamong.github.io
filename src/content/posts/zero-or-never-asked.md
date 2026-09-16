---
title: 0건인가, 못 물어본 건가
date: 2026-09-16
category: Develop
kind: long
blurb: 조회가 실패해도 결과는 0건으로 보입니다.
featured: false
tags: [debugging, observability]
series: 빈 결과 읽기
part: 2
---

[에러가 없다고 문제가 없는 건 아니다](/posts/exit-zero-proves-nothing/)에서 건수를 남기라고 썼습니다. 하지만 건수를 남겨도 0건이 뜻하는 경우는 여전히 2가지입니다.

- 물어봤고, 답이 없었다
- 못 물어봤다

첫째는 정상이고, 둘째는 실패입니다. 하지만 결과는 모두 0건으로 보입니다.

## 가짜 0건

조회 함수가 예외를 잡아 빈 목록을 반환하면, 호출하는 쪽은 "조회는 됐고 대상이 없다"고 해석합니다. 안내 문구를 함께 보내도 판단은 달라지지 않습니다. 문구는 사람이 읽을 설명일 뿐, 기계가 집계할 값이 아닙니다.

<figure>
<svg viewBox="0 0 560 182" role="img" aria-label="끝까지 간 조회와 중간에 끊긴 조회가 똑같이 0건으로 표시된다" style="width:100%;height:auto">
  <defs>
    <marker id="tip2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="8" y="20">조회 완료</text>
    <text x="8" y="110">조회 중단</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.25">
    <rect x="8" y="30" width="80" height="34" rx="6"/>
    <rect x="104" y="30" width="80" height="34" rx="6"/>
    <rect x="200" y="30" width="80" height="34" rx="6"/>
    <rect x="320" y="30" width="90" height="34" rx="6"/>
    <rect x="8" y="120" width="80" height="34" rx="6"/>
    <rect x="320" y="120" width="90" height="34" rx="6"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.2" stroke-dasharray="4 4">
    <rect x="104" y="120" width="80" height="34" rx="6"/>
    <rect x="200" y="120" width="80" height="34" rx="6"/>
  </g>
  <g fill="currentColor" font-size="13">
    <text x="30" y="52">질의</text>
    <text x="126" y="52">수신</text>
    <text x="222" y="52">집계</text>
    <text x="350" y="52">0건</text>
    <text x="30" y="142">질의</text>
    <text x="350" y="142">0건</text>
  </g>
  <g fill="currentColor" fill-opacity="0.3" font-size="13">
    <text x="126" y="142">수신</text>
    <text x="222" y="142">집계</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.55" marker-end="url(#tip2)">
    <path d="M88 47 H100"/>
    <path d="M184 47 H196"/>
    <path d="M280 47 H316"/>
  </g>
  <path d="M48 154 V172 H365 V158" fill="none" stroke="currentColor" stroke-opacity="0.4" stroke-dasharray="4 4" marker-end="url(#tip2)"/>
  <text x="96" y="142" text-anchor="middle" fill="currentColor" fill-opacity="0.55" font-size="14">✕</text>
  <g fill="currentColor" fill-opacity="0.45" font-size="12">
    <text x="424" y="52">정상</text>
    <text x="424" y="142">실패</text>
  </g>
</svg>
<figcaption>같은 0건이지만 하나는 답이고 하나는 사고입니다</figcaption>
</figure>

판단 기준은 하나입니다. **조회가 끝까지 완료됐는지입니다.** 끝까지 완료됐는데 결과가 비었으면 0건입니다. 중간에 끊긴 결과는 0건이 아니라 실패입니다.

## 부분 성공

60만 행을 요청했는데 앞의 501행만 받은 뒤 전송이 끊긴 적이 있습니다. 기존 `except` 가 예외를 삼켰고, 시스템은 "총 행 수: 501"을 그대로 보냈습니다. 받는 사람은 501행이 전체 결과라고 믿습니다.

부분 성공은 0건보다 나쁩니다. 0건은 이상하다는 느낌을 주지만, 501행이라는 숫자는 그럴듯해 보입니다.

## 실패 표시는 한 곳에

실패 표시는 어디에 남겨야 할까요. 반환 지점마다 남기면 지점 수만큼 손이 갑니다. 지점이 늘어날수록 누락 가능성도 높아집니다.

이 방식은 규칙을 아는 사람에게만 통합니다. 새로 합류한 사람은 규칙을 모른 채 반환 지점을 하나 더 만들 것입니다. 그래서 모든 호출이 공통으로 지나는 지점을 찾아 거기에만 남깁니다. 그 지점을 우회하는 코드는 테스트로 막아야 합니다.

## 지표를 믿기 전 점검 사항

남긴 건수도 믿을 수 없습니다. 집계 방식이 틀리면 지표가 현실과 어긋납니다.

| 점검 | 점검 내용 |
|---|---|
| 분모 | 성공률의 분모가 시도 전체인지, 거기까지 도달한 것만인지 |
| 기본값 | 상태가 빈 값일 때 성공과 실패 중 어느 쪽으로 분류되는지 |
| 알림 | 실패가 사람에게 닿는지, 로그에만 남는지 |
| 근거 | 지표가 초록인 이유가 어느 검사 덕인지 |

마지막 점검이 제일 어렵습니다. 오판율 0%가 제 설계 덕이라고 생각했습니다. 나중에 보니 다른 목적으로 넣은 검사가 오판 4건을 막고 있었습니다.

초록인 근거를 설명하지 못하면, 그 지표를 믿을 수 없습니다.
