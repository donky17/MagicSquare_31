# MagicSquare_xx

4×4 마방진(Magic Square)을 다루는 프로그램 과제입니다.  
QA 엔지니어 관점에서 **문제 정의·검증 가능한 요구**를 먼저 고정하고, 이후 구현·테스트로 확장하는 것을 목표로 합니다.

> **현재 단계:** 문제 정의(STEP 1~5) + Dual-Track · Clean Architecture **설계서** 완료 — **구현·실행 코드 없음**

---

## PRD (구현 전 제품 요구 문서)

- PRD 문서: [Report/06.PRD_MagicSquare_xx.md](./Report/06.PRD_MagicSquare_xx.md)
- PRD가 고정하는 것:
  - **Vision / Goals / Non-goals**
  - **MVP 범위(2빈칸 입력 → 결과 또는 오류)**
  - **Input / Output / Error Contract**
  - **Invariants(P/I/O/M)와 Dual-Track 검증 전략**
  - **Quality bar(결정성/회귀/커버리지/금지 패턴 요약)**

---

## 프로젝트 요약

| 항목 | 내용 |
|------|------|
| 도메인 | 4×4 격자, 1~16을 각각 한 번씩 배치 |
| 핵심 규칙 | 행·열·대각선 합이 모두 동일 (매직 상수 34) |
| 접근 | TDD·명세·불변조건·오라클 설계를 전제로 한 문제 정의 |
| 1차 목표 | **마방진인지 판단하는 기준**을 신뢰·테스트·회귀 가능하게 만드는 것 |
| 2차 목표 (확장) | 판정이 안정된 뒤, 규칙을 만족하는 유효 배치 **산출** |
| 설계 (현재) | 2빈칸 완성, Logic / UI Boundary / Data 레이어, Dual-Track TDD |

---

## 설계 요약 (02.Report)

2빈칸 퍼즐 유스케이스 기준 **입·출력 계약** (구현 전):

| 항목 | 계약 |
|------|------|
| 입력 | `int[4][4]`, `0`=빈칸 **2개**, 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]` (좌표 **1-index**) |
| 레이어 | Domain(판정·해결) → Screen Boundary → Data(Repository) |

상세: [Report/02.DualTrack_CleanArchitecture_Design_Report.md](./Report/02.DualTrack_CleanArchitecture_Design_Report.md)

---

## 진짜 문제 정의 (STEP 5)

### 표면 정의 (피해야 할 정의)

> 「4×4 마방진을 완성하는 프로그램을 만든다.」

단일 정답·생성·UI까지 범위가 넓어지고, QA·검증이 부수적으로 밀리기 쉽습니다.

### 개선된 정의 (본 프로젝트의 문제)

> **4×4 격자와 1~16 배치에 대해, 마방진으로서의 유효성(값 집합·행·열·대각선 합 일치)을 명시된 규칙으로 판정하고, 그 판정을 반복 가능하게 검증할 수 있도록 요구를 고정·테스트·회귀 가능한 형태로 다루는 과제이다. 유효 배치 산출은 판정이 안정된 이후의 확장 범위로 둔다.**

**한 줄:** 만들기보다 **「마방진인가?」에 대한 판단 기준**이 중심입니다.

---

## 핵심 불변 조건 (Invariant)

완전히 채워진 4×4 배치를 기준으로 합니다.

| ID | 내용 |
|----|------|
| I-1 | 4행 4열, 16칸 |
| I-2 | 각 칸은 1~16의 정수 |
| I-3 | 1~16이 각각 정확히 한 번 (중복·누락 없음) |
| I-4 ~ I-7 | 행 4·열 4·대각 2의 합이 모두 동일 (34) |
| M-1 ~ M-3 | 동일 배치 → 동일 판정, 배치 내용만 의존, 유효성은 I-1~I-7에만 근거 |

**의도적으로 1차 Invariant에 넣지 않는 것:** 특정 한 장의 격자와의 일치, 회전·반사 동형 처리, 구성 방법.

---

## Why 요약 (문제 정의 근거)

| 단계 | 질문 | 핵심 결론 |
|------|------|-----------|
| STEP 1 | 무엇을 관찰하는가? | 규칙 있는 작은 도메인을 프로그램 요구로 옮기기 **전** 단계 |
| STEP 2 | 왜 완성? | 검증·시연용 샘플이 필요할 수 있으나, **완성은 수단·검증이 목적**에 가깝다 |
| STEP 3 | 왜 프로그램? | 반복 가능성, 검증 자동화, 오류 방지, 규칙 명세화 |
| STEP 4 | 왜 TDD? | **규칙 통과** 통제, 불변 고정, 명확한 입·출력, 검증 우선 |
| STEP 5 | 진짜 문제는? | 판단 기준을 신뢰·테스트·회귀 가능하게 만드는 것 |

---

## 범위 (In / Out)

### In scope (1차)

- 완전히 채워진 4×4 배치에 대한 **유효성 판정** 규칙
- 규칙의 명시, 테스트, 회귀
- 유효 / 무효 및 대표적 위반 유형에 대한 **판단 일관성**

### Out of scope (1차 목표 아님)

- 특정 한 장만을 「정답」으로 하는 기대
- 사용자 퍼즐·힌트·난이도
- 모든 유효 배치 나열·개수
- 구성 방식·성능·최적화

---

## 훈련하려는 사고 능력

- 명세 분해 · 오라클 설계 · 불변조건 우선
- 범위·우선순위 통제 (판정 1차, 산출 2차)
- 테스트 주도적 요구 고정 · 실패 모드 분류
- 다해·동형에 대한 계약 사고 (유일 출력에 묶지 않기)

---

## 저장소 구조

```
MagicSquare_xx/
├── README.md                                                    ← 이 파일
├── src/                                                         ← 애플리케이션 소스 (boundary, entity)
├── docs/                                                        ← test_plan.md, defect_list.md
├── Report/
│   ├── 01.ProblemDefinition_Report.md                           ← STEP 1~5 문제 정의
│   ├── 02.DualTrack_CleanArchitecture_Design_Report.md          ← Dual-Track · CA 설계
│   └── 07.AC_FR_01_01_RED_Testing_and_QA_Report.md              ← AC-FR-01-01 RED·QA 보고서
├── Prompt/
│   ├── 02.DualTrack_CleanArchitecture_Design-Prompt.md           ← 설계 단계 대화 transcript
│   └── 07.AC_FR_01_01_RED_Testing-Prompt.md                     ← RED 테스트 단계 transcript
└── Prompting/
    └── 01.ProblemDefinition_Report-Prompt.md                    ← 문제 정의 대화 transcript
