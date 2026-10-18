---
title: 실제 처리 흐름을 거치는 에러코드 테스트
date: 2026-10-16
category: Backend·System
kind: long
blurb: 테스트에 넣은 값이 실제 값과 같은 길을 지나야 합니다.
featured: false
tags: [testing, logging, pytest, contract]
series: 로그 마스킹과 에러코드
part: 3
---

[1부](/posts/masked-log-lost-error-code/)의 테스트는 마스킹 전 JSON 메시지를 파서에 직접 넣었습니다.\
실제 서버에서는 마스킹을 거친 메시지가 파서로 갔는데, 테스트는 그 단계를 건너뛰었습니다.\
그래서 13일 동안 테스트가 계속 통과했습니다.

이번 글에서는 [2부](/posts/error-code-as-field/)의 구조가 실제로 지켜지는지 확인하는 테스트를 짭니다.\
2부와 마찬가지로 설명용 예시이고, 코드는 Python 과 pytest 입니다.

## 하드코딩한 메시지와 실제 처리 흐름

테스트할 함수는 2부의 `handle_api_error` 입니다.\
응답 본문을 받아 에러코드를 읽고, 사람이 읽을 메시지를 만들고, 로그를 남깁니다.\
실제 서버가 거치는 단계가 이 함수 하나에 모여 있습니다.\
1부의 테스트는 이 단계를 건너뛰고 파서에 메시지를 바로 넣었습니다.

<figure>
<svg viewBox="0 0 560 200" role="img" aria-label="1부 테스트는 하드코딩한 메시지를 파서에 바로 넣었고, 3부 테스트는 응답 본문을 실제 처리 함수에 넣어 메시지와 로그를 함께 확인한다" style="width:100%;height:auto">
  <defs>
    <marker id="arr-p3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="8" y="18">1부 테스트</text>
    <text x="8" y="110">3부 테스트</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.3">
    <rect x="8" y="30" width="140" height="34" rx="6"/>
    <rect x="300" y="30" width="110" height="34" rx="6"/>
    <rect x="8" y="132" width="110" height="34" rx="6"/>
    <rect x="148" y="132" width="130" height="34" rx="6"/>
    <rect x="308" y="122" width="110" height="26" rx="6"/>
    <rect x="308" y="156" width="110" height="26" rx="6"/>
  </g>
  <g fill="currentColor" font-size="12" text-anchor="middle">
    <text x="78" y="51">하드코딩한 메시지</text>
    <text x="355" y="51">에러코드 파서</text>
    <text x="63" y="153">응답 본문</text>
    <text x="213" y="153">handle_api_error</text>
    <text x="363" y="139">ApiFailure</text>
    <text x="363" y="173">로그 레코드</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.5" marker-end="url(#arr-p3)">
    <path d="M150 47 H296"/>
    <path d="M120 149 H144"/>
    <path d="M280 145 L304 136"/>
    <path d="M280 153 L304 168"/>
  </g>
  <path d="M440 135 H470 M440 169 H470" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
  <path d="M470 135 V169" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
  <g fill="currentColor" fill-opacity="0.55" font-size="11">
    <text x="223" y="40" text-anchor="middle">마스킹 단계 건너뜀</text>
    <text x="478" y="156">둘 다 확인</text>
  </g>
</svg>
<figcaption>테스트 입력은 실제 입력과 같은 단계를 지나고 있을까요?</figcaption>
</figure>

아래 테스트는 메시지를 직접 만들지 않습니다.\
응답 본문을 `handle_api_error` 에 넣고, 돌아온 결과와 실제로 남은 로그를 확인합니다.\
테스트 값의 `401` 과 토큰은 설명용 가짜 값입니다.

```python
BODY = '{"code":401,"message":"...","token":"example-token-123"}'
```

## 메시지 형식과 에러코드

첫 번째 테스트는 메시지 형식이 달라져도 에러코드가 유지되는지 봅니다.

```python
def test_code_does_not_depend_on_message_format():
    plain = handle_api_error(BODY)
    custom = handle_api_error(
        BODY, format_message=lambda code: f"[외부 API] 실패 ({code})"
    )
    assert plain.message != custom.message
    assert plain.code == custom.code == 401
```

메시지 형식을 일부러 다르게 만들어 넣고, 두 결과의 에러코드가 같은지 확인합니다.\
누군가 나중에 메시지에서 에러코드를 다시 뽑도록 고치면, 두 메시지 어디에도 `"code":` 모양이 없어서 이 테스트가 실패합니다.\
1부의 의존 관계가 다시 생기는 수정을 잡는 테스트입니다.

## 나머지 두 테스트와 보장 범위

같은 방식으로 두 가지를 더 확인합니다.\
하나는 [caplog](https://docs.pytest.org/en/stable/how-to/logging.html) 로 실제로 남은 로그 레코드까지 보고, 메시지와 로그 어디에도 토큰이 없는지 확인합니다.\
다른 하나는 [parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html) 로 에러코드를 읽을 수 없는 응답 네 가지를 넣습니다.\
`code` 가 없는 경우, 문자열인 경우, JSON 이 아닌 경우, JSON 이지만 객체가 아닌 경우입니다.\
각 경우에 빈 값을 돌려주고 경고를 한 번만 남기는지 봅니다.

세 테스트가 지키는 것은 `handle_api_error` 한 경로입니다.

| 테스트 | 잡는 실수 | 보장하지 않는 것 |
|---|---|---|
| 메시지 형식 독립 | 에러코드를 다시 메시지에서 뽑는 수정 | 다른 코드가 `failure.message` 를 파싱하는지 여부 |
| 토큰 미노출 | 메시지·경고에 응답 원문을 다시 넣는 수정 | `token` 이 아닌 다른 이름의 자격증명 |
| 읽기 실패 동작 | 경고 없이 빈 값만 돌려주는 수정 | 목록에 넣지 않은 응답 형식 |

다른 코드가 `failure.message` 를 정규식으로 읽기 시작하면 첫 번째 테스트로는 알 수 없습니다.\
메시지 문구를 바꾸기 전에 `failure.message` 를 읽는 곳을 검색하는 일은 여전히 사람이 해야 합니다.

두 번째 테스트도 `example-token-123` 하나만 확인합니다.\
응답에 새 자격증명 필드가 생기면 `BODY` 에도 그 필드를 추가해야 합니다.\
가릴 필드 목록을 설정이나 DB 로 따로 관리한다면, `BODY` 를 그 목록으로 만들어 이 작업을 줄일 수 있습니다.

1부의 테스트는 하드코딩한 메시지를 파서에 넣었습니다.\
이 테스트들은 `BODY` 를 실제 처리 함수에 넣고, 사람이 읽는 메시지와 로그까지 거친 결과를 확인합니다.\
두 테스트의 차이는 입력이 실제 처리 단계를 거치는지 하나입니다.
