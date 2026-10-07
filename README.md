# 🦿 Sim2Real Walking Robot Challenge

<p align="center">
  <img src="https://img.shields.io/badge/PseudoLab-S13-blue">
  <a href="https://discord.gg/pseudolab"><img src="https://img.shields.io/badge/Discord-PseudoLab-5865F2?logo=discord&logoColor=white"></a>
  <img src="https://img.shields.io/github/stars/Pseudo-Lab/Sim2Real-Walking-Robot?logo=github&label=Stars">
  <img src="https://img.shields.io/github/forks/Pseudo-Lab/Sim2Real-Walking-Robot?logo=github&label=Forks">
  <img src="https://img.shields.io/github/issues/Pseudo-Lab/Sim2Real-Walking-Robot?label=issues">
  <img src="https://img.shields.io/github/issues-pr/Pseudo-Lab/Sim2Real-Walking-Robot?label=pull%20requests">
  <img src="https://img.shields.io/github/contributors/Pseudo-Lab/Sim2Real-Walking-Robot">
  <img src="https://img.shields.io/github/license/Pseudo-Lab/Sim2Real-Walking-Robot?color=yellow">
</p>

> **We do not stop when the robot walks in simulation.  
> We measure what happens when it meets the real world.**

## 🚀 소개

**Sim2Real Walking Robot Challenge**는 저비용 오픈소스 이족보행 로봇을 이용하여  
시뮬레이션에서 학습한 locomotion policy가 실제 로봇에서 **얼마나, 왜 달라지는지 직접 측정하는 Physical AI 프로젝트**입니다.

MuJoCo에서 PPO 기반 보행 정책을 학습하고, 동일한 정책을 실제 로봇에 배포하여 Sim-to-Real gap을 측정합니다.

단순히 로봇을 걷게 만드는 데서 끝나지 않습니다.

> **Simulation → Learning → Real Robot → Failure → Measurement → Improvement**

성공한 실험뿐 아니라 넘어짐, 진동, 제자리걸음, 복귀 실패 같은 **실패도 데이터로 기록**합니다.

하드웨어가 없어도 Simulation Track만으로 프로젝트의 핵심 학습과 실험을 완주할 수 있습니다.

---

## 🗓️ Project Overview

| 항목 | 내용 |
|---|---|
| 기수 | 가짜연구소 13기 Open Academy |
| 활동 기간 | **2026.10.04 – 2027.01.09** |
| 구성 | 12주 Core + 2주 Buffer / Research Transition |
| 정기 모임 | 매주 **일요일 21:00–23:00** |
| 커뮤니케이션 | Pseudo-Lab Discord `#Room-GH` |
| Repository | `Pseudo-Lab/Sim2Real-Walking-Robot` |
| License | MIT |
| Core Robot | Open Duck Mini 계열 low-cost biped |
| Simulation | MuJoCo + `microduck_rl` |
| Robot Learning | PPO / LeRobot |
| Model & Data Sharing | GitHub + Hugging Face Hub |

---

# ✨ Why This Project?

Robot Learning의 대표적인 흐름 중 하나는

> **Learn in Simulation → Deploy to Reality**

입니다.

시뮬레이션에서는 대규모 병렬 환경을 이용해 빠르게 locomotion policy를 학습할 수 있습니다.

그러나 실제 로봇으로 옮기는 순간 문제가 달라집니다.

### 1. Hardware Gap

논문에 등장하는 로봇은 개인이나 입문자가 쉽게 접근하기 어려운 경우가 많습니다.

우리는 **low-cost open-source biped**를 이용하여 실제 Sim-to-Real 실험의 진입장벽을 낮춥니다.

### 2. Reality Gap

시뮬레이션과 현실은 같지 않습니다.

- mass / inertia mismatch
- servo delay
- torque saturation
- friction
- IMU noise
- encoder resolution
- battery voltage drop
- terrain variation

