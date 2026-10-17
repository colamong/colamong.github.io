---
title: 메시지 형식에 기대지 않는 에러코드 전달
date: 2026-10-16
category: Backend·System
kind: long
blurb: 사람이 읽는 문구는 코드의 입력이 아니어야 합니다.
featured: false
tags: [logging, parsing, design, contract]
series: 로그 마스킹과 에러코드
part: 2
---

[1부](/posts/masked-log-lost-error-code/)에서는 로그의 자격증명을 가리다가 에러코드 파싱이 깨진 일을 다뤘습니다.\
에러코드 파서가 응답 본문이 아니라 사람이 읽는 메시지를 읽고 있었습니다.\
이번 글에서는 같은 실수가 구조상 생기지 않게 하려면 무엇을 바꿔야 하는지 살펴봅니다.

아직 실제 서비스에 적용한 개선책은 아닙니다.\
검토 중인 설계를 설명하는 예시이고, 코드는 설명용 Python 입니다.

## 검토한 세 가지 방향

고치는 방향은 여러 가지를 생각할 수 있습니다.

| 방향 | 방법 | 남는 문제 |
|---|---|---|
| 파서 확장 | 파서가 `code=401` 모양도 읽도록 정규식 추가 | 다음에 문구가 바뀌면 다시 깨짐 |
| 필드 단위 마스킹 | 메시지를 JSON 그대로 두고 `token` 값만 가림 | 메시지 형식을 바꾸는 다른 수정에는 그대로 깨짐 |
| 에러코드 필드 분리 | 응답 본문에서 에러코드를 따로 읽어 필드로 전달 | 응답 본문 형식에는 여전히 의존 |

앞의 두 방향은 이번 수정만 놓고 보면 문제를 해결합니다.\
파서를 넓히면 `code=401` 도 읽을 수 있고, 필드만 가리면 `"code":401` 이 그대로 남으니까요.\
그런데 둘 다 에러코드를 메시지에서 읽는 구조는 그대로 둡니다.\
메시지 문구를 다시 고치는 날, 같은 일이 생길 수 있습니다.

그래서 이 글에서는 세 번째 방향을 자세히 살펴봅니다.

## 에러코드를 별도 필드로 전달하는 구조

아래 예시는 에러코드를 응답 본문에서 한 번 읽어 필드로 넘깁니다.\
사람이 읽을 메시지는 그 필드로 따로 만듭니다.

```python
@dataclass
class ApiFailure:
    code: int | None  # 코드가 읽는 값
    message: str      # 사람이 읽는 값

def handle_api_error(body: str, format_message=format_message) -> ApiFailure:
    code = read_code(body)
    if code is None:
        logger.warning("에러코드를 읽을 수 없음: 응답 형식이 예상과 다름")
    failure = ApiFailure(code=code, message=format_message(code))
    logger.error(failure.message)
    return failure
```

`read_code` 는 응답 본문을 JSON 으로 읽어 정수 `code` 만 돌려주고, 그 밖의 경우에는 빈 값을 돌려줍니다.\
에러코드가 필요한 코드는 이제 `failure.code` 를 읽습니다.\
사람은 `failure.message` 를 읽습니다.

<figure>
<svg viewBox="0 0 560 230" role="img" aria-label="1부 구조에서는 응답 본문이 마스킹과 메시지를 거쳐 파서로 가고, 바꾼 구조에서는 응답 본문에서 에러코드 필드와 메시지가 따로 갈라진다" style="width:100%;height:auto">
  <defs>
    <marker id="arr-p2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0 0L10 5L0 10z" fill="currentColor" fill-opacity="0.55"/>
    </marker>
  </defs>
  <g fill="currentColor" font-size="12" font-weight="600">
    <text x="8" y="18">1부 구조</text>
    <text x="8" y="128">바꾼 구조</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.3">
    <rect x="8" y="30" width="90" height="34" rx="6"/>
    <rect x="128" y="30" width="80" height="34" rx="6"/>
    <rect x="238" y="30" width="80" height="34" rx="6"/>
    <rect x="348" y="30" width="96" height="34" rx="6"/>
    <rect x="8" y="160" width="90" height="34" rx="6"/>
    <rect x="128" y="140" width="96" height="34" rx="6"/>
    <rect x="128" y="186" width="96" height="34" rx="6"/>
    <rect x="254" y="140" width="96" height="34" rx="6"/>
    <rect x="254" y="186" width="96" height="34" rx="6"/>
  </g>
  <g fill="currentColor" font-size="12" text-anchor="middle">
    <text x="53" y="51">응답 본문</text>
    <text x="168" y="51">마스킹</text>
    <text x="278" y="51">메시지</text>
    <text x="396" y="51">에러코드 파서</text>
    <text x="53" y="181">응답 본문</text>
    <text x="176" y="161">read_code</text>
    <text x="176" y="207">format_message</text>
    <text x="302" y="161">code 필드</text>
    <text x="302" y="207">메시지</text>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity="0.5" marker-end="url(#arr-p2)">
    <path d="M100 47 H124"/>
    <path d="M210 47 H234"/>
    <path d="M320 47 H344"/>
    <path d="M100 172 L124 157"/>
    <path d="M226 157 H250"/>
    <path d="M302 176 V182"/>
    <path d="M226 203 H250"/>
  </g>
  <g fill="currentColor" fill-opacity="0.55" font-size="11">
    <text x="396" y="84" text-anchor="middle">메시지 모양에 의존</text>
    <text x="360" y="161">에러코드를 쓰는 코드</text>
    <text x="360" y="207">사람</text>
  </g>
