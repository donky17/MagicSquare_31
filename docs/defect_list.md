# MagicSquare_xx — 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 ID | DL-AC-FR-01-01 |
| 기준 AC | AC-FR-01-01 (FR-01 입력 검증, PRD §8.1 `INVALID_SIZE`) |
| 테스트 계획 | [test_plan.md](./test_plan.md) |
| 최종 실행 | `pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v` (2026-05-29) |
| 실행 결과 | **25 passed** (25 collected) |
| 상태 | **GREEN 완료** — Open 결함 0건 |

---

## 요약

| 구분 | 건수 | Severity |
|------|------|----------|
| **Open — 구현 (Boundary)** | 0 | — |
| **Open — 테스트 설계 (Scope 메타)** | 0 | — |
| **Open — 커버리지/품질 목표** | 0 | — |
| **Resolved** | 12 | — |

---

## Open 결함

*없음 (GREEN DoD 충족)*

---

## Resolved 결함

### Boundary 구현 (AC-FR-01-01)

| ID | Severity | AC ID | 수정 요약 | 해결 커밋 |
|----|----------|-------|-----------|----------|
| DEF-001 | Critical | AC-FR-01-01 | `grid is None` → `FailureResult(INVALID_SIZE)` | 커밋 1 |
| DEF-002 | Critical | AC-FR-01-01 | `len(grid) != GRID_SIZE` 조기 거부 (`[]`) | 커밋 2-A |
| DEF-003 | Critical | AC-FR-01-01 | `any(len(row) != GRID_SIZE)` jagged 거부 | 커밋 2-A |
| DEF-004 | Critical | AC-FR-01-01 | `len(grid) != GRID_SIZE` 3×4 거부 | 커밋 2-A |

### 테스트 설계 (Scope / 메타 검증)

| ID | Severity | AC ID | 수정 요약 | 해결 커밋 |
|----|----------|-------|-----------|----------|
| DEF-005 | Low | AC-FR-01-01 | `_functional_test_function_names()` — 메타 클래스 제외 | 커밋 2-B |
| DEF-006 | Low | AC-FR-01-01 | 기능 테스트 함수명만 `ac_fr_01_02`~`05` 검사 | 커밋 2-B |
| DEF-007 | Low | AC-FR-01-01 | 기능 테스트 함수명만 `fr_02`~`05` 검사 | 커밋 2-B |
| DEF-008 | Low | AC-FR-01-01 | `_functional_test_source()` — 기능 테스트 소스만 검사 | 커밋 2-B |

### 품질 목표

| ID | Severity | AC ID | 수정 요약 | 해결 커밋 |
|----|----------|-------|-----------|----------|
| DEF-009 | Medium | AC-FR-01-01 | `screen_boundary.py` 검증 분기 93% 커버 확인 | 커밋 2-C |

### 환경·구조 (참고)

| ID | Severity | 수정 요약 |
|----|----------|-----------|
| DEF-R01 | High | `tests/boundary/` + `conftest.py` src 우선 — shadowing 해소 |
| DEF-R02 | High | `entity/` → `src/entity/` |
| DEF-R03 | Medium | DEF-R02 해결 후 HTML 커버리지 생성 확인 |

---

## 테스트 ↔ 결함 매핑 (GREEN)

| 테스트 클래스 | 통과 | 관련 Resolved ID |
|---------------|------|------------------|
| `TestNormalFailureReturn` | 5 | DEF-001 |
| `TestBoundaryValues` | 5 | DEF-002 ~ DEF-004 |
| `TestDomainIsolation` | 5 | DEF-001 ~ DEF-004 |
| `TestMessageIdentity` | 5 | DEF-001 ~ DEF-004 |
| `TestScopeRestriction` | 5 | DEF-005 ~ DEF-008 |

---

## 회귀 확인 명령

```powershell
pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py -v
pytest tests/boundary/test_grid_input_validation_ac_fr_01_01.py --cov=src --cov-report=term-missing
```

**DoD:** Open 결함 0건, **25 passed**, README·defect_list GREEN 체크리스트 완료.

---

*본 문서는 AC-FR-01-01 GREEN 완료 스냅샷이다.*