등이 실제 로봇의 동작을 바꿉니다.

그래서 이 프로젝트의 질문은 단순히

> **"Can the robot walk?"**

가 아닙니다.

우리가 묻는 것은

> **"Why does a policy that walks in simulation fail in reality?"**

입니다.

---

# 🎯 Research Questions

프로젝트 전체를 관통하는 핵심 질문입니다.

1. **Simulation success rate는 real-world success rate를 얼마나 예측하는가?**
2. **Domain Randomization의 범위를 넓힐수록 실물 성능도 계속 좋아지는가?**
3. **Actuator Modeling은 Domain Randomization과 비교해 Sim-to-Real gap을 얼마나 줄이는가?**
4. **Simulation에서는 성공하지만 real robot에서 실패하는 대표적인 failure mode는 무엇인가?**
5. **동일한 policy를 동일 조건에서 반복했을 때 결과는 얼마나 재현되는가?**
6. **Low-cost biped에서도 기존 Sim-to-Real 연구 결과를 재현할 수 있는가?**

Research Question은 프로젝트가 진행되면서 추가되거나 수정될 수 있습니다.

---

# 🎯 Goals

이번 시즌의 목표 결과물입니다.

1. **재현 가능한 보행 학습 파이프라인**  
   설치부터 policy training까지 README만 보고 재현

2. **공개 Policy Checkpoints**  
   조건별 policy + config + training curve

3. **4-way Controlled Comparison**  
   A/B/C/D 조건을 동일한 evaluation protocol로 비교

4. **Sim↔Real Gap Report**  
   동일 policy의 simulation / real robot 결과 비교

5. **Hardware DIY Guide**  
   3D printing → assembly → calibration → deployment

6. **Research Extension Foundation**  
   선행연구·코드·실험 로그·failure data를 축적하여 희망자의 후속 공동연구와 arXiv로 연결

> 완벽한 로봇보다 **재현 가능한 실험과 배울 수 있는 기록**을 남기는 것이 목표입니다.

---

# 🤖 What We Build

## Target Platforms

| 구분 | 내용 |
|---|---|
| Simulator | MuJoCo + `microduck_rl` |
| Main Biped | Open Duck Mini 계열 |
| Follow-up | Micro Duck MD-01 등 low-cost biped |
| Preliminary Robot Learning | SO-ARM101 + LeRobot |
| Algorithm | PPO |
| Policy / Dataset | Hugging Face Hub |
| Code / Experiments | GitHub |

SO-ARM101은 walking robot의 최종 대상이 아니라 **Robot Learning pipeline을 빠르게 이해하기 위한 선행 실습**입니다.

이를 통해

> **Teleoperate → Record → Train → Evaluate → Deploy**

흐름을 경험한 뒤 locomotion RL로 확장합니다.

---

# 🔬 Experimental Design

## Four Conditions

동일한 evaluation protocol을 사용하여 네 조건을 비교합니다.

| Condition | Description |
|---|---|
| **A. Baseline** | 기본 PPO + 기본 reward + randomization 없음 |
| **B. Reward Redesign** | energy / symmetry / foot placement 등 reward 개선 |
| **C. Domain Randomization** | mass / friction / delay / terrain randomization |
| **D. Actuator Modeling** | 실제 servo delay / torque 특성을 simulation에 반영 |

각 policy를

**Simulation → Real Robot**

순서로 동일하게 평가합니다.

따라서 기본 결과 구조는

> **4 Conditions × 2 Environments = 8 Experimental Cells**

입니다.

---

# 📐 Sim-to-Real Gap Coordinates

단순히 "잘 걸었다"라고 보고하지 않습니다.

모든 실험에 다음 조건을 기록합니다.

