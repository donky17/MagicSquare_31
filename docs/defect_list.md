# MagicSquare_xx — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 ID | DL-AC-FR-01-01 |
| 기준 AC | AC-FR-01-01 (FR-01 입력 검증, PRD §8.1 `INVALID_SIZE`) |
| 테스트 계획 | [test_plan.md](./test_plan.md) |
| 최종 실행 | `pytest` (2026-05-29, Python 3.13.13, pytest 9.0.3) |
| 실행 결과 | **24 failed, 11 passed** (총 35 collected) |
| 상태 | **RED 단계** — 구현 결함 + 메타 테스트 설계 결함 혼재 |

---

## 요약

| 구분 | 건수 | Severity |
|------|------|----------|
| **Open — 구현 (Boundary)** | 4 | Critical |
| **Open — 테스트 설계 (Scope 메타)** | 4 | Low |
| **Open — 커버리지/품질 목표** | 1 | Medium |
| **Resolved — 환경/구조** | 3 | — |

---

## Open 결함

### Boundary 구현 (AC-FR-01-01)

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | `ScreenBoundary.submit(grid=None)` 호출 (`tests/boundary_layer/…`, TC-A-01) | `FailureResult(code="INVALID_SIZE", message="Grid must be 4x4.")` 반환, `resolve` 0회 | `NotImplementedError: AC-FR-01-01: input validation not implemented` | `src/boundary/screen_boundary.py`에 입력 검증·조기 거부 미구현 (RED 스텁) | `grid is None` 분기 추가 후 `FailureResult` 반환, `resolve` 미호출 |
| DEF-002 | Critical | AC-FR-01-01 | `submit(grid=[])` 호출 (TC-A-05) | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | 동일 `NotImplementedError` | DEF-001과 동일 — 빈 리스트(0행) 차원 검증 누락 | `len(grid) != 4` 조기 거부 추가 |
| DEF-003 | Critical | AC-FR-01-01 | `submit(grid=[[]]*4)` 호출 | `INVALID_SIZE` 실패 객체 | 동일 `NotImplementedError` | DEF-001과 동일 — jagged(행 4·열 0) 검증 누락 | 각 행 `len(row) == 4` 검증 추가 |
| DEF-004 | Critical | AC-FR-01-01 | `submit(grid=[[0]*4 for _ in range(3)])` 호출 (3×4, TC-A-06) | `INVALID_SIZE` 실패 객체 | 동일 `NotImplementedError` | DEF-001과 동일 — 행 수 ≠ 4 검증 누락 | 4×4 차원 검증 함수 추출 후 선행 적용 |

> **영향 범위:** DEF-001~004는 동일 근본 원인으로 **기능 테스트 20건** 실패  
> (`TestNormalFailureReturn` 5, `TestBoundaryValues` 5, `TestDomainIsolation` 5, `TestMessageIdentity` 5)

### 테스트 설계 (Scope / 메타 검증)

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-005 | Low | AC-FR-01-01 | `pytest …::TestScopeRestriction::test_module_has_no_4x4_valid_grid_test_function` | 4×4 정상 시나리오 테스트 함수 없음 | `AssertionError`: `test_module_has_no_4x4_valid_grid_test_function` 이름에 `valid`·`4x4` 동시 포함 | 메타 테스트가 **자기 함수명**을 검사 대상에 포함 | AST 검사에서 `test_module_*` 제외 또는 함수명 변경 |
| DEF-006 | Low | AC-FR-01-01 | `pytest …::test_module_has_no_forbidden_ac_fr_01_02_to_05_test_names` | 소스에 `ac_fr_01_02`~`05` 문자열 없음 | `AssertionError`: 모듈 docstring·주석에 `AC-FR-01-02` 등 포함 | 전체 파일 raw `lower()` 검색으로 docstring 오탐 | 검사 대상을 `test_*` 함수명·`submit()` 호출부로 한정 |
| DEF-007 | Low | AC-FR-01-01 | `pytest …::test_module_has_no_fr_02_to_05_references_in_test_names` | 테스트 함수명에 `fr_02`~`fr_05` 없음 | `AssertionError`: `test_module_has_no_fr_02_to_05_…` 이름에 `fr_02` 포함 | 금지 문자열이 **검증 함수명**에 포함 | 함수명 변경 또는 exclude 리스트 적용 |
| DEF-008 | Low | AC-FR-01-01 | `pytest …::test_module_has_no_4x3_or_5x5_grid_literal_tests` | 소스에 `range(5)`·4×3 리터럴 없음 | `AssertionError`: docstring/주석·`FORBIDDEN_TEST_NAME_FRAGMENTS` 등에서 `range(5)` 등 매칭 | 전체 소스 문자열 검색의 false positive | AST 기반 리터럴만 검사하거나 exclude 패턴 적용 |

