# MagicSquare_xx — 테스트 계획서

| 항목 | 내용 |
|------|------|
| 문서 ID | TP-AC-FR-01-01 |
| 기준 AC | **AC-FR-01-01** — `grid = None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |
| PRD 요구사항 | **FR-01** (MS-US-01 입력 검증), **§9.2 Input Contract**, 불변식 **P-1** (4×4 차원) |
| Report 근거 | `Report/06.PRD_MagicSquare_xx.md`, `Report/02.DualTrack_CleanArchitecture_Design_Report.md` (U-T01, D-T07, IT-03), `Report/05.InvariantsBased_TDD_UserJourney_Stories_Scenarios_Report.md` |
| 기술 스택 | Python 3.10+, pytest, pydantic, unittest.mock |
| 작성일 | 2026-05-29 |
| 작성 역할 | 시니어 QA 리드 |

---

## 1. 목적 및 범위

### 1.1 목적

본 계획서는 **FR-01 입력 유효성 검사**의 최우선 Acceptance Criteria인 **AC-FR-01-01**을 중심으로, Dual-Track TDD에서 **Boundary(형식·조기 거부)** 와 **Domain 진입점 격리**를 pytest 단위 테스트로 검증하는 범위·우선순위·측정 전략을 정의한다.

### 1.2 In Scope

- Boundary 레이어: `grid` 형식/차원 선검증 (null, 빈 리스트, jagged, 크기 불일치)
- 오류 계약: `errorCode` + 고정 `message` 쌍 반환
- Domain 해 결정 진입점(`solve` 또는 동등 포트) **미호출** 검증
- pydantic 기반 입력 스키마 검증(선택·권장)과 Boundary 비즈니스 로직의 역할 분리

### 1.3 Out of Scope (본 AC 범위 외 — 테스트 포함 금지)

| 제외 항목 | 사유 |
|-----------|------|
| **4×4 정상 입력** (빈칸 2개, 값·중복 유효) | AC-FR-01-01은 **형식 거부** 전용; 정상 흐름은 FR-01 후속 AC 또는 MS-US-05(Output Contract)에서 검증 |
| 빈칸 개수 오류 (P-2) | 별도 AC (예: AC-FR-01-02, U-T04) |
| 값 범위·중복 오류 (P-3, P-4) | 별도 AC (U-T03, U-T08) |
| No solution 실패 | Domain/Output Contract (MS-US-05) |
| Data 레이어 영속화 | 별도 Data 테스트 (DT-T*) |

---

## 2. 추적성 (Traceability)

| 계층 | ID | AC/Story | 검증 대상 |
|------|-----|----------|-----------|
| Boundary | **AC-FR-01-01** | FR-01, MS-US-01 | `grid = None` → `INVALID_SIZE`, Domain 미호출 |
| Boundary | AC-FR-01-02 | FR-01, P-1 | `grid = []` → `INVALID_SIZE` |
| Boundary | AC-FR-01-03 | FR-01, P-1 | jagged `[[]]*4` → `INVALID_SIZE` |
| Boundary | AC-FR-01-04~06 | FR-01, P-1 | 3×4, 4×3, 5×5 → `INVALID_SIZE` |
| Domain (참고) | D-T07 | P-1 | `validatePartialGrid` 차원 위반 (Boundary 통과 후 위임 경로) |
| Integration (참고) | IT-03 | FR-01 | E2E null 입력 (후속 단계) |

**Report 02 매핑 참고:** Report 설계서는 null에 `UI_NULL_GRID`, 차원 위반에 `DIMENSION_INVALID`를 사용한다. 본 AC는 QA 계약상 **`INVALID_SIZE` + `"Grid must be 4x4."`** 를 고정 golden string으로 사용한다. 구현 시 Boundary 내부 코드 enum과의 1:1 매핑은 별도 매핑 표로 문서화한다.

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 Dual-Track 분리

| Track | 대상 모듈 (예정) | Mock 정책 | 본 AC 포함 |
|-------|------------------|-----------|------------|
| **UI / Boundary Track** | `boundary/` (ScreenBoundary, GridInputValidator) | **Domain `solve` Mock** — 호출 횟수·인자 검증 | **Yes (1차)** |
| **Logic / Domain Track** | `entity/` 또는 `control/` (`validatePartialGrid`, `PartialGridValidator`) | Domain 외부 I/O 없음, 순수 입력 | No (AC-FR-01-01 범위 외; D-T07은 후속 RED) |

AC-FR-01-01 및 본 문서의 경계값 목록은 **Boundary Track 단위 테스트**에만 포함한다.

### 3.2 테스트 파일 배치 (권장)

```
tests/
├── boundary/
│   └── test_grid_input_validation.py    # AC-FR-01-01 ~ 06 (본 계획)
├── entity/
│   └── test_partial_grid_validator.py   # D-T07 등 (후속)
└── conftest.py                          # 공통 fixture, mock factory
```

### 3.3 우선순위 (RED → GREEN 순서)

| 우선순위 | Test-ID | 시나리오 | AC | RED 선행 이유 |
|----------|---------|----------|-----|---------------|
| **P0** | B-T01 | `grid = None` | AC-FR-01-01 | FR-01 최선행 조건; null은 모든 후속 검증의 전제 붕괴 |
| **P0** | B-T02 | `grid = []` | AC-FR-01-02 | 빈 컨테이너 — null과 구분되는 0×0 형식 |
| **P1** | B-T03 | `grid = [[]] * 4` | AC-FR-01-03 | 행 4개 존재·열 0 — jagged/길이 불일치 대표 |
| **P1** | B-T04 | `grid` = 3×4 | AC-FR-01-04 | 행 수 불일치 |
| **P1** | B-T05 | `grid` = 4×3 | AC-FR-01-05 | 열 수 불일치 |
| **P1** | B-T06 | `grid` = 5×5 | AC-FR-01-06 | 양방향 초과 |
| **P2** | B-T07 | Domain Mock 호출 횟수 일괄 assert (B-T01~06 공통) | AC-FR-01-01~06 | 격리 전략 회귀 보호 |
| **P2** | B-T08 | 오류 스키마 필드 존재 (`code`, `message`) | Error Contract | UX-2, R-3 회귀 |
| **—** | *(제외)* | 4×4 정상 입력 | — | **본 AC 범위 외, 테스트 작성 금지** |

### 3.4 테스트 패턴

- **Framework:** pytest
- **Pattern:** AAA (Arrange – Act – Assert)
- **Naming:** `test_<layer>_<condition>_<expected>`  
  예: `test_boundary_grid_none_returns_invalid_size_and_skips_domain`
- **Fixture scope:** function (기본); session/module은 사용하지 않음
- **Parametrize:** B-T04~B-T06은 `@pytest.mark.parametrize`로 크기 불일치 케이스 통합 가능

---

## 4. 경계값 케이스 목록

모든 케이스의 **공통 기대 결과:**

```json
{
  "code": "INVALID_SIZE",
  "message": "Grid must be 4x4."
}
```

| ID | 입력 | Arrange 상세 | 기대 | Domain `solve` 호출 |
|----|------|--------------|------|---------------------|
| **B-T01** | `grid = None` | 명시적 `None` 전달 | `INVALID_SIZE` | **0회** |
| **B-T02** | `grid = []` | 빈 리스트 (행 0개) | `INVALID_SIZE` | **0회** |
| **B-T03** | `grid = [[]] * 4` | 4행, 각 행 길이 0 (jagged) | `INVALID_SIZE` | **0회** |
| **B-T04** | 3×4 격자 | `[[0]*4 for _ in range(3)]` | `INVALID_SIZE` | **0회** |
| **B-T05** | 4×3 격자 | `[[0]*3 for _ in range(4)]` | `INVALID_SIZE` | **0회** |
| **B-T06** | 5×5 격자 | `[[0]*5 for _ in range(5)]` | `INVALID_SIZE` | **0회** |

### 4.1 명시적 제외 (포함 금지)

| 입력 | 제외 사유 |
|------|-----------|
| **4×4 정상 입력** (예: 빈칸 2개, 1~16 범위 준수) | AC-FR-01-01은 **INVALID_SIZE 거부**만 검증; 정상 입력은 Domain 호출·성공 응답 AC에서 다룸 (U-T05, D-T01) |

---

## 5. 예외 / 특이 케이스 목록

AC-FR-01-01 직접 범위는 아니나, FR-01 입력 검증 RED/GREEN 시 **인접 회귀**로 함께 기록한다. 구현 착수 시 우선순위 P2~P3로 분류.

| ID | 케이스 | 입력 예시 | 기대 동작 | 비고 |
|----|--------|-----------|-----------|------|
| E-01 | **Jagged row 혼합** | `[[1,2,3,4], [1,2,3], [1,2,3,4], [1,2,3,4]]` | `INVALID_SIZE` (또는 설계 확정 시 `UI_JAGGED_ROW`) | B-T03 확장; Report 02 U-T02 |
| E-02 | **비-리스트 타입** | `grid = "4x4"`, `grid = 16`, `grid = {}` | `INVALID_SIZE` 또는 타입 거부 코드 | pydantic `ValidationError` → Boundary 오류 스키마 변환 |
| E-03 | **numpy/list 혼용 행** | 행 하나만 tuple | 형식 거부 | Python 3.10+ 타입 힌트와 런타임 검증 불일치 방지 |
| E-04 | **얕은 복사 함정** | `[[]]*4` 후 `grid[0].append(1)` | 여전히 INVALID_SIZE (변형 후에도 4×4 아님) | `[[]]*4` idiom 부작용 인지 테스트 |
| E-05 | **None vs missing key** | API body에 `grid` 필드 누락 | pydantic: 필수 필드 오류 → Boundary 표준 오류 | API Boundary 전용 |
| E-06 | **Domain 예외 누수 방지** | (형식 오류 입력) | Domain 예외가 raw로 전파되지 않음 | Boundary가 항상 Error schema 반환 |
| E-07 | **message golden string** | B-T01~06 아무거나 | `message` 완전 일치 (공백·마침표 포함) | Report R-3, UX-3 |
| E-08 | **결정성 (M-1)** | B-T01 동일 입력 2회 | 동일 `code`, `message` | 메타 불변식 |

---

## 6. Domain 해 결정 진입점 호출 횟수 검증 전략

### 6.1 검증 대상

- **진입점:** Domain 해 결정 함수 — Report 02 기준 `solve(grid: int[4][4]) -> int[6]`
- **주입 위치:** Boundary → Control → Domain 경로에서 **Boundary 테스트는 Domain 포트만 Mock**

### 6.2 Mock / Spy 전략 (unittest.mock)

| 항목 | 전략 |
|------|------|
| **도구** | `unittest.mock.create_autospec` 또는 `MagicMock(spec=SolvePort)` |
| **주입** | Boundary 생성자/factory에 Domain 포트 주입 (DI); 테스트에서 mock 교체 |
| **Assert** | `mock_solve.assert_not_called()` — B-T01~06 각각 |
| **회귀** | `mock_solve.call_count == 0` — parametrize 일괄 검증 (B-T07) |
| **부정 검증** | `assert_not_called()` 실패 시, 호출 인자 `call_args`를 failure message에 포함 |

### 6.3 Fixture 예시 (계획 수준 — 구현 시 참고)

```python
# conftest.py (개념)
@pytest.fixture
def mock_domain_solve(mocker):
    return mocker.patch("boundary.screen.solve", autospec=True)

