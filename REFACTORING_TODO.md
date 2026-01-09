# Refactoring TODO

Internal code cleanup while preserving all external API contracts.

## Constraints
- **No API changes** - All request/response schemas remain identical
- **No endpoint changes** - All routes stay the same
- **No breaking changes** - Frontend integration unaffected

---

## 1. User Management Consolidation (High Priority)

**Problem**: 4 overlapping user systems
- `app/routers/users.py` (7KB) - Legacy user selection
- `app/routers/user_switching.py` (11KB) - New switching API
- `app/routers/user_management.py` (11KB) - DB-backed management
- `app/data/mock_users.py` (9KB) - Mock data

**Action**:
- [ ] Merge into single `app/routers/users.py`
- [ ] Consolidate services into `app/services/user_service.py`
- [ ] Remove `user_switching.py`, `user_management.py` after merge
- [ ] Keep models: `user_profile.py`, `user_switching.py`, `user_management.py` (merge if overlapping)

---

## 2. Translation System Removal (High Priority)

**Problem**: Unused translation infrastructure (~25KB)

**Files to remove**:
- [ ] `app/middleware/translation_middleware.py`
- [ ] `app/middleware/translation.py`
- [ ] `app/middleware/translations/` (entire folder)
- [ ] `app/services/translation_precompute_service.py`
- [ ] `app/storage/translation_database.py`
- [ ] `app/utils/translation.py`
- [ ] `app/utils/translation_helpers.py`
- [ ] `app/utils/db_translation.py`

**Action**:
- [ ] Remove translation middleware from `main.py`
- [ ] Remove translation imports from routers
- [ ] Delete all translation files

---

## 3. Main.py Cleanup (High Priority)

**Problem**: `main.py` is 1348 lines with embedded mock data

**Action**:
- [ ] Extract mock data to `app/data/mock_data.py`
- [ ] Keep `main.py` to ~100-150 lines (app setup, routers, middleware)
- [ ] Move health/biomarker mock endpoints to appropriate routers

---

## 4. Service Layer Consolidation (Medium Priority)

**Problem**: Duplicate user services
- `app/services/user_context.py` (31KB)
- `app/services/user_service.py` (7KB)
- `app/services/user_db_service.py` (4KB)
- `app/services/user_data_manager.py` (11KB)
- `app/services/user_health_generator.py` (8KB)

**Action**:
- [ ] Audit each service for actual usage
- [ ] Merge overlapping functionality
- [ ] Target: 2-3 user service files max

---

## 5. Database Config Consolidation (Low Priority)

**Problem**: Multiple database configs
- `app/database.py`
- `app/config/database.py`
- `app/storage/database.py`

**Action**:
- [ ] Keep `app/database.py` as single source
- [ ] Merge or remove `app/config/database.py`
- [ ] `app/storage/database.py` is storage layer - keep separate

---

## 6. Model Cleanup (Low Priority)

**Problem**: Potentially overlapping models
- `app/models/user_profile.py`
- `app/models/user_switching.py`
- `app/models/user_management.py`

**Action**:
- [ ] Audit for duplicate Pydantic models
- [ ] Consolidate into single `user_models.py` if significant overlap

---

## 7. Unused Imports & Dead Code (Low Priority)

**Action**:
- [ ] Run `ruff check --select=F401` for unused imports
- [ ] Remove dead code paths
- [ ] Clean up `__pycache__` folders

---

## Execution Order

1. Translation removal (isolated, low risk)
2. Main.py mock data extraction
3. User router consolidation
4. Service layer cleanup
5. Database/model cleanup
6. Final import cleanup

---

## Validation

After each phase:
- [ ] All existing tests pass
- [ ] Manual API smoke test
- [ ] No import errors on startup