### 품질 목표

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-009 | Medium | AC-FR-01-01 | `pytest --cov=src --cov-report=term-missing` (RED 직후) | Boundary 검증 분기 실행·목표 85%+ (의미 있는 branch) | Line 92%이나 `submit()`은 `raise`만 실행, **검증 분기 0%** | GREEN 전 스텁만 존재 | DEF-001~004 수정 후 재측정; `screen_boundary` 검증 경로 커버 |

---

## Resolved 결함 (환경·구조 — 참고)

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-R01 | High | — | `pytest tests/boundary/…` (구 경로) | `from boundary.screen_boundary` 성공 | `ModuleNotFoundError: boundary.screen_boundary` | `tests/boundary/`가 `src/boundary/` 패키지명 shadowing | 테스트 디렉터리 → `tests/boundary_layer/` |
| DEF-R02 | High | — | `pytest` 전체 수집 | `entity.user` import 성공 | `ModuleNotFoundError: entity.user` | `entity/`가 `src/` 밖, `pythonpath=src`만 설정 | `entity/` → `src/entity/`, `tests/entity_layer/` |
| DEF-R03 | Medium | — | `pytest --cov=src --cov-report=html` | `htmlcov/index.html` 생성 | 수집 ERROR로 HTML 미생성 | DEF-R02로 수집 중단 | DEF-R02 해결 후 HTML 생성 확인 |

---

## 테스트 ↔ 결함 매핑

| 테스트 클래스 | 실패 수 | 관련 Open ID |
|---------------|---------|----------------|
| `TestNormalFailureReturn` | 5 | DEF-001 |
| `TestBoundaryValues` | 5 | DEF-002, DEF-003, DEF-004 |
| `TestDomainIsolation` | 5 | DEF-001 ~ DEF-004 |
| `TestMessageIdentity` | 5 | DEF-001 ~ DEF-004 |
| `TestScopeRestriction` | 4 | DEF-005 ~ DEF-008 |
| `TestScopeRestriction` (pass) | 1 | — (`test_module_docstring_declares_ac_fr_01_01_only`) |
| `tests/entity_layer/test_user.py` | 0 | — |

---

## 수정 우선순위 (QA 권장)

1. **P0:** DEF-001 ~ DEF-004 — `ScreenBoundary.submit()` GREEN (공통 `_validate_grid_size()` 추출 권장)
2. **P1:** DEF-005 ~ DEF-008 — 메타 테스트 정합성 (구현과 독립적으로 수정 가능)
3. **P2:** DEF-009 — GREEN 후 `pytest --cov=src --cov-report=html` 재실행, Boundary ≥ 85% 확인

---

## 회귀 확인 명령

```powershell
pytest tests/boundary_layer/ -v
pytest --cov=src --cov-report=term-missing --cov-report=html
```

**DoD:** Open 결함 0건, boundary_layer **25 passed**, README 결함 체크리스트 「모든 결함 수정 후 회귀 테스트 통과」 체크.

---

*본 문서는 RED 단계 스냅샷이며, GREEN 반영 시 상태·실제값·Resolved 테이블을 갱신한다.*