| Coordinate | Definition | Measurement |
|---|---|---|
| Terrain | 평지 / 경사 / 요철 | MuJoCo heightfield / real surface |
| Mass & Inertia | simulation 대비 실제 편차 | 실제 부품 측정 |
| Actuator Delay | command-response delay | servo step response |
| Torque Limit | saturation point | servo measurement |
| Friction | foot-ground friction | incline test |
| Observation Noise | IMU / encoder noise | stationary logging |
| Voltage Drop | battery state에 따른 변화 | runtime voltage logging |

이 좌표를 이용하여 단순 평균 성능이 아니라

> **어떤 현실 조건에서 policy가 무너지는가**

를 분석합니다.

---

# 📊 Evaluation Protocol

W4에서 다음 평가 protocol을 동결합니다.

1. **Straight Walking**
2. **Turning**
3. **Perturbation Recovery**
4. **Continuous Walking — 30 sec**

프로토콜 동결 이후에는 가능한 한 동일한 조건으로 모든 policy를 평가합니다.

---

# 📏 Metrics

| Category | Metric |
|---|---|
| Performance | success rate / velocity |
| Efficiency | Cost of Transport / torque integral |
| Stability | body roll/pitch RMS |
| Recovery | perturbation recovery time |
| Sim-to-Real | simulation success − real success |
| Robustness | perturbation condition별 success |
| Reproducibility | 동일 policy 반복실험 분산 |
| Training Cost | steps / wall-clock / GPU-hours |

### Repeated Trials

핵심 조건은 가능하면 **10회 반복 측정**합니다.

한 번 걷는 것과 **반복해서 걷는 것**은 다른 문제입니다.

> **Reproducibility itself is a result.**

---

# 💥 Failure Is Data

실패를 제거하지 않고 분류합니다.

예:

- Fall
- No Progress
- Oscillation
- Tracking Error
- Foot Slip
- Recovery Failure
- Actuator Saturation
- Observation Failure

> **Success is a result. Failure is also data.**

실물 실패 영상과 sensor / action log를 가능한 한 함께 보존합니다.

---

# 🧪 Real-world Perturbation Audit

실제 로봇에 통제된 perturbation을 가합니다.

| Perturbation | Example |
|---|---|
| External Force | 측면 외력 |
| Terrain | 5 / 10 / 15 mm obstacle |
| Payload | +50 / +100 g |
| Friction | mat / floor / acrylic |

이를 통해 단순 walking success가 아니라 **robustness와 recovery**를 비교합니다.

---

# 🧱 Resource Levels

모든 참가자가 동일한 하드웨어나 GPU를 가질 필요는 없습니다.

| Level | 내용 | 이번 기수 |
|---|---|---|
| **Level 1** | MuJoCo + PPO + A/B | Core |
| **Level 2** | C/D + parallel rollout + randomization | Core |
| **Level 3** | Real robot deployment + perturbation | Challenge |

하드웨어 조달이 늦어져도 simulation research는 계속 진행합니다.

---

# 🛟 Fallback Paths

| 상황 | 대체 경로 |
|---|---|
| Hardware 없음 | A–D Simulation comparison |
| Biped 조립 지연 | Simulation + servo-level characterization |
| Full walking 실패 | Standing / stepping / limited locomotion |
| GPU 부족 | randomization sweep 범위 축소 |
| Real deployment 실패 | failure analysis 자체를 결과로 기록 |

범위는 줄일 수 있지만 **실험의 뼈대는 유지**합니다.

---

# 📚 Learning & Research Flow

이 프로젝트는 정해진 논문을 발표하고 끝나는 스터디가 아닙니다.

우리가 지향하는 흐름은 다음과 같습니다.

> **Learn → Read → Question → Reproduce → Build → Simulate → Train → Deploy → Measure → Improve → Share**

논문도 같은 방식으로 사용합니다.

> **Seed Paper → Research Question → Related Papers → Authors / Labs → Code → Reproduction → Our Experiment**

---

# 🗺️ Weekly Roadmap

## Phase 1 — Foundations & Research Questions