@pytest.fixture
def boundary(mock_domain_solve):
    return ScreenBoundary(domain_solve=mock_domain_solve)
```

### 6.4 Spy vs Mock 선택 기준

| 방식 | 사용 시점 |
|------|-----------|
| **Mock (replace)** | Boundary 단위 테스트 **기본** — Domain 완전 격리, 호출 횟수 0 단정 |
| **Spy (wrap)** | Integration(IT-03) 또는 Boundary+실 Domain smoke — 본 AC P0~P1에서는 **사용하지 않음** |

### 6.5 실패 시 진단 체크리스트

1. Boundary가 차원 검사 **전에** Domain을 호출하지 않는가?
2. pydantic 검증 실패가 Domain 호출 **이전**에 catch되는가?
3. 예외 handler가 fallback으로 Domain을 재시도하지 않는가?

---

## 7. pydantic 역할 (입력 계약)

| 레이어 | 책임 |
|--------|------|
| **pydantic Model** | `grid: list[list[int]]` 존재·타입·nullable 거부 (선택: `min_length=4`, `max_length=4`) |
| **Boundary Validator** | P-1 차원 최종 판정 (각 row 길이 4, null/empty/jagged) — **AC-FR-01-01 비즈니스 로직** |
| **Domain** | P-2~P-5 및 해 결정 — **본 AC에서 호출 금지** |

pydantic `ValidationError` 발생 시 Boundary는 Domain을 호출하지 않고 `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }`로 **정규화**한다.

---

## 8. 커버리지 목표

Report 02 §4.4 및 PRD §13 기준:

| 레이어 | 목표 | 본 AC 기여 |
|--------|------|------------|
| **Domain (entity/control)** | **≥ 95%** | AC-FR-01-01 Boundary 테스트만으로는 Domain 커버리지 **미기여** (Mock으로 제외) |
| **Boundary** | **≥ 85%** | B-T01~08이 `grid` 형식 거부 분기·오류 매핑 경로 커버 |
| **Data** | ≥ 80% | 본 AC 해당 없음 |

### 8.1 Boundary 커버리지 — 본 AC에서 반드시 커버할 분기

- `grid is None` 분기
- `len(grid) != 4` 분기
- `any(len(row) != 4 for row in grid)` 분기
- 오류 응답 빌더 (`code`, `message` 조립)
- Domain 호출 **직전** early-return 경로

### 8.2 Domain 95%+ 달성 경로 (후속, 참고)

- D-T07 (`validatePartialGrid` — 3×4 등) — Boundary Mock **없이** Domain 단위 테스트
- 본 문서 범위 완료 후 Logic Track RED 진행

---

## 9. pytest-cov 측정 전략

### 9.1 설치

```bash
pip install pytest-cov
```

### 9.2 실행 (Boundary Track — 본 AC)

```bash
pytest tests/boundary/test_grid_input_validation.py \
  --cov=src \
  --cov-report=term-missing \
  -v
