# MagicSquare_xx

4×4 마방진(Magic Square)을 다루는 프로그램 과제입니다.  
QA 엔지니어 관점에서 **문제 정의·검증 가능한 요구**를 먼저 고정하고, 이후 구현·테스트로 확장하는 것을 목표로 합니다.

> **현재 단계:** AC-FR-01-01 **GREEN 완료** — Boundary `ScreenBoundary.submit()` 입력 검증 (통합 2커밋 전략)

---

## TDD GREEN 체크리스트 (AC-FR-01-01 · 통합 2커밋)

> 테스트 파일: [`tests/boundary/test_grid_input_validation_ac_fr_01_01.py`](./tests/boundary/test_grid_input_validation_ac_fr_01_01.py) (25건)  
> 검증 명령: `pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v`  
> 커밋 전략: **세분화 4커밋 대신 통합 2커밋** (None → size 일괄)

### 커밋 1 — `grid=None` (B-T01) · DEF-001 · ✅ GREEN 완료

- [x] RED 확인: `submit(grid=None)` → `NotImplementedError` 또는 계약 미충족
- [x] GREEN 구현: `grid is None` → `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")`
- [x] `resolve` 0회 호출 (Domain 격리)
- [x] `TestNormalFailureReturn` 5건 통과 (#1~5)
- [x] `TestDomainIsolation` — None 2건 통과 (#6~7)
- [x] `TestMessageIdentity` — None 2건 통과 (#8~9)
- [x] 커밋: `a85ae7d` — `feat(boundary): AC-FR-01-01 GREEN commit 1 and project docs`

**대상 입력:** `grid = None`  
**검증:** `pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py::TestNormalFailureReturn -v` (9/9 PASS)

---

### 커밋 2 — size 위반 일괄 (B-T02~B-T04) · DEF-002~004 + 메타 · DEF-005~008 · ✅ GREEN 완료

#### 2-A. Boundary 구현 (size 검증 일괄)

- [x] RED 확인: `[]`, `[[]]*4`, `3×4` → `NotImplementedError` 또는 계약 미충족
- [x] GREEN 구현 — `[]` (0행): `len(grid) == 0` 조기 거부
- [x] GREEN 구현 — jagged `[[]]*4`: `any(len(row) != 4 for row in grid)` 조기 거부
- [x] GREEN 구현 — `3×4`: `len(grid) != 4` 조기 거부
- [x] 공통 응답: `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")`
- [x] 모든 size 실패 경로에서 `resolve` 0회 호출
- [x] `TestBoundaryValues` 5건 통과 (#10~14)
- [x] `TestDomainIsolation` — size 3건 통과 (#15~17)
- [x] `TestMessageIdentity` — size 3건 통과 (#18~20)

**대상 입력:**

| ID | 입력 | 건수 |
|----|------|------|
| B-T02 | `grid = []` | 4 |
| B-T03 | `grid = [[]] * 4` | 4 |
| B-T04 | `grid = [[0]*4 for _ in range(3)]` | 3 |

#### 2-B. 메타 테스트 정합성 (TestScopeRestriction)

- [x] #21 `test_module_has_no_4x4_valid_grid_test_function` — 기능 테스트 함수명만 검사 (자기 자신 제외)
- [x] #22 `test_module_has_no_forbidden_ac_fr_01_02_to_05_test_names` — docstring/상수 오탐 제거
- [x] #23 `test_module_has_no_fr_02_to_05_references_in_test_names` — 메타 함수명 self-match 제거
- [x] #24 `test_module_has_no_4x3_or_5x5_grid_literal_tests` — 기능 테스트 소스만 검사
- [x] #25 `test_module_docstring_declares_ac_fr_01_01_only` (이미 GREEN)

#### 2-C. 커밋 2 완료 기준

- [x] 기능 테스트 20건 전체 GREEN (`TestNormalFailureReturn` ~ `TestMessageIdentity`)
- [x] 메타 테스트 5건 전체 GREEN (`TestScopeRestriction`)
- [x] **파일 합계 25 passed**
- [x] `pytest --cov=src --cov-report=term-missing` — Boundary 검증 분기 커버 확인 (DEF-009, `screen_boundary` 93%)
- [x] [docs/defect_list.md](./docs/defect_list.md) Open 결함 0건 갱신
- [x] 커밋: `feat(boundary): AC-FR-01-01 GREEN — INVALID_SIZE size validation`

**수정 허용 범위 (커밋 2-A):** `src/boundary/screen_boundary.py`, `src/boundary/models.py`, `src/boundary/__init__.py`  
**금지:** `resolve()` 구현, AC-FR-01-02~05 선행, 4×3·5×5·정상 4×4 테스트 추가

**검증:** `pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v` (25/25 PASS)

---

### GREEN 단계 공통 규칙

- [x] RED 없이 프로덕션 코드 작성 금지 (`.cursorrules` green_phase)
- [ ] GREEN 단계에서 리팩터링·추상화 확장 금지 (통과에 필요한 최소 코드만)
- [ ] 테스트 삭제·완화·skip으로 RED 숨기기 금지

---

### 진행 현황 스냅샷

| 구분 | 통과 | 실패 | 비고 |
|------|------|------|------|
| 커밋 1 (None) | 9 | 0 | GREEN 완료 |
| 커밋 2-A (size) | 11 | 0 | GREEN 완료 |
| 커밋 2-B (메타) | 5 | 0 | GREEN 완료 |
| **합계** | **25** | **0** | 25 collected |

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
├── pytest.ini
├── src/                                                         ← boundary (ScreenBoundary, FailureResult)
├── tests/
│   ├── conftest.py                                              ← src 우선 sys.path, mock_resolve fixture
│   └── boundary/
│       └── test_grid_input_validation_ac_fr_01_01.py            ← AC-FR-01-01 (25건)
├── docs/                                                        ← test_plan.md, defect_list.md
├── Report/
│   ├── 01.ProblemDefinition_Report.md                           ← STEP 1~5 문제 정의
│   ├── 02.DualTrack_CleanArchitecture_Design_Report.md          ← Dual-Track · CA 설계
│   ├── 06.PRD_MagicSquare_xx.md                                 ← 구현 전 PRD
│   ├── 07.AC_FR_01_01_RED_Testing_and_QA_Report.md              ← AC-FR-01-01 RED·QA 보고서
│   └── 10.AC_FR_01_01_GREEN_Testing_and_Implementation_Report.md ← AC-FR-01-01 GREEN 보고서
├── Prompt/
│   ├── 02.DualTrack_CleanArchitecture_Design-Prompt.md           ← 설계 단계 대화 transcript
│   ├── 07.AC_FR_01_01_RED_Testing-Prompt.md                     ← RED 테스트 단계 transcript
│   └── 10.AC_FR_01_01_GREEN_Testing-Prompt.md                   ← GREEN 테스트 단계 transcript
└── Prompting/
    └── 01.ProblemDefinition_Report-Prompt.md                    ← 문제 정의 대화 transcript
```

| 경로 | 설명 |
|------|------|
| [src/boundary/screen_boundary.py](./src/boundary/screen_boundary.py) | Boundary 진입점 — `submit()` 입력 검증 (AC-FR-01-01 GREEN) |
| [tests/boundary/test_grid_input_validation_ac_fr_01_01.py](./tests/boundary/test_grid_input_validation_ac_fr_01_01.py) | AC-FR-01-01 Full RED→GREEN (25건) |
| [Report/01.ProblemDefinition_Report.md](./Report/01.ProblemDefinition_Report.md) | 관찰, Why #1~#3, 진짜 문제 정의, Invariant, 부록 전체 |
| [Report/02.DualTrack_CleanArchitecture_Design_Report.md](./Report/02.DualTrack_CleanArchitecture_Design_Report.md) | Logic / UI Boundary / Data 설계, 테스트·통합·Traceability |
| [Report/06.PRD_MagicSquare_xx.md](./Report/06.PRD_MagicSquare_xx.md) | 구현 전 PRD(비전/범위/계약/불변식/검증/품질바) |
| [Report/07.AC_FR_01_01_RED_Testing_and_QA_Report.md](./Report/07.AC_FR_01_01_RED_Testing_and_QA_Report.md) | AC-FR-01-01 RED 테스트·QA·결함·환경 정비 보고서 |
| [Report/10.AC_FR_01_01_GREEN_Testing_and_Implementation_Report.md](./Report/10.AC_FR_01_01_GREEN_Testing_and_Implementation_Report.md) | AC-FR-01-01 GREEN 완료·통합 2커밋·25 passed 스냅샷 |
| [docs/test_plan.md](./docs/test_plan.md) | AC-FR-01-01 테스트 계획서 (B-T01~B-T06) |
| [docs/defect_list.md](./docs/defect_list.md) | RED/GREEN 결함 목록 |
| [Prompt/02.DualTrack_CleanArchitecture_Design-Prompt.md](./Prompt/02.DualTrack_CleanArchitecture_Design-Prompt.md) | Dual-Track 설계 단계 User/Cursor 프롬프트 export |
| [Prompt/07.AC_FR_01_01_RED_Testing-Prompt.md](./Prompt/07.AC_FR_01_01_RED_Testing-Prompt.md) | AC-FR-01-01 RED 테스트 단계 transcript |
| [Prompt/10.AC_FR_01_01_GREEN_Testing-Prompt.md](./Prompt/10.AC_FR_01_01_GREEN_Testing-Prompt.md) | AC-FR-01-01 GREEN 테스트 단계 transcript |
| [Prompting/01.ProblemDefinition_Report-Prompt.md](./Prompt/01.ProblemDefinition_Report-Prompt.md) | 문제 정의 단계 User/Cursor 프롬프트 export |

---

## 다음 단계 (제안)

1. [02 설계서](./Report/02.DualTrack_CleanArchitecture_Design_Report.md) 기준 **Domain RED** (D-T07~D-T09)
2. UI Boundary U-IN-04~08 (`tests/boundary/test_u_in_validation.py`)
3. Data `MatrixRepository` InMemory → (선택) File JSON
4. 통합 시나리오 IT-01~IT-06, 커버리지 목표 (Domain 95%+ / UI 85%+ / Data 80%+)

---

## RED 단계 To-Do 리스트 (완료)

> AC-FR-01-01 RED는 완료되었습니다. GREEN 진행은 상단 **「TDD GREEN 체크리스트」** 를 따릅니다.

### Track A — UI / Boundary 테스트 (RED 작성 완료)
- [x] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [x] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [x] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [x] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [x] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [x] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [x] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트 (RED 스코프)
- [x] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [x] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [x] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [x] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록 ([docs/defect_list.md](./docs/defect_list.md))
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인 (GREEN 커밋 2 완료 — 25/25 PASS)

---

## Golden Master 회귀 안전장치

> Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.

### 기준 파일 생성

- [x] GM-01: `golden_master_expected.txt` 생성 ([tests/golden_master_expected.txt](./tests/golden_master_expected.txt))
- [x] GM-02: 정상/역순/오류 시나리오 추가 (GM-TC-01~05)
- [x] GM-03: `git add tests/golden_master_expected.txt`

### 테스트 코드

- [x] GM-04: `test_golden_master_magic_square` 작성 ([tests/test_golden_master_magic_square.py](./tests/test_golden_master_magic_square.py))
- [x] GM-05: approve 패턴 적용 (`--approve-golden`, `GOLDEN_MASTER_APPROVE=1`)
- [x] GM-06: Golden Master 테스트 PASS 확인 (`pytest -m golden_master -v` — 9/9 PASS)

### 회귀 보호

- [x] GM-07: row-major 규칙 보호
- [x] GM-08: 1-index 출력 보호
- [x] GM-09: reverse 조합 fallback 보호
- [x] GM-10: Error Contract 보호

> 상세 설계: [docs/golden_master_approve_pattern.md](./docs/golden_master_approve_pattern.md)

---

## TDD REFACTOR 체크리스트 (`src/boundary/screen_boundary.py`)

> **전제:** `.cursorrules` `refactor_phase` — 기능 변경 없이 구조만 개선, **관련 테스트 GREEN 유지**, 커버리지·핵심 경로 검증 유지.  
> **범위:** AC-FR-01-01(25 GREEN) + Golden Master(9 GREEN)가 보호하는 `screen_boundary` 경로만. RED 스켈레톤·U-IN/U-OUT/U-FLOW·control/UI 신규 테스트는 **이번 REFACTOR 범위 밖** (별도 GREEN phase).  
> **상세 보고서:** [Report/14.Screen_Boundary_REFACTOR_Implementation_Report.md](./Report/14.Screen_Boundary_REFACTOR_Implementation_Report.md) · Transcript: [Prompt/14.Screen_Boundary_REFACTOR-Prompt.md](./Prompt/14.Screen_Boundary_REFACTOR-Prompt.md) · 준비: [Report/13...](./Report/13.REFACTOR_Phase_Readiness_and_Checklist_Report.md)

### REFACTOR 단계 공통 규칙

- [ ] 외부 동작(기능)을 바꾸지 않는다
- [ ] 리팩터 중 관련 테스트가 계속 GREEN인지 수시로 확인한다
- [ ] 테스트 삭제·완화·skip으로 실패를 숨기지 않는다
- [ ] 커버리지를 낮추거나 테스트가 못 잡는 변경을 섞지 않는다

---

### 1. 테스트 안전망 (이번 REFACTOR 범위)

| 대상 | `test_*.py` | 상태 | 역할 |
|------|-------------|------|------|
| `src/boundary/screen_boundary.py` | [`test_grid_input_validation_ac_fr_01_01.py`](./tests/boundary/test_grid_input_validation_ac_fr_01_01.py) | **25 GREEN** | size 검증 · `INVALID_SIZE` · `resolve` 0회 격리 |
| | [`test_golden_master_magic_square.py`](./tests/test_golden_master_magic_square.py) | **9 GREEN** | `ScreenBoundary` + `resolve` 통합 회귀 |

---

### 2. REFACTOR 착수 순서

```
[1] screen_boundary.py 구조 리팩터 (§ 3 Refactoring To-Do)
[2] 매 변경 후: pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v
              pytest -m golden_master -v
```

| 단계 | 수정 허용 범위 | 금지 |
|------|----------------|------|
| 1 | `src/boundary/screen_boundary.py` — 책임 분리 · `GRID_SIZE` SSOT · private 추출 | AC-FR-01-01 `INVALID_SIZE` 계약 변경 |
| | | invalid size 시 `resolve` 호출 |
| | | GM-TC-03~05 Error Contract code·message 변경 |

---

### 3. Refactoring To-Do — `src/boundary/screen_boundary.py`

> **금지:** `INVALID_SIZE` code·message 변경, invalid size 시 `resolve` 호출, GM-TC-03~05 Error Contract code·message 변경.

| # | 항목 | 내용 | 허용 이유 |
|---|------|------|-----------|
| 1 | stale docstring | 구현 완료 전 RED 시절 docstring 제거 | 동작 무관 |
| 2 | `GRID_SIZE` SSOT | `entity.constants.GRID_SIZE` import (모듈 re-export 유지) | 값 4 불변 → AC-FR-01-01 유지 |
| 3 | size 검증 DRY | `None` / 행·열 불일치의 동일 `FailureResult` 블록 → `_invalid_size_result()` 등 | code·message·`resolve` 0회 불변 |
| 4 | private 추출 | `_is_valid_grid_size(grid)` | AC-FR-01-01 격리 테스트 유지 |
| 5 | domain 매핑 정리 | `DomainError` → `FailureResult` try/except를 `_to_failure(exc)` 등으로 분리 | GM-TC-03~05 code·message 불변 |

**체크리스트**

- [x] **SB-R-01** stale docstring 제거 (`ScreenBoundary` 클래스 docstring)
- [x] **SB-R-02** `GRID_SIZE` — `from entity.constants import GRID_SIZE` + 모듈 re-export
- [x] **SB-R-03** `_invalid_size_result()` — `INVALID_SIZE` / `"Grid must be 4x4."` 단일 생성
- [x] **SB-R-04** `_is_valid_grid_size(grid)` — size 검증 private 추출
- [x] **SB-R-05** `_to_failure(exc: DomainError)` — domain → DTO 매핑 분리
- [x] **SB-R-V** 검증 — AC-FR-01-01 25/25 + Golden Master 9/9 PASS

---

### 4. 검증 명령

```bash
# AC-FR-01-01 (Boundary size 검증 — REFACTOR 중 항상 GREEN)
pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v

# Golden Master (통합 회귀 — REFACTOR 안전망)
pytest -m golden_master -v
```

#### 수동 스모크 테스트 (GUI)

> 자동화 pytest 이후, REFACTOR·릴리스 전 **사람이 눈으로 확인**하는 최소 시나리오.  
> Golden Master(GM-TC-01~05)와 동일 입력·기대를 GUI에서 재현한다.

**실행 (프로젝트 루트):**

```bash
pip install -r requirements.txt   # 최초 1회 (PyQt6)
python main.py
```

```powershell
# Windows · venv 사용 시
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

**공통 확인**

- [ ] 창 제목 `MagicSquare_xx — 4×4 마방진 퍼즐`, 4×4 격자·「해결」「초기화」「샘플 불러오기」 버튼 표시
- [ ] 기동 시 **샘플 불러오기** 상태 메시지 (`샘플 퍼즐이 로드되었습니다…`)
- [ ] 창 닫기 시 프로세스 정상 종료 (크래시 없음)

| ID | 조작 | 기대 결과 (결과 패널) |
|----|------|------------------------|
| **SM-01** | 샘플 로드 → **해결** (GM-TC-02 / G2) | 녹색 성공 — `(3,3)→6`, `(4,4)→1`, 벡터 `[3, 3, 6, 4, 4, 1]` |
| **SM-02** | **초기화** 후 격자 수동 입력 — GM-TC-01 격자 → **해결** | 성공 — `(3,3)→6`, `(4,3)→15` (small-first) |
| **SM-03** | 빈칸 3개 (예: (4,3)·(4,4) 모두 `0`) → **해결** | `[EMPTY_COUNT_INVALID]` 빨간 오류 |
| **SM-04** | non-zero `7` 중복 (GM-TC-04) → **해결** | `[DUPLICATE_NONZERO]` |
| **SM-05** | GM-TC-05 격자 입력 → **해결** | `[NO_VALID_COMPLETION]` |
| **SM-06** | 한 칸에 `abc` 입력 → **해결** | `[UI_PARSE_ERROR]` — `(행,열) 칸에 올바른 정수…` |
| **SM-07** | 한 칸에 `17` 또는 `-1` → **해결** | `[UI_CELL_RANGE]` — `0 또는 1~16` |
| **SM-08** | **초기화** → **해결** (빈 격자) | Domain/Boundary 오류 코드 표시 (빈칸 수·값 계약 위반) |

REFACTOR 후 **SM-01·SM-02**는 반드시 재실행한다 (출력 포맷·좌표 1-index·격자 반영 회귀).

---

### 5. 진행 현황 (REFACTOR)

| 구분 | GREEN | 비고 |
|------|-------|------|
| AC-FR-01-01 (`screen_boundary` size) | 25 | REFACTOR 완료 |
| Golden Master | 9 | 통합 회귀 안전망 |
| `screen_boundary.py` To-Do (§ 3) | 6/6 | SB-R-01~05 + SB-R-V 완료 |

---

## 문서 이력

| 날짜 | 내용 |
|------|------|
| 2026-05-28 | STEP 1~5 문제 정의 완료, `Report/01.ProblemDefinition_Report.md` 작성 |
| 2026-05-28 | Dual-Track · Clean Architecture 설계, `Report/02...`, `Prompt/02...` 작성 |
| 2026-05-28 | 구현 전 PRD 초안 작성, `Report/06.PRD_MagicSquare_xx.md` 작성 |
| 2026-05-29 | AC-FR-01-01 RED 결함 목록, `docs/defect_list.md` 작성 |
| 2026-05-29 | AC-FR-01-01 RED·QA 보고서·transcript, `Report/07...`, `Prompt/07...` 작성 |
| 2026-05-29 | AC-FR-01-01 GREEN 시작 — Boundary `ScreenBoundary.submit()`, 통합 2커밋 전략 README 반영 |
| 2026-05-29 | AC-FR-01-01 GREEN 완료 보고서·transcript 갱신, `Report/10...`, `Prompt/10...` (25 passed) |
| 2026-05-29 | TDD REFACTOR 체크리스트 추가 (`control` / `boundary` / `boundary/ui`) |
| 2026-05-29 | REFACTOR 준비 보고서·transcript, `Report/13...`, `Prompt/13...` |
| 2026-05-29 | `screen_boundary.py` Refactoring To-Do (§ 3-A) 추가 |
| 2026-05-29 | REFACTOR 체크리스트 범위 정리 — RED·범위 밖 항목 제거, `screen_boundary` 한정 |
| 2026-05-29 | `screen_boundary.py` REFACTOR 3커밋 완료 — `Report/14...`, `Prompt/14...` |

---

## 참고

- 문제 정의: [01.ProblemDefinition_Report.md](./Report/01.ProblemDefinition_Report.md)
- 아키텍처·TDD 설계: [02.DualTrack_CleanArchitecture_Design_Report.md](./Report/02.DualTrack_CleanArchitecture_Design_Report.md)
- Boundary 구현은 AC-FR-01-01 입력 검증부터 진행 중이며, Domain `resolve()` 및 정상 4×4 흐름은 후속 AC에서 다룹니다.