### W1–W4 · Everyone Together

| Week | Date | Topic | Main Activities |
|---|---|---|---|
| **W1** | 10.04–10.10 | Kickoff | RL / Robot Learning / Sim-to-Real overview · MuJoCo setup · resource check |
| **W2** | 10.11–10.17 | PPO + Research Question | **Seed Paper 탐색 · 관심 Research Question 공유 · 관련 논문/연구실 탐색 · 기본 walking reproduction · Open Duck Mini 부품 주문** |
| **W3** | 10.18–10.24 | Parallel RL | locomotion training · reward curves · SO-ARM101 / LeRobot data workflow |
| **W4** | 10.25–10.31 | Reward & Experimental Design | evaluation protocol freeze · gap coordinates freeze · 3D printing · track selection |

### W4 Freeze Gate

W4 이후에는 핵심 evaluation protocol을 가능한 한 변경하지 않습니다.

---

# ⚙️ Phase 2 — Parallel Development

### W5–W8

| Week | Topic | Simulation / Policy | Reward / Randomization | Hardware / Deployment |
|---|---|---|---|---|
| **W5** | Motion Style | A 안정화 | reward ablation | assembly start |
| **W6** | Recent Research | B training | randomization sweep design | printing / wiring |
| **W7** | Domain Randomization | C training | DR comparison | assembly / URDF measurement |
| **W8** | Actuator Modeling | D training | C vs D analysis | servo calibration / delay / torque |

### Minimum Spine

W8까지 다음이 완료되면 실물이 없어도 프로젝트의 기본 연구 구조는 살아 있습니다.

> Environment  
> → PPO Baseline  
> → Frozen Evaluation  
> → A/B/C/D Simulation  
> → Controlled Comparison

---

# 🦿 Phase 3 — Real Robot & Sim-to-Real

### W9–W11

| Week | Topic | Main Activities |
|---|---|---|
| **W9** | First Real Deployment | real robot first run · condition A · failure logging |
| **W10** | Controlled Comparison | B/C/D deployment · repeated trials |
| **W11** | Sim↔Real Gap | final metrics · perturbation audit · failure taxonomy · result freeze |

W11에서 핵심 결과 수치를 동결합니다.

---

# 📦 Phase 4 — Open Source & Research Transition

### W12–W14

| Week | Date | Main Activities | Output |
|---|---|---|---|
| **W12** | 12.20–12.26 | final presentation · README · configs · evaluation code · demo · HF release | Public repository |
| **W13** | 12.27–01.02 | buffer / reproducibility test | Reproduction log |
| **W14** | 01.03–01.09 | **Core 결과 동결 · 공동연구팀 구성 · Publication Go/No-Go · Micro Duck 후속실험 설계** | **Core release · Research questions · extension team** |

---

# 🧭 Milestones

| # | Milestone | Due | Completion |
|---|---|---|---|
| **M1** | Environment & Research Question | 10.31 | setup · Seed Paper 탐색 · Research Question 초안 · evaluation freeze |
| **M2** | Simulation Policy | 11.14 | A/B policies · training curves · reward analysis |
| **M3** | Sim-to-Real Preparation | 12.05 | C/D · hardware assembly · actuator calibration |
| **M4** | Real Deployment & Gap Analysis | 12.19 | real deployment · repeated trials · failure taxonomy · result freeze |
| **M5** | Open Source & Research Transition | 01.09 | reproducibility · GitHub/HF release · Research Question 정리 · Publication Go/No-Go |

---

# 👥 Research Tracks

W1–W4는 공통으로 진행하고 이후 관심과 역량에 따라 트랙을 나눕니다.

### ① Learning / Policy

- PPO
- training
- policy evaluation
- reproducibility
- checkpoint management

### ② Sim-to-Real

- reward design
- domain randomization
- actuator modeling
- gap analysis
- experiment design

### ③ Robot / Deployment

