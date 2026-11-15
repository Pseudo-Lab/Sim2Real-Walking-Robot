# Open Duck Mini v2 — 공개 정책 기준선 (시뮬레이션)

정책 `BEST_WALK_ONNX_2.onnx`, 장면 `scene_flat_terrain_backlash.xml`, 과제당 10회, 2026-11-16 실행. 실물 결과는 아직 없습니다.

## 네 과제 (외란 과제는 4 N)

| Condition | Env | Task | n | Success | 95% CI | Consistency |
|---|---|---|---|---|---|---|
| A | sim | endurance | 10 | 100% | 72%–100% | 1.00 |
| A | sim | push_recovery | 10 | 100% | 72%–100% | 1.00 |
| A | sim | straight | 10 | 100% | 72%–100% | 1.00 |
| A | sim | turn | 10 | 100% | 72%–100% | 1.00 |

## 옆으로 밀기 (0.1초)

| Condition | Env | Task | n | Success | 95% CI | Consistency |
|---|---|---|---|---|---|---|
| push_5N | sim | push_recovery | 10 | 100% | 72%–100% | 1.00 |
| push_10N | sim | push_recovery | 10 | 60% | 31%–83% | 0.60 |
| push_15N | sim | push_recovery | 10 | 0% | 0%–28% | 1.00 |
| push_20N | sim | push_recovery | 10 | 0% | 0%–28% | 1.00 |
| push_25N | sim | push_recovery | 10 | 0% | 0%–28% | 1.00 |
| push_30N | sim | push_recovery | 10 | 0% | 0%–28% | 1.00 |
