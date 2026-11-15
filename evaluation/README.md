# Evaluation — `s2rbench`

시뮬레이션과 실물 로봇을 **같은 로그 형식, 같은 지표 코드**로 평가하는 도구입니다.
프로젝트 README의 Evaluation Protocol · Metrics · Failure taxonomy · 4 Conditions × 2 Environments 표를 코드로 옮긴 것입니다.

```
에피소드 로그(.npz) ──▶ 지표 계산 ──▶ 성공 판정 ──▶ 실패 분류 ──▶ 보고서(report.md / results.json / report.png)
   sim · real 공통        metrics.py     protocol.yaml   failures.py     report.py
```

## 바로 해보기

```bash
pip install -r requirements.txt
python examples/demo/make_demo_logs.py --out runs_demo     # 가짜 데이터 320개 (보고서 모양 확인용)
python -m s2rbench validate runs_demo                 # 로그 형식 검사
python -m s2rbench report runs_demo -o report_demo    # 보고서 생성
pytest tests
```

결과 견본: [`examples/demo/sample_report/`](examples/demo/sample_report/report.md) (가짜 데이터)

## Open Duck Mini로 돌려보기 (현재 주 플랫폼)

공개된 학습 완료 정책으로 네 과제를 바로 돌릴 수 있습니다. 직접 학습한 정책은 `--onnx` 와 `--condition`(A~D)만 바꾸면 됩니다.

```bash
git clone https://github.com/apirrone/Open_Duck_Playground ../../Open_Duck_Playground
# 정책 파일: https://github.com/apirrone/Open_Duck_Mini 의 BEST_WALK_ONNX_2.onnx
python examples/openduck/run_benchmark.py --playground ../../Open_Duck_Playground \
    --onnx BEST_WALK_ONNX_2.onnx --condition A --out runs/openduck/sim
python -m s2rbench report runs/openduck -o report
```

외란 수준별 강건성은 힘을 바꿔 가며 돌리면 됩니다.

```bash
for f in 5 10 15 20; do
  python examples/openduck/run_benchmark.py --playground ../../Open_Duck_Playground --onnx BEST_WALK_ONNX_2.onnx \
      --tasks push_recovery --push-n $f --condition push_${f}N --out runs_push/sim
done
python -m s2rbench report runs_push -o report_push
```

공개 정책으로 실제 돌린 결과: [`examples/openduck/baseline.md`](examples/openduck/baseline.md)

실물 Open Duck Mini에서는 런타임의 제어 루프에 `Recorder` 를 넣어 같은 형식으로 남기고 `runs/real/` 에 두면, 보고서가 시뮬과 실물을 나란히 비교합니다.

### MicroDuck (로봇 수령 후)

`examples/microduck/stand_push.py` 는 MicroDuck 모델을 세워 놓고 미는 예제로 남겨 두었습니다. 로봇이 도착하면 Open Duck과 같은 방식의 실행기를 추가합니다.

## 로봇을 추가할 때

로봇마다 달라지는 것은 `examples/<로봇>/` 안에만 둡니다. `s2rbench/` 와 `protocol.yaml` 은 모든 로봇이 함께 씁니다.

```
examples/
├── openduck/    run_benchmark.py · baseline.md
├── microduck/   stand_push.py
└── demo/        make_demo_logs.py · sample_report/   (가짜 데이터)
```

새 로봇은 `examples/<로봇>/run_benchmark.py` 하나를 추가하고, 로그의 meta에 `robot="<로봇>"` 을 적으면 됩니다.
로그도 `runs/<로봇>/sim`, `runs/<로봇>/real` 로 나눠 두세요. 한 폴더에 여러 로봇이 섞여 있으면 보고서가 멈추고 `--robot` 으로 하나를 고르라고 알려 줍니다.

## 로그 남기기

제어 주기마다 `step()` 한 번, 끝나면 `finish()`. 시뮬레이션이든 실물이든 같습니다.

```python
from s2rbench import Recorder

rec = Recorder(env="real", condition="C", task="straight", policy_id="c_v3", trial=4,
               mass_kg=0.74, torque_limit=0.6, control_hz=50)
for ...:                                    # 제어 루프
    rec.step(t=t, base_rpy=rpy, cmd_vel=cmd, joint_torque=tau, joint_vel=qd, action=a)
rec.finish(termination="timeout",           # 넘어졌으면 "fall"
           measured_distance_m=1.32).save("runs/real/C_straight_04.npz")
```

MuJoCo에서는 `MujocoProbe` 가 필요한 값을 한 번에 뽑아 줍니다 (`s2rbench/mujoco_recorder.py`).