- 3D printing
- assembly
- calibration
- real deployment
- perturbation experiments
- failure logging

트랙은 고정된 직책이 아닙니다.

필요하면 이동하고 서로의 실험을 함께 리뷰합니다.

---

# 🧭 Milestone Principles

일정이 압축되어도 다음은 가능하면 유지합니다.

| Item | Why |
|---|---|
| **W2 Hardware Order** | 실물 실험 일정 확보 |
| **W4 Evaluation Freeze** | 조건 간 공정한 비교 |
| **Baseline A** | C/D의 효과를 말하기 위한 기준 |
| **Repeated Trials** | 우연과 재현 가능한 성능을 구별 |
| **Failure Logs** | Sim-to-Real 원인 분석의 핵심 |

---

# 🔁 Research Extension

12주 Core의 목표는

> **재현 가능한 Sim-to-Real 실험 + 공개 저장소**

까지입니다.

그러나 연구 준비는 기수 종료 후 갑자기 시작하지 않습니다.

**2026년 10월부터** Seed Papers, 관련 연구, 연구실, 공개 코드 및 주요 venue를 탐색합니다.

> **Core Project → Open Source → Joint Research → arXiv → Research Community**

Core에서 의미 있고 재현 가능한 결과가 확보되면 W14에서 **Publication Go/No-Go**를 검토합니다.

희망자는 이후 공동연구팀으로 계속 참여합니다.

---

# 🔍 Research Preparation — Start Now

Seed Papers는 논문을 한 편씩 배정하기 위한 목록이 아닙니다.

Research Question을 찾기 위한 **starting points**입니다.

각 참가자는 관심 분야에서 다음 흐름을 탐색할 수 있습니다.

> **Seed Paper → Question → Related Papers → Authors → Lab → Code → Our Experiment**

관심 있는 연구를 발견하면 다음을 확인합니다.

- What problem did they solve?
- What robot did they use?
- What simulator?
- What assumptions?
- Is the code public?
- Can we reproduce it?
- What changes on a low-cost robot?
- What can we measure differently?

---

# 📖 Seed Papers & Research Directions

## A. Reinforcement Learning Foundations

대표 출발점:

- Schulman et al., **Proximal Policy Optimization Algorithms** (2017)

Questions:

- Why is PPO widely used for locomotion?
- How sensitive is locomotion to reward design?
- How large is seed-to-seed variance?

---

## B. Legged Locomotion & Sim-to-Real

Explore:

- Sim-to-Real locomotion
- Domain Randomization
- Actuator Modeling
- System Identification
- Robust Locomotion

Questions:

> Does more Domain Randomization always improve real-world performance?

> When does Actuator Modeling outperform broad randomization?

> What dominates the reality gap on low-cost servos?

---

## C. Parallel Robot Learning

Explore:

- parallel simulation
- GPU rollout
- scalable RL
- locomotion training

Question:

> Does faster training actually produce better real-world policies?

---

## D. Low-cost & Open-source Robotics

Explore:

- LeRobot
- Open Duck Mini
- Micro Duck
- open-source locomotion systems

Question:

> **How much modern Robot Learning can be reproduced on low-cost hardware?**

---

## E. Recent Research

프로젝트 기간 동안 다음 커뮤니티의 최신 연구를 지속적으로 살펴봅니다.

- ICRA
- CoRL
- RSS
- IEEE-RAS Humanoids
- related workshops

관심 키워드:

`Legged Locomotion` · `Humanoid` · `Sim-to-Real` ·  
`Domain Randomization` · `Actuator Modeling` ·  
`System Identification` · `Robust Control` ·  
`Failure Recovery` · `Physical AI` · `Robot Foundation Models`

특정 논문 목록은 고정하지 않습니다.

새로운 연구가 나오면 Seed Papers에 추가합니다.

---

# 🔎 Find Your Research Question

