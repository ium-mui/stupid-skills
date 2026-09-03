# 기여 가이드

[English](CONTRIBUTING.md)

새로운 스킬을 추가할 때는 사람들이 쉽게 검색하고 설치하며 이해할 수 있어야 합니다.

## 이름 규칙

- 언어 변형을 `skills/<behavior>/` 아래에 모읍니다.
- 언어별 동작에는 `stupid-<behavior>-<locale>` 형식을 사용합니다.
- 언어 중립 동작에는 `stupid-<behavior>` 형식을 사용합니다.
- 영문 소문자, 숫자와 한 개의 하이픈만 사용합니다.
- 이름은 64자 미만이어야 합니다.
- 폴더 이름과 frontmatter의 `name`을 동일하게 유지합니다.
- `config/repository.json`에 등록된 언어만 사용합니다.

예시:

```text
skills/kkwettu/stupid-kkwettu-en-us/SKILL.md
skills/kkwettu/stupid-kkwettu-ko/SKILL.md
skills/random-footnote/stupid-random-footnote-en-us/SKILL.md
skills/shrug/stupid-shrug/SKILL.md
```

모든 패밀리에는 공통 동작과 전체 변형을 설명하는 영문 `README.md`와 한국어 `README.ko.md`가 있어야 합니다. 패밀리 폴더에는 `SKILL.md`나 두 README 이외의 파일을 두지 않습니다. 내부의 `stupid-*` 폴더가 실제 설치 단위이며 패밀리 밖으로 복사해도 완전한 스킬이어야 합니다.

## 언어 규칙

언어 변형은 각각 독립된 스킬입니다. 입력 언어와 관계없이 선언된 언어의 동작을 사용해야 하며, 다른 언어로 자동 전환하면 안 됩니다.

동작과 출력이 언어에 영향을 받지 않을 때만 언어 중립 스킬을 사용합니다. 언어 중립 스킬도 패밀리와 영문·한국어 패밀리 README가 필요합니다.

두 변형의 차이가 출력 번역뿐이어도 별도로 설치할 수 있는 스킬로 제공합니다. 말투, 형식 또는 장난의 동작도 다르다면 각 `SKILL.md`에 차이를 직접 작성합니다.

영어가 기본 문서 언어입니다. 공개 저장소 문서를 변경할 때는 같은 Pull Request에서 해당 `.ko.md` 번역도 함께 수정합니다.

## 스킬 생성

다음 명령을 실행합니다.

```sh
make new-skill
```

생성기는 필요할 때 두 패밀리 README를 만들고 변형 목록을 갱신하며, 지원하지 않는 언어, 잘못된 이름과 이미 존재하는 대상 폴더를 거부합니다. 생성 후에는 다음 작업을 수행합니다.

1. 생성된 `SKILL.md`를 검토하고 동작을 명확하게 작성합니다.
2. frontmatter 설명은 짧고 다른 스킬과 구분되게 작성합니다.
3. 현실적인 입력·출력 예시를 하나 이상 유지합니다.
4. `README.md`와 `README.ko.md`의 스킬 목록을 수정합니다.
5. `make check`를 실행합니다.

## 언어 추가

`config/repository.json`의 `supported_locales`에 소문자 로케일 식별자를 추가하고, 두 README와 기여 가이드를 수정한 다음 해당 언어를 사용하는 실제 스킬 또는 하네스 테스트를 하나 이상 추가합니다.

지역별 동작이 중요하지 않으면 `ko` 같은 언어 코드를 사용합니다. 지역 구분이 필요하면 `en-us` 같은 지역 코드를 사용합니다.

## Pull Request 확인 목록

- 스킬에 고유한 `stupid-` 이름이 있습니다.
- 패밀리에 내용이 동기화된 영문·한국어 README가 있습니다.
- 폴더에 필수 `SKILL.md`가 있습니다.
- 언어별 스킬은 선언된 언어가 고정되어 자동으로 변경되지 않습니다.
- 영어와 한국어 공개 문서가 함께 유지됩니다.
- `make check`가 통과합니다.