| 배열 | 모양 | 필수 | 없으면 |
|---|---|---|---|
| `t`, `base_rpy` | (T,), (T,3) | 필수 | — |
| `cmd_vel` | (T,3) | 권장 | 진행률 계산 불가 |
| `base_pos` | (T,3) | 선택 | meta의 `measured_distance_m`(줄자 실측)로 대체 |
| `joint_torque`, `joint_vel` | (T,J) | 선택 | CoT · 토크 적분 · 포화 판정이 빈칸 |
| `action` | (T,J) | 선택 | action rate가 빈칸 |
| `foot_contact`, `foot_pos` | (T,2), (T,2,3) | 선택 | 발 미끄러짐 판정이 빈칸 |
| `perturb` | (T,) | 외란 과제에서 필수 | 복구 시간이 빈칸 |
| `obs_valid`, `battery_v` | (T,) | 선택 | — |

meta 필수 항목: `env`(sim/real), `condition`(A~D), `task`, `policy_id`, `trial`.
Gap Coordinates(바닥 재질, 추가 하중, 배터리 전압 등)는 meta에 자유롭게 적으면 `results.json` 까지 따라갑니다.

값이 없는 지표는 추정하지 않고 NaN으로 둡니다.

## 무엇을 계산하나

| README 항목 | 계산 방법 | 위치 |
|---|---|---|
| Success rate | `protocol.yaml` 기준 통과 비율, Wilson 95% 구간 | `protocol.py`, `report.py` |
| Velocity | 명령 방향 이동 거리 ÷ 시간, 진행률(실제 ÷ 명령) | `metrics.py` |
| Cost of Transport | Σ\|τ·ω\|Δt ÷ (m·g·거리) | `metrics.py` |
| Torque integral | Σ\|τ\|Δt | `metrics.py` |
| Roll / pitch RMS | IMU 자세의 RMS | `metrics.py` |
| Recovery time | 외란 종료 후 기울기가 ±5° 안에 1초 머물 때까지 | `metrics.py` |
| Sim-to-Real gap | 시뮬 성공률 − 실물 성공률, 부트스트랩 95% 구간 | `report.py` |
| Robustness | `condition` 을 외란 수준으로 두면 수준별 성공률 표 | `report.py` |
| Reproducibility | 같은 칸의 반복 시행이 다수 결과와 일치하는 비율 | `report.py` |
| Failure taxonomy | 규칙 기반 자동 분류 8종 | `failures.py` |

보고서에 추가로 들어가는 두 가지:

- **Retention = 실물 성공률 ÷ 시뮬 성공률.** 시뮬에서 되던 것이 실물에 얼마나 남았는지를 한 숫자로 봅니다. 시뮬 성공률이 20% 미만이면 비워 둡니다(전이를 논할 수 없는 정책).
- **Sim-predicts-real.** 조건 × 과제 칸마다 시뮬 성공률과 실물 성공률의 순위 상관(Spearman). 연구 질문 1번 "시뮬 성공률이 실물 성공률을 얼마나 예측하는가"에 대한 직접 측정입니다.

성공률은 과제별로 먼저 구한 뒤 평균합니다. 시행 수가 많은 과제가 결과를 끌고 가지 않게 하기 위해서입니다.

## 팀이 정해야 할 것

1. **`protocol.yaml` 의 숫자.** 지금 값은 초안입니다(직진은 명령 거리의 60% 이상, 외란 복구 3초 이내 등). 명령 대비 비율로 정의해 로봇이 달라도 같은 파일을 쓸 수 있게 했습니다. 확정하면 `version` 을 올리고 이후로는 바꾸지 않습니다.
2. **실물의 위치 측정 방법.** 추적 장비가 없으면 줄자 실측값을 meta에 넣는 방식으로 충분히 돌아갑니다.
3. **실패 분류 임계값.** `protocol.yaml` 의 `failure` 항목. 실물 영상과 대조해 조정이 필요합니다.

## 한계

- 실물 로봇 로그로는 아직 검증하지 못했습니다. 단위 시험, 가짜 데이터, MuJoCo의 Open Duck Mini(공개 보행 정책)와 MicroDuck 모델(서 있기 + 밀기)까지 확인했습니다.
- `openduck/run_benchmark.py` 는 시행마다 바닥 마찰(0.7~1.0배)과 초기 관절 각도만 조금 바꿉니다. 조건이 좁아서 시뮬 반복 간 편차가 실물보다 작게 나옵니다.
- `microduck/stand_push.py` 는 보행 정책이 아니라 단순 위치 서보로 서 있는 로봇을 미는 예제입니다. 학습 때 쓰는 BAM 액추에이터 모델도 넣지 않았습니다.
- 토크는 시뮬에서는 액추에이터 힘, 실물에서는 전류 추정값이라 CoT를 시뮬과 실물 사이에 직접 비교할 때는 주의가 필요합니다.