</svg>
<figcaption>에러코드를 쓰는 코드는 각 구조에서 무엇을 읽고 있을까요?</figcaption>
</figure>

이 구조에서 메시지 문구를 바꾸면 `format_message` 만 바뀝니다.\
`read_code` 는 메시지가 아니라 응답 본문을 읽으니까요.\
마스킹 방식이 바뀌어도 마찬가지입니다.\
메시지에 응답 본문을 아예 넣지 않기 때문에, 메시지 쪽에는 가릴 토큰이 처음부터 들어가지 않습니다.

그래도 `read_code` 역시 응답 본문의 형식에 기대고 있다고 볼 수 있습니다.\
맞습니다.\
다만 응답 본문의 형식은 외부 API 와 맞춘 약속입니다.\
반면 사람용 메시지는 우리 코드 안에서 언제든 고칠 수 있는 문구입니다.\
자주 바뀌는 문구 대신, 쉽게 바뀌지 않는 약속에 기대도록 옮긴 겁니다.

HTTP API 에러 응답 표준인 [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457#section-3.1.4)도 같은 기준을 둡니다.

<blockquote class="quote-tr">
<label title="눌러서 번역 보기"><input type="checkbox"><span class="quote-en">Consumers SHOULD NOT parse the "detail" member for information; extensions are more suitable and less error-prone ways to obtain such information.</span><span class="quote-ko">사용하는 쪽은 정보를 얻으려고 "detail" 필드를 파싱하면 안 됩니다. 확장 필드가 더 알맞고 오류도 적은 방법입니다.</span></label>
</blockquote>

그 약속이 깨지는 경우, 즉 응답에서 `code` 를 읽을 수 없을 때의 동작은 따로 정해 두어야 합니다.

## 에러코드를 읽을 수 없는 경우

1부의 파서는 이런 경우 빈 값만 돌려주고 끝났습니다.\
그래서 13일 동안 아무도 알아채지 못했습니다.

| 선택지 | 결과 | 어울리는 상황 |
|---|---|---|
| 빈 값 반환 | 실패를 알 수 없음 | 에러코드가 없어도 되는 기능 |
| 빈 값 반환 + 경고 | 처리는 이어지고, 실패는 로그로 확인 | 원래 에러 보고를 막으면 안 될 때 |
| 예외 | 처리가 멈춤 | 에러코드 없이 진행하면 잘못된 결과가 나올 때 |

어느 쪽이 맞는지는 시스템의 요구에 따라 다릅니다.\
이 예시에서는 빈 값 반환과 경고를 고릅니다.\
`handle_api_error` 는 이미 실패한 API 호출을 보고하는 중입니다.\
여기서 예외를 던지면 에러코드를 읽을 수 없다는 이유로 원래 실패 보고까지 사라집니다.

경고 문구에는 응답 원문을 넣지 않고, 형식이 예상과 다르다는 사실만 남깁니다.\
경고에 원문을 붙이면 마스킹으로 가린 토큰이 경고 로그에 다시 남기 때문입니다.

## 경고와 구조 변경의 차이

1부 구조에 이 경고만 더했다면, 마스킹 수정 직후부터 경고가 찍혀 13일씩 걸리지는 않았을 겁니다.\
그래도 파싱은 깨진 채로 남고, 누군가 경고를 보고 파서를 고쳐야 합니다.\
경고는 실패를 빨리 알려 줄 뿐입니다.

반면 구조를 바꾸면 메시지를 고치는 수정으로는 파싱이 깨지지 않습니다.\
응답 형식이 바뀌는 경우는 여전히 남기 때문에 이 예시에서는 둘 다 둡니다.

이 동작들이 실제로 지켜지는지 확인하는 테스트는 3부에서 이어집니다.
