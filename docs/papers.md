# 📚 Paper Study — Robot Learning & Sim2Real

## Goal

논문을 단순히 읽고 요약하는 것이 아니라,

**Paper → Question → Code → Experiment → Robot**

으로 연결하는 것을 목표로 합니다.

아래 논문은 참여자에게 배정된 논문이 아니라,
연구 주제를 탐색하기 위한 **Seed Papers**입니다.

각 참여자는 Seed Papers를 참고하여 관심 있는 연구 질문을 정하고,
관련 논문을 추가로 탐색하여 자신의 연구 논문을 선정합니다.

---

## 🌱 Seed Papers

| # | Topic | Paper | Research Question |
|---|---|---|---|
| 1 | RL | **Proximal Policy Optimization Algorithms** (2017) | 왜 locomotion에서 PPO를 많이 사용하는가? |
| 2 | Parallel RL | **Learning to Walk in Minutes** (CoRL 2022) | 병렬 simulation은 보행 학습을 얼마나 빠르게 하는가? |
| 3 | Sim2Real | **Rapid Motor Adaptation (RMA)** (RSS 2021) | 실제 환경 변화에 어떻게 빠르게 적응하는가? |
| 4 | Robust Locomotion | **DreamWaQ** (ICRA 2023) | 제한된 센서만으로 안정적인 보행이 가능한가? |
| 5 | Terrain | **Extreme Parkour with Legged Robots** (ICRA 2024) | perception과 RL을 어떻게 결합하는가? |
| 6 | Biped RL | **Learning Agile Soccer Skills for a Bipedal Robot** (2024) | 2족 로봇의 Sim2Real은 어떻게 이루어지는가? |
| 7 | Low-cost Robot | **Berkeley Humanoid Lite** (2025) | 저비용·3D printed robot에서도 Sim2Real이 가능한가? |
| 8 | Physics Gap | **ASAP** (2025) | simulation과 실제 physics의 차이를 어떻게 줄이는가? |
| 9 | Foundation Model | **Humanoid Locomotion as Next Token Prediction** (2024) | locomotion을 sequence prediction으로 볼 수 있는가? |

---

## 🔎 Find Your Research Question

예를 들어:

**Low-cost Biped**

Berkeley Humanoid Lite  
→ 더 단순한 biped는 가능한가?  
→ 4 / 6 / 8 DOF 비교  
→ 관련 논문 탐색  
→ MuJoCo 실험  
→ 실제 robot

또는:

**Sim2Real**

RMA / ASAP  
→ Reality Gap의 가장 큰 원인은 무엇인가?  
→ Domain Randomization  
→ Actuator Modeling  
→ 실제 robot 비교

Seed Paper와 최종적으로 연구할 논문은 **같을 필요가 없습니다.**

---

## 🧑‍🔬 My Research Interest

각 참여자는 다음 내용을 정리합니다.

**Topic**

관심 있는 Robot Learning / Walking Robot 주제

**Research Question**

> 내가 정말 궁금한 것은 무엇인가?

**Candidate Papers**

1.
2.
3.

**Selected Paper**

아직 미정이어도 됩니다.

**Why?**

왜 이 문제를 연구하고 싶은가?

---

## 🗣️ Sharing

선정한 논문을 중심으로 짧게 공유합니다.

1. 이 논문이 해결하려는 문제
2. 핵심 아이디어
3. 가장 흥미로운 실험
4. 우리 프로젝트에 적용할 수 있는 아이디어

가능하면 논문의 **Code / GitHub / Simulation**도 함께 확인합니다.

---

## 🚀 From Paper to Robot

최종 목표는 논문 발표 자체가 아닙니다.

**Read → Question → Code → Reproduce → Experiment → Sim2Real**

좋은 아이디어는 GitHub Issue와 실험으로 연결합니다.