논문 한 편을 완벽하게 설명하는 것보다 **좋은 질문 하나를 발견하는 것**을 중요하게 봅니다.

예:

> Domain Randomization을 많이 적용할수록 항상 실물 성능이 좋아질까?

> 저가 servo의 delay를 정확히 모델링하면 randomization을 줄일 수 있을까?

> Simulation에서 성공하고 real robot에서 실패하는 조건을 자동 분류할 수 있을까?

> 같은 policy를 10회 실행했을 때 발생하는 분산 자체가 Sim-to-Real gap의 일부일까?

질문이 생기면 그 질문을 따라 새로운 논문을 찾아갑니다.

---

# 📝 My Research Interest

참가자는 `docs/literature/`에 자신의 연구 관심을 기록할 수 있습니다.

```text
Name / GitHub ID:

Research Topic:

Research Question:

Seed Paper:

Related Papers:

Interesting Authors / Labs:

Open-source Code:

What I want to reproduce:

What I want to test on our robot:
```

Research Question은 언제든 바뀔 수 있습니다.

---

# 🧪 From Paper to Experiment

논문 스터디의 결과가 슬라이드에서 끝나지 않도록 합니다.

> **Read → Question → Reproduce → Modify → Experiment → Measure → Share**

논문 결과가 재현되지 않아도 괜찮습니다.

재현 실패의 원인이

- environment
- dependency
- hardware
- actuator
- training setting
- undocumented assumption

중 무엇인지 기록하는 것 역시 의미 있는 결과입니다.

---

# 🚀 January 2027 — Joint Research Sprint

Core 결과가 충분하다면 **2027년 1월을 집중 공동연구 기간**으로 운영합니다.

참여는 선택 사항입니다.

| Period | Focus | Output |
|---|---|---|
| **01.01–01.09** | Core 결과 동결 · Publication Go/No-Go · team formation | Research Question / Contributions |
| **01.10–01.16** | missing experiments · repeated Sim/Real trials | Final experimental data |
| **01.17–01.23** | statistics · Sim↔Real gap · failure taxonomy · Related Work | Figures / Tables |
| **01.24–01.31** | joint writing · internal review · external feedback | **arXiv manuscript** |

연구 기여는 여러 형태가 가능합니다.

**RL / Reward / DR / Actuator Modeling / Hardware / Experiments / Data Analysis / Failure Analysis / Visualization / Literature / Writing**

공동저자 여부와 순서는 단순 참가 여부가 아니라 **실제 연구 기여를 바탕으로 공동연구팀에서 논의**합니다.

---

# 📄 February 2027 — arXiv Target

## 🎯 Target: February 2027 — arXiv Preprint

Tentative research direction:

> **Measuring and Reducing the Sim-to-Real Gap in Low-Cost Biped Locomotion**

가능한 contribution 후보:

1. **Low-cost Biped Sim-to-Real Evaluation Protocol**
2. **Baseline / Reward / Domain Randomization / Actuator Modeling Controlled Comparison**
3. **Quantitative Sim↔Real Gap Measurement**
4. **Real-world Failure-mode Analysis**
5. **Reproducible Open-source Code, Logs and Hardware Information**

다만 contribution을 미리 결론 내리지는 않습니다.

> **실험으로 확인된 결과만 research claim으로 발전시킵니다.**

---

# 🎓 Workshop & Conference Path

Workshop이나 Conference는 **2027년 2월이 되어서 처음 찾지 않습니다.**

프로젝트 초기부터 관련 연구와 venue를 함께 추적합니다.

관심 커뮤니티:

- ICRA
- CoRL
- RSS
- IEEE-RAS Humanoids
- Robot Learning / Sim-to-Real / Embodied AI / Physical AI Workshops

흐름은 다음과 같습니다.

> **Paper → Authors → Lab → Venue → CFP → Our Research**

2027년 2월 이후에는 그때의 실제 CFP와 연구 결과를 함께 검토하여 **주제·완성도·일정이 맞는 Workshop / Conference에 후속 투고**를 검토합니다.

