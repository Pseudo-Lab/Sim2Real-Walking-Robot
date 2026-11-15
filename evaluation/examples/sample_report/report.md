> 이 보고서는 `make_demo_logs.py` 가 만든 **가짜 데이터**로 생성한 견본입니다. 실험 결과가 아닙니다.

# Sim-to-Real benchmark report

Protocol `0.1-draft` · 320 episodes · 95% intervals (bootstrap over trials)

## Conditions × environments

| Condition | Sim success | Real success | Gap (sim − real) | Retention (real ÷ sim) |
|---|---|---|---|---|
| A | 72% [60%, 85%] | 20% [8%, 32%] | +52 pp [+35, +70] | 0.28 [0.12, 0.46] |
| B | 75% [62%, 88%] | 32% [20%, 45%] | +42 pp [+25, +60] | 0.43 [0.26, 0.63] |
| C | 88% [78%, 95%] | 78% [65%, 90%] | +10 pp [-5, +25] | 0.89 [0.72, 1.06] |
| D | 75% [62%, 88%] | 60% [45%, 73%] | +15 pp [-5, +33] | 0.80 [0.59, 1.07] |

Success is macro-averaged over tasks. Retention is left blank when sim success is below 20%.

## Does simulation predict reality?

Spearman rank correlation between sim and real success over 16 condition × task cells: **+0.35**

## Reproducibility

Share of trials that agree with the majority outcome of their cell (1.00 = every repeat ends the same way).

- sim: 0.78
- real: 0.76

## Failure taxonomy

| Failure | Sim | Real |
|---|---|---|
| recovery_failure | 8 | 17 |
| fall | 13 | 11 |
| actuator_saturation | 0 | 12 |
| foot_slip | 0 | 18 |
| oscillation | 4 | 13 |
| no_progress | 3 | 6 |
| tracking_error | 8 | 7 |

## Per task

| Condition | Env | Task | n | Success | 95% CI | Consistency |
|---|---|---|---|---|---|---|
| A | real | endurance | 10 | 40% | 17%–69% | 0.60 |
| A | real | push_recovery | 10 | 30% | 11%–60% | 0.70 |
| A | real | straight | 10 | 0% | 0%–28% | 1.00 |
| A | real | turn | 10 | 10% | 2%–40% | 0.90 |
| A | sim | endurance | 10 | 70% | 40%–89% | 0.70 |
| A | sim | push_recovery | 10 | 90% | 60%–98% | 0.90 |
| A | sim | straight | 10 | 70% | 40%–89% | 0.70 |
| A | sim | turn | 10 | 60% | 31%–83% | 0.60 |
| B | real | endurance | 10 | 70% | 40%–89% | 0.70 |
| B | real | push_recovery | 10 | 30% | 11%–60% | 0.70 |
| B | real | straight | 10 | 10% | 2%–40% | 0.90 |
| B | real | turn | 10 | 20% | 6%–51% | 0.80 |
| B | sim | endurance | 10 | 70% | 40%–89% | 0.70 |
| B | sim | push_recovery | 10 | 90% | 60%–98% | 0.90 |
| B | sim | straight | 10 | 70% | 40%–89% | 0.70 |
| B | sim | turn | 10 | 70% | 40%–89% | 0.70 |
| C | real | endurance | 10 | 70% | 40%–89% | 0.70 |
| C | real | push_recovery | 10 | 80% | 49%–94% | 0.80 |
| C | real | straight | 10 | 70% | 40%–89% | 0.70 |
| C | real | turn | 10 | 90% | 60%–98% | 0.90 |
| C | sim | endurance | 10 | 90% | 60%–98% | 0.90 |
| C | sim | push_recovery | 10 | 60% | 31%–83% | 0.60 |
| C | sim | straight | 10 | 100% | 72%–100% | 1.00 |
| C | sim | turn | 10 | 100% | 72%–100% | 1.00 |
| D | real | endurance | 10 | 60% | 31%–83% | 0.60 |
| D | real | push_recovery | 10 | 90% | 60%–98% | 0.90 |
| D | real | straight | 10 | 30% | 11%–60% | 0.70 |
| D | real | turn | 10 | 60% | 31%–83% | 0.60 |
| D | sim | endurance | 10 | 70% | 40%–89% | 0.70 |
| D | sim | push_recovery | 10 | 80% | 49%–94% | 0.80 |
| D | sim | straight | 10 | 80% | 49%–94% | 0.80 |
| D | sim | turn | 10 | 70% | 40%–89% | 0.70 |
