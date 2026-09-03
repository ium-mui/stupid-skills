# stupid-skills

[English](README.md)

쓸모없고 진지하지 않으며 이상하게 즐거운 AI 스킬을 쉽게 검색할 수 있도록 모아 둔 저장소입니다.

설치 가능한 모든 스킬 이름은 `stupid-`로 시작하며 `skills/<behavior>/` 아래의 문서화된 동작 패밀리에 속합니다. 언어별 동작은 각각 독립된 스킬로 제공하고, 언어 중립 동작은 로케일 접미사가 없는 스킬로 제공합니다. 영어 문서를 원본으로 관리하고 한국어 번역 문서를 함께 유지합니다.

## 제공 스킬

| 스킬 | 언어 | 동작 |
| --- | --- | --- |
| [`stupid-kkwettu-en-us`](skills/kkwettu/stupid-kkwettu-en-us) | 영어(미국) | 일반 문장을 `kkwettu`로 바꿉니다 |
| [`stupid-kkwettu-ko`](skills/kkwettu/stupid-kkwettu-ko) | 한국어 | 일반 문장을 `꿰뚜`로 바꿉니다 |

## 설치 및 사용

저장소를 복제한 다음 원하는 언어 변형을 Codex 스킬 디렉터리로 복사합니다.

```sh
git clone https://github.com/ium-mui/stupid-skills.git
cd stupid-skills
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/kkwettu/stupid-kkwettu-ko "${CODEX_HOME:-$HOME/.codex}/skills/"
```

필요하다면 Codex를 다시 시작하거나 스킬 목록을 새로 고친 후 `$stupid-kkwettu-ko`처럼 설치한 스킬 이름으로 호출합니다.

같은 동작의 언어 변형은 한 번에 하나만 설치하는 것을 권장합니다. 각 변형은 언어를 자동으로 감지하거나 다른 언어로 전환하지 않습니다.

## 새 스킬 추가

대화형 생성기를 실행합니다.

```sh
make new-skill
```

생성기가 동작 이름, 언어 또는 언어 중립 모드, 설명, 지침과 예시를 질문합니다. 패밀리를 처음 생성할 때는 영문·한국어 패밀리 설명도 함께 입력받은 후 다음 구조를 만듭니다.

```text
skills/<behavior>/
├── README.md
├── README.ko.md
└── stupid-<behavior>[-<locale>]/
    └── SKILL.md
```

생성기는 두 패밀리 README의 변형 목록을 자동으로 갱신합니다. 생성된 파일을 검토하고 최상위 영어·한국어 README 목록에 스킬을 추가한 다음 아래 명령을 실행합니다.

```sh
make check
```

이 명령은 모든 스킬을 검증하고 하네스 테스트를 실행합니다. Pull Request와 `main` 브랜치 push에서도 GitHub Actions가 같은 검사를 실행합니다.

## 지원 언어

| 로케일 | 언어 | 기본값 |
| --- | --- | --- |
| `en-us` | 영어(미국) | 예 |
| `ko` | 한국어 | 아니요 |

지원 언어와 `stupid` 접두사는 [`config/repository.json`](config/repository.json)에서 관리합니다.

언어 중립 스킬은 `stupid-shrug`처럼 로케일 접미사를 사용하지 않지만 `skills/shrug/` 안에서 두 패밀리 README와 함께 관리합니다.

## 저장소 구조

```text
stupid-skills/
├── skills/
│   └── kkwettu/             동작 패밀리이며 직접 설치하지 않음
│       ├── README.md         영문 패밀리 설명
│       ├── README.ko.md      한국어 패밀리 설명
│       ├── stupid-kkwettu-en-us/
│       │   └── SKILL.md     설치 가능한 영어 변형
│       └── stupid-kkwettu-ko/
│           └── SKILL.md     설치 가능한 한국어 변형
├── scripts/                 생성기와 검증 하네스
├── templates/               새 스킬 템플릿
├── tests/                   하네스 테스트
├── config/repository.json   접두사와 지원 언어 설정
├── AGENTS.md                코딩 에이전트용 저장소 규칙
├── CONTRIBUTING.md          기여 가이드
└── README.ko.md             한국어 README
```

## 문서

- [기여 가이드](CONTRIBUTING.ko.md) · [English](CONTRIBUTING.md)
- [에이전트 규칙](AGENTS.ko.md) · [English](AGENTS.md)

## 주의사항

이 스킬들은 장난과 실험을 위한 것입니다. 중요한 의사결정, 실제 업무 또는 정확한 의사소통이 필요한 작업에는 사용하지 마세요. 장난용 스킬은 안전, 정확성 또는 사용자의 명시적 요청보다 우선하지 않습니다.

## 라이선스

MIT