arXiv가 끝이 아니라 다음 연구를 위한 출발점이 될 수 있습니다.

---

# 🌎 Global Research Exchange

관련 분야를 연구하는 국내외 교수·연구자·현업 전문가와 **Research Conversation**을 추진할 수 있습니다.

단순 초청 강연보다 다음 형태를 지향합니다.

> **Guest Research Talk → Our Progress → Research Questions → Discussion → Feedback**

우리도 연구자에게 질문합니다.

> *Is this a meaningful research question?*

> *What experiment are we missing?*

> *How should we measure the Sim-to-Real gap?*

> *What would make this result publishable?*

외부 연구자는 참여 정도에 따라

**Guest Researcher / Research Collaborator / Advisor**

형태로 연구 질문, 실험 설계, 결과 해석 또는 후속 공동연구에 참여할 수 있습니다.

---

# 🤖 From Paper to Research Community

논문을 읽었다면 저자와 연구실도 찾아봅니다.

> **Paper → Researcher → Lab → Community → Conversation → New Research Question**

국제 로봇 학회와 Workshop은 논문을 제출하는 장소인 동시에 **연구자를 직접 만나고 새로운 질문을 발견하는 장소**입니다.

ICRA 2027 서울 개최도 이러한 research-community experience의 기회로 활용하고자 합니다.

관심 논문의 연구자와 연구실을 미리 찾아보고, 관련 session / poster / workshop 등에 참여할 수 있습니다.

행사 이후에는 팀 내부 **Research Review / Teach-back**으로 배운 내용을 공유하고 후속 실험과 연결합니다.

---

# 🗓️ Research & Publication Roadmap

| Period | Stage | Target |
|---|---|---|
| **2026.10** | Seed Papers · literature / labs / venues 탐색 | Research Questions |
| **2026.11** | A/B/C/D Simulation experiments | Controlled comparison |
| **2026.12** | Real robot · repeated trials · failure analysis | Sim↔Real results |
| **2026.12 말** | Open-source release | Reproducible repository |
| **2027.01** | **Joint Research Sprint** | experiments + analysis + writing |
| **2027.02** | **arXiv target** | Public preprint |
| **2027.02 이후** | 당시 CFP + 연구 결과 검토 | Workshop / Conference challenge |
| **2027.05** | Research community participation | Research exchange / Teach-back |
| **Beyond** | Micro Duck · new research questions | Follow-up research / Season 2 |

---

# 👥 Team

## Core Team

| Role | Name | Focus |
|---|---|---|
| 🧭 Builder | @andrewJYjang | project coordination · experiment design · policy |
| 🦿 Runner | TBD | Learning / Policy |
| 🎯 Runner | TBD | Sim-to-Real |
| 🔧 Runner | TBD | Robot / Deployment |

실제 구성은 참여 상황과 W4 관심 조사에 따라 조정합니다.

중요한 것은 사람 수를 맞추는 것보다 **실험과 지식을 공유하여 특정 한 사람에게만 작업이 종속되지 않도록 하는 것**입니다.

---

# 🧑‍🤝‍🧑 How We Work

> **Explore → Question → Design → Build → Test → Measure → Improve → Share**

우리의 기본 원칙:

- 🧪 **작게 시작합니다.**
- ❓ **질문에서 실험을 시작합니다.**
- 📖 **성공과 실패를 모두 기록합니다.**
- 🔁 **재현 가능한 결과를 지향합니다.**
- 🤝 **서로의 실험을 리뷰합니다.**
- 🌱 **각자의 속도와 관심에 따라 깊이를 선택할 수 있습니다.**
- 🌍 **가능하면 결과를 Open Source로 공유합니다.**

이 프로젝트는 많은 시간을 투자하는 사람이 좋은 Runner라는 전제에서 출발하지 않습니다.