```

| 경로 | 설명 |
|------|------|
| [Report/01.ProblemDefinition_Report.md](./Report/01.ProblemDefinition_Report.md) | 관찰, Why #1~#3, 진짜 문제 정의, Invariant, 부록 전체 |
| [Report/02.DualTrack_CleanArchitecture_Design_Report.md](./Report/02.DualTrack_CleanArchitecture_Design_Report.md) | Logic / UI Boundary / Data 설계, 테스트·통합·Traceability |
| [Report/06.PRD_MagicSquare_xx.md](./Report/06.PRD_MagicSquare_xx.md) | 구현 전 PRD(비전/범위/계약/불변식/검증/품질바) |
| [Report/07.AC_FR_01_01_RED_Testing_and_QA_Report.md](./Report/07.AC_FR_01_01_RED_Testing_and_QA_Report.md) | AC-FR-01-01 RED 테스트·QA·결함·환경 정비 보고서 |
| [docs/test_plan.md](./docs/test_plan.md) | AC-FR-01-01 테스트 계획서 |
| [docs/defect_list.md](./docs/defect_list.md) | RED 단계 결함 목록 |
| [Prompt/02.DualTrack_CleanArchitecture_Design-Prompt.md](./Prompt/02.DualTrack_CleanArchitecture_Design-Prompt.md) | Dual-Track 설계 단계 User/Cursor 프롬프트 export |
| [Prompt/07.AC_FR_01_01_RED_Testing-Prompt.md](./Prompt/07.AC_FR_01_01_RED_Testing-Prompt.md) | AC-FR-01-01 RED 테스트 단계 transcript |
| [Prompting/01.ProblemDefinition_Report-Prompt.md](./Prompt/01.ProblemDefinition_Report-Prompt.md) | 문제 정의 단계 User/Cursor 프롬프트 export |

---

## 다음 단계 (제안)

1. [02 설계서](./Report/02.DualTrack_CleanArchitecture_Design_Report.md) 기준 **Domain RED** (D-T07~D-T09)부터 구현·테스트
2. UI Boundary Contract 테스트 (U-T01~, Domain Mock)
3. Data `MatrixRepository` InMemory → (선택) File JSON
4. 통합 시나리오 IT-01~IT-06, 커버리지 목표( Domain 95%+ / UI 85%+ / Data 80%+ )
5. 미결정 Q-1~Q-3 (Application 레이어, 응답 래핑, 파일 포맷) 확정

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록 ([docs/defect_list.md](./docs/defect_list.md))
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 문서 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-28 | STEP 1~5 문제 정의 완료, `Report/01.ProblemDefinition_Report.md` 작성 |
| 2026-05-28 | Dual-Track · Clean Architecture 설계, `Report/02...`, `Prompt/02...` 작성 |
| 2026-05-28 | 구현 전 PRD 초안 작성, `Report/06.PRD_MagicSquare_xx.md` 작성 |
| 2026-05-29 | AC-FR-01-01 RED 결함 목록, `docs/defect_list.md` 작성 |
| 2026-05-29 | AC-FR-01-01 RED·QA 보고서·transcript, `Report/07...`, `Prompt/07...` 작성 |

---

## 참고

- 문제 정의: [01.ProblemDefinition_Report.md](./Report/01.ProblemDefinition_Report.md)
- 아키텍처·TDD 설계: [02.DualTrack_CleanArchitecture_Design_Report.md](./Report/02.DualTrack_CleanArchitecture_Design_Report.md)
- 저장소에는 **실행 코드·알고리즘 구현**이 없으며, Report는 설계·계약·테스트 계획 수준입니다.