```

> **Note:** 저장소 ECB 구조가 `boundary/`, `entity/` 루트에 있을 경우, 측정 대상을 아래처럼 조정한다.  
> `--cov=boundary --cov-report=term-missing`

### 9.3 Dual-Track 분리 측정

| Track | 명령 | 목표 |
|-------|------|------|
| Boundary only | `pytest tests/boundary/ --cov=boundary --cov-report=term-missing` | **≥ 85%** |
| Domain only | `pytest tests/entity/ tests/control/ --cov=entity --cov=control --cov-report=term-missing` | **≥ 95%** |
| Full (CI) | `pytest --cov=src --cov-report=term-missing --cov-report=html` | 각 레이어 threshold gate |

### 9.4 커버리지 게이트 (CI 권장)

```bash
pytest --cov=src --cov-report=term-missing \
  --cov-fail-under=85
```

- Boundary 전용 job: `--cov=boundary --cov-fail-under=85`
- Domain 전용 job: `--cov=entity --cov=control --cov-fail-under=95`

### 9.5 측정 시 주의

| 항목 | 규칙 |
|------|------|
| Mock 사용 | Boundary 테스트에서 Domain mock 시 Domain 코드는 **execute되지 않음** — Domain 커버리지는 Logic Track에서 별도 측정 |
| `--cov=src` | `src` 패키지 도입 시 layout alias; 미도입 시 ECB 루트 모듈명 사용 |
| term-missing | RED phase에서 missing line을 RED 대상 구현 위치 힌트로 활용 |
| html report | `htmlcov/index.html` — PR 리뷰용 (선택) |

---

## 10. RED → GREEN → REFACTOR 체크리스트

### RED (Boundary)

- [ ] B-T01: `grid=None` → `INVALID_SIZE`, `mock_solve.assert_not_called()`
- [ ] B-T02~B-T06: 경계값 각각 RED
- [ ] 의도한 단일 실패 원인 확인 (다중 assert 실패 시 테스트 분리)

### GREEN (최소 구현)

- [ ] Boundary에 null/empty/jagged/크기 불일치 early-return
- [ ] 고정 message `"Grid must be 4x4."` 반환
- [ ] Domain 호출 코드 경로에 도달하지 않음

### REFACTOR

- [ ] pydantic 모델과 Boundary validator 책임 정리
- [ ] 중복 차원 검사 제거 (단, 외부 계약 불변)
- [ ] 전체 테스트 green + Boundary coverage ≥ 85% 유지

---

## 11. 완료 기준 (Definition of Done)

| # | 기준 |
|---|------|
| 1 | AC-FR-01-01 (B-T01) pytest **GREEN** |
| 2 | §4 경계값 B-T02~B-T06 전건 GREEN |
| 3 | Domain `solve` **호출 0회** assert 전건 통과 |
| 4 | `message` golden string 회귀 테스트 통과 |
| 5 | Boundary coverage **≥ 85%** (`pytest-cov` term-missing 확인) |
| 6 | **4×4 정상 입력 테스트가 본 AC 테스트 파일에 포함되지 않음** |

---

## 12. 참고 문서

- [Report/06.PRD_MagicSquare_xx.md](../Report/06.PRD_MagicSquare_xx.md) — FR-01, §9.2 Input Contract
- [Report/02.DualTrack_CleanArchitecture_Design_Report.md](../Report/02.DualTrack_CleanArchitecture_Design_Report.md) — U-T01~U-T04, D-T07, §4.4 Coverage
- [Report/05.InvariantsBased_TDD_UserJourney_Stories_Scenarios_Report.md](../Report/05.InvariantsBased_TDD_UserJourney_Stories_Scenarios_Report.md) — MS-US-01, SC-BND-VAL
- [.cursor/rules/magicsquare-tdd-testing.mdc](../.cursor/rules/magicsquare-tdd-testing.mdc) — RED/GREEN/REFACTOR, AAA

---

*본 문서는 테스트 **계획**이며, 구현 코드는 포함하지 않는다. AC-FR-01-01 범위에서 4×4 정상 입력 시나리오는 의도적으로 제외한다.*
