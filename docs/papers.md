# 📚 Paper Study

Sim2Real Walking Robot Challenge에서 함께 공부할
Robot Learning / Reinforcement Learning / Sim2Real 관련 논문 목록입니다.

목표는 논문을 단순히 요약하는 것이 아니라,

**Paper → Idea → Code → Experiment → Robot**

으로 연결하는 것입니다.

---

## 1. Proximal Policy Optimization Algorithms
**Schulman et al., 2017**

PPO(Proximal Policy Optimization)의 기본 논문.
현재 로봇 locomotion 강화학습에서 가장 널리 사용되는
알고리즘 중 하나이다.

### 우리가 볼 것
- PPO는 어떻게 동작하는가?
- 왜 locomotion에서 PPO를 많이 사용하는가?
- 우리 walking policy의 baseline으로 어떻게 사용할 수 있는가?

Paper:
https://arxiv.org/abs/1707.06347

---

## 2. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning
**Rudin et al., CoRL 2022**

수많은 simulation environment를 병렬 실행하여
보행 정책을 매우 빠르게 학습하는 방법을 보여준다.

### 우리가 볼 것
- Parallel RL이 왜 중요한가?
- 많은 robot simulation을 동시에 돌리면 무엇이 달라지는가?
- MuJoCo / Isaac Lab에서 비슷한 실험을 할 수 있는가?

Paper:
https://proceedings.mlr.press/v164/rudin22a.html

---

## 3. RMA: Rapid Motor Adaptation for Legged Robots
**Kumar et al., RSS 2021**

로봇이 실제 환경에서 마찰, 지형, payload 등의 변화에
빠르게 적응하도록 하는 방법을 연구한다.

### 우리가 볼 것
- Simulation과 Real Robot의 차이를 어떻게 다루는가?
- Domain Randomization은 어떻게 사용되는가?
- 우리 Sim2Real gap 측정에 적용할 수 있는가?

Paper:
https://roboticsproceedings.org/rss17/p011.html

---

## 4. DreamWaQ
**Learning Robust Quadrupedal Locomotion With Implicit Terrain Imagination**
**ICRA 2023**

제한된 센서 정보만으로도 로봇이 다양한 지형에서
안정적으로 이동하도록 학습하는 연구이다.

### 우리가 볼 것
- Observation은 무엇인가?
- IMU와 joint state만으로 무엇을 알 수 있는가?
- 저가형 walking robot에도 적용 가능한가?

Paper:
https://arxiv.org/abs/2301.10602

---

## 5. Extreme Parkour with Legged Robots
**ICRA 2024**

강화학습과 perception을 결합하여 로봇이
복잡한 장애물과 지형을 통과하도록 만든 연구이다.

### 우리가 볼 것
- Terrain information을 policy가 어떻게 사용하는가?
- Robust locomotion이란 무엇인가?
- 단순 walking 이후 어떤 방향으로 확장할 수 있는가?

Project:
https://extreme-parkour.github.io/

---

## 6. Learning Agile Soccer Skills for a Bipedal Robot with Deep Reinforcement Learning
**Science Robotics, 2024**

소형 2족 로봇에게 강화학습을 이용하여
걷기, 방향전환, 공 다루기 등의 동작을 학습시킨 연구이다.

### 우리가 볼 것
- Biped locomotion을 어떻게 학습하는가?
- Reward는 어떻게 설계했는가?
- Simulation에서 배운 동작을 실제 robot으로 어떻게 옮겼는가?

---

## 7. Berkeley Humanoid Lite
**2025**

3D printing과 비교적 쉽게 구할 수 있는 부품을 이용해
저비용 humanoid research platform을 구축한 연구이다.

### 우리가 볼 것
- 저비용 robot을 어떻게 설계했는가?
- 3D printed robot에서도 Sim2Real이 가능한가?
- 우리가 더 단순한 6-DOF biped를 만들 수 있는가?

Paper:
https://arxiv.org/abs/2504.17249

---

## 8. ASAP
**Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills**
**2025**

Simulation의 물리 특성과 실제 로봇의 움직임 차이를
실제 데이터를 이용하여 줄이는 접근을 다룬다.

### 우리가 볼 것
- Reality Gap은 어디에서 발생하는가?
- Actuator modeling은 왜 중요한가?
- Domain Randomization과 어떤 차이가 있는가?

Paper:
https://arxiv.org/abs/2502.01143

---

## 9. Humanoid Locomotion as Next Token Prediction
**2024**

로봇의 locomotion을 전통적인 RL 문제뿐 아니라
sequence prediction 관점에서도 바라보는 연구이다.

### 우리가 볼 것
- Robot motion을 token처럼 예측한다는 것은 무엇인가?
- Transformer와 locomotion을 어떻게 연결하는가?
- 향후 Robot Foundation Model과 어떤 관계가 있는가?

Paper:
https://arxiv.org/abs/2402.19469

---

# Study Method

9명의 참여자가 우선 한 편씩 선택합니다.

각자 다음 네 가지를 중심으로 5~10분 정도 공유합니다.

1. 이 논문이 해결하려는 문제
2. 핵심 아이디어
3. 가장 흥미로운 실험 결과
4. 우리 Walking Robot 프로젝트에 적용할 수 있는 한 가지

가능하면 논문의 GitHub code도 함께 확인합니다.