**꾸준히 질문하고, 실험하고, 기록하고, 공유하는 것**을 더 중요하게 봅니다.

---

# 🔗 GitHub Workflow

### Issues

```text
[WXX][track] Task
```

예:

```text
[W06][sim] Train condition B policy
```

### Branches

```text
wXX/track/short-description
```

### Pull Requests

관련 Issue를 연결합니다.

```text
Closes #NN
```

가능하면 최소 1인의 review 후 merge합니다.

### Labels

```text
week/W01 ... week/W14

track/learning
track/sim2real
track/robot

type/task
type/bug
type/question
type/docs

gate/freeze

good first issue
help wanted
```

---

# 📁 Repository Structure

```text
Sim2Real-Walking-Robot/
│
├── simulation/
│   ├── configs/
│   └── envs/
│
├── policies/
│
├── hardware/
│
├── perturb/
│
├── eval/
│
├── docs/
│   ├── literature/
│   └── weekly/
│
├── notebooks/
│
├── EVALUATION.md
├── HARDWARE.md
├── CONTRIBUTING.md
└── README.md
```

---

# ⚠️ Risks & Responses

| Risk | Response |
|---|---|
| Hardware delay | simulation track continues |
| Micro Duck availability | Open Duck Mini / available low-cost platform first |
| 3D printing delay | external printing or reduced hardware scope |
| GPU shortage | reduce sweep size |
| Servo variance | per-servo calibration |
| Robot damage | spare parts + safe test environment |
| Walking fails | standing / stepping / failure analysis |
| DR does not help | negative result reported |
| Real deployment fails | simulation + actuator characterization remains |
| Participant leaves | documentation + shared ownership |
| Schedule pressure | preserve core experiment, reduce optional challenges |

> **Negative result is not project failure.**

---

# 📚 Project Outputs

예상 결과물:

- 🧠 PPO policies
- 📊 A/B/C/D experiment results
- 📐 Sim-to-Real evaluation protocol
- 🦿 real robot deployment logs
- 💥 failure taxonomy
- 🔧 hardware / calibration guide
- 🤗 Hugging Face policies
- 💻 reproducible GitHub repository
- 🎥 demonstration videos
- 📄 optional joint research manuscript / arXiv

---

# 🌱 Beyond the Core

모든 참가자가 논문을 써야 하는 프로젝트는 아닙니다.

Core만 완주해도

> **Learn → Build → Simulate → Train → Deploy → Measure → Open Source**

라는 하나의 완결된 Robot Learning 경험을 갖게 됩니다.

더 깊이 연구하고 싶은 사람은

> **Research Question → Additional Experiments → Joint Research → arXiv → Workshop / Conference → Research Community**

로 이어갈 수 있습니다.

그리고 그 과정에서 또 다른 질문이 생기면 다음 프로젝트가 시작됩니다.

> **The goal is not just to make a robot walk.  
> The goal is to understand why it walks, why it fails, and what we can learn from both.**

---

# 🌱 How to Engage

기수 참가자가 아니더라도 공개 세션, Issue, Pull Request 등을 통해 참여할 수 있습니다.

특히 다음 기여를 환영합니다.

- reward function experiments
- new terrain / perturbation conditions
- actuator characterization
- reproducibility tests
- documentation
- literature / open-source implementation discovery

자세한 기여 방법은 `CONTRIBUTING.md`를 참고합니다.

---

# 🙏 Acknowledgement

이 프로젝트는 **Pseudo-Lab Open Academy**의 일부로 진행됩니다.

서로의 질문과 시행착오를 공개하고 함께 배우는 과정이  
Pseudo-Lab의 **Serendipity Revolution**으로 이어지기를 기대합니다.

Sim2Real-Walking-Robot is developed as part of Pseudo-Lab's open research community.

Special thanks to all contributors and to the open-source Robot Learning community.

---

# 📄 License

MIT License
