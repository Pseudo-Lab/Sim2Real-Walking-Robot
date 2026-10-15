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

## 🚀 Introduction

**Sim2Real Walking Robot Challenge** is a Physical AI project using low-cost open-source biped robots to
directly measure **how and why locomotion policies trained in simulation behave differently on real robots**.

We train PPO-based locomotion policies in MuJoCo, deploy the same policies to real robots, and measure the Sim-to-Real gap.

Our goal is not simply to make the robot walk.

> **Simulation → Learning → Real Robot → Failure → Measurement → Improvement**

We record not only successful experiments but also **failures as data**, including falls, oscillation, no-progress behavior, and recovery failures.

Even without hardware, participants can complete the project's core learning and experiments through the Simulation Track. The research we begin here can continue well beyond 2027 and 2030, growing as experienced researchers and practitioners join when their circumstances allow. What can robots do well, and what remains difficult for them? What about walking robots? Walking is only one small part of what robots can do, but for humanoids, locomotion has a very different impact. That is why we started here. We hope this project will grow into deeper and better research over many years, supported by capable researchers who are watching, encouraging, and contributing to the work.

---

## 🗓️ Project Overview

| Item | Details |
|---|---|
| Cohort | Pseudo-Lab Open Academy, Season 13 |
| Project Period | **2026.10.04 – 2027.01.09** |
| Structure | 12-week Core + 2-week Buffer / Research Transition |
| Regular Meeting | Every **Sunday, 20:30–22:30** |
| Communication | Pseudo-Lab Discord `#Room-GH` |
| Repository | `Pseudo-Lab/Sim2Real-Walking-Robot` |
| License | MIT |
| Core Robot | Open Duck Mini family of low-cost bipeds |
| Simulation | MuJoCo + `microduck_rl` |
| Robot Learning | PPO / LeRobot |
| Model & Data Sharing | GitHub + Hugging Face Hub |

---

# ✨ Why This Project?

One of the representative workflows in Robot Learning is

> **Learn in Simulation → Deploy to Reality**

.

In simulation, we can use massively parallel environments to train locomotion policies quickly.

But the problem changes the moment we move to a real robot.

### 1. Hardware Gap

Robots used in research papers are often difficult for individuals and beginners to access.

We use a **low-cost open-source biped** to lower the barrier to real Sim-to-Real experimentation.

### 2. Reality Gap

Simulation and reality are not the same.

- mass / inertia mismatch
- servo delay
- torque saturation
- friction
- IMU noise
- encoder resolution
- battery voltage drop
- terrain variation

These factors can significantly change the behavior of a real robot.

So the question of this project is not simply

> **"Can the robot walk?"**

.

What we ask instead is

> **"Why does a policy that walks in simulation fail in reality?"**

.

---

# 🎯 Research Questions

These are the core questions that guide the entire project.

1. **How well does simulation success rate predict real-world success rate?**
2. **Does expanding the range of Domain Randomization always improve real-world performance?**
3. **How much can Actuator Modeling reduce the Sim-to-Real gap compared with Domain Randomization?**
4. **What are the representative failure modes that succeed in simulation but fail on a real robot?**
5. **How reproducible are the results when the same policy is repeated under the same conditions?**
6. **Can existing Sim-to-Real research findings be reproduced on a low-cost biped?**

Research Questions may be added or revised as the project progresses.

---

# 🎯 Goals

The target outputs for this season are:

1. **Reproducible Locomotion Training Pipeline**  
   Reproduce the full process from installation to policy training using only the README

2. **Public Policy Checkpoints**  
   Policy + config + training curve for each condition

3. **4-way Controlled Comparison**  
   Compare A/B/C/D under the same evaluation protocol

4. **Sim↔Real Gap Report**  
   Compare simulation and real-robot results for the same policy

5. **Hardware DIY Guide**  
   3D printing → assembly → calibration → deployment

6. **Research Extension Foundation**  
   Build a shared base of prior work, code, experiment logs, and failure data that can support follow-up joint research and an arXiv submission

> The goal is to leave behind **reproducible experiments and records that others can learn from**, rather than merely a perfect robot. Research roles should therefore be assigned early, with participants moving the work forward actively.

---

# 🤖 What We Build

## Target Platforms

| Category | Details |
|---|---|
| Simulator | MuJoCo + `microduck_rl` |
| Main Biped | Open Duck Mini family |
| Follow-up | Low-cost bipeds such as Micro Duck MD-01 |
| Preliminary Robot Learning | SO-ARM101 + LeRobot |
| Algorithm | PPO |
| Policy / Dataset | Hugging Face Hub |
| Code / Experiments | GitHub |

SO-ARM101 is not the final walking-robot target. It is a **preliminary exercise for quickly understanding the Robot Learning pipeline**.

Through this, we first experience the flow

> **Teleoperate → Record → Train → Evaluate → Deploy**

and then expand to locomotion RL.

---

# 🔬 Experimental Design

## Four Conditions

We compare four conditions using the same evaluation protocol.

| Condition | Description |
|---|---|
| **A. Baseline** | Basic PPO + basic reward + no randomization |
| **B. Reward Redesign** | Improve rewards such as energy / symmetry / foot placement |
| **C. Domain Randomization** | mass / friction / delay / terrain randomization |
| **D. Actuator Modeling** | Reflect real servo delay / torque characteristics in simulation |

Each policy is evaluated in the same order:

**Simulation → Real Robot**

using the same evaluation procedure.

Therefore, the basic result structure is

> **4 Conditions × 2 Environments = 8 Experimental Cells**

.

---

# 📐 Sim-to-Real Gap Coordinates

We do not report results simply as "it walked well."

For every experiment, we record the following conditions.

| Coordinate | Definition | Measurement |
|---|---|---|
| Terrain | flat / slope / uneven surface | MuJoCo heightfield / real surface |
| Mass & Inertia | deviation between simulation and reality | physical component measurement |
| Actuator Delay | command-response delay | servo step response |
| Torque Limit | saturation point | servo measurement |
| Friction | foot-ground friction | incline test |
| Observation Noise | IMU / encoder noise | stationary logging |
| Voltage Drop | variation with battery state | runtime voltage logging |

Using these coordinates, we analyze more than average performance. We ask

> **Under which real-world conditions does the policy break down?**

and analyze the answer.

---

# 📊 Evaluation Protocol

At W4, we freeze the following evaluation protocol.

1. **Straight Walking**
2. **Turning**
3. **Perturbation Recovery**
4. **Continuous Walking — 30 sec**

After the protocol is frozen, all policies are evaluated under the same conditions as much as possible.

---

# 📏 Metrics

| Category | Metric |
|---|---|
| Performance | success rate / velocity |
| Efficiency | Cost of Transport / torque integral |
| Stability | body roll/pitch RMS |
| Recovery | perturbation recovery time |
| Sim-to-Real | simulation success − real success |
| Robustness | success by perturbation condition |
| Reproducibility | variance across repeated runs of the same policy |
| Training Cost | steps / wall-clock / GPU-hours |

### Repeated Trials

For key conditions, we aim for **10 repeated trials whenever possible**.

Walking once and **walking repeatedly** are different problems.

> **Reproducibility itself is a result.**

---

# 💥 Failure Is Data

We classify failures instead of removing them.

Examples:

- Fall
- No Progress
- Oscillation
- Tracking Error
- Foot Slip
- Recovery Failure
- Actuator Saturation
- Observation Failure

> **Success is a result. Failure is also data.**

Whenever possible, we preserve real-world failure videos together with sensor / action logs.

---

# 🧪 Real-world Perturbation Audit

We apply controlled perturbations to the real robot.

| Perturbation | Example |
|---|---|
| External Force | lateral force |
| Terrain | 5 / 10 / 15 mm obstacle |
| Payload | +50 / +100 g |
| Friction | mat / floor / acrylic |

This allows us to compare **robustness and recovery**, not just walking success.

---

# 🧱 Resource Levels

Participants do not all need the same hardware or GPU resources.

| Level | Description | This Cohort |
|---|---|---|
| **Level 1** | MuJoCo + PPO + A/B | Core |
| **Level 2** | C/D + parallel rollout + randomization | Core |
| **Level 3** | Real robot deployment + perturbation | Challenge |

Simulation research continues even if hardware procurement is delayed.

---

# 🛟 Fallback Paths

| Situation | Fallback Path |
|---|---|
| No hardware | A–D Simulation comparison |
| Biped assembly delayed | Simulation + servo-level characterization |
| Full walking fails | Standing / stepping / limited locomotion |
| Limited GPU | Reduce randomization sweep range |
| Real deployment fails | Treat failure analysis itself as a result |

The scope may shrink, but **the experimental spine remains intact**.

---

# 📚 Learning & Research Flow

This project is not a paper-reading study that ends with a scheduled presentation.

We follow this research flow:

> **Learn → Read → Question → Reproduce → Build → Simulate → Train → Deploy → Measure → Improve → Share**

We use papers in the same way.

> **Seed Paper → Research Question → Related Papers → Authors / Labs → Code → Reproduction → Our Experiment**

---

# 🗺️ Weekly Roadmap

## Phase 1 — Foundations & Research Questions

### W1–W4 · Everyone Together

| Week | Date | Topic | Main Activities |
|---|---|---|---|
| **W1** | 10.04–10.10 | Kickoff | RL / Robot Learning / Sim-to-Real overview · MuJoCo setup · resource check |
| **W2** | 10.11–10.17 | PPO + Research Question | **Explore Seed Papers · share research interests and Research Questions · explore related papers/labs · reproduce basic walking · order Open Duck Mini parts** |
| **W3** | 10.18–10.24 | Parallel RL | locomotion training · reward curves · SO-ARM101 / LeRobot data workflow |
| **W4** | 10.25–10.31 | Reward & Experimental Design | evaluation protocol freeze · gap coordinates freeze · 3D printing · track selection |

### W4 Freeze Gate

After W4, we avoid changing the core evaluation protocol whenever possible.

---

# ⚙️ Phase 2 — Parallel Development

### W5–W8

| Week | Topic | Simulation / Policy | Reward / Randomization | Hardware / Deployment |
|---|---|---|---|---|
| **W5** | Motion Style | Stabilize A | reward ablation | assembly start |
| **W6** | Recent Research | B training | randomization sweep design | printing / wiring |
| **W7** | Domain Randomization | C training | DR comparison | assembly / URDF measurement |
| **W8** | Actuator Modeling | D training | C vs D analysis | servo calibration / delay / torque |

### Minimum Spine

If the following are completed by W8, the core research structure remains viable even without a physical robot.

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

At W11, we freeze the core quantitative results.

---

# 📦 Phase 4 — Open Source & Research Transition

### W12–W14

| Week | Date | Main Activities | Output |
|---|---|---|---|
| **W12** | 12.20–12.26 | final presentation · README · configs · evaluation code · demo · HF release | Public repository |
| **W13** | 12.27–01.02 | buffer / reproducibility test | Reproduction log |
| **W14** | 01.03–01.09 | **Freeze Core results · form joint research team · Publication Go/No-Go · design follow-up Micro Duck experiments** | **Core release · Research Questions · extension team** |

---

# 🧭 Milestones

| # | Milestone | Due | Completion |
|---|---|---|---|
| **M1** | Environment & Research Question | 10.31 | setup · Seed Paper exploration · draft Research Question · evaluation freeze |
| **M2** | Simulation Policy | 11.14 | A/B policies · training curves · reward analysis |
| **M3** | Sim-to-Real Preparation | 12.05 | C/D · hardware assembly · actuator calibration |
| **M4** | Real Deployment & Gap Analysis | 12.19 | real deployment · repeated trials · failure taxonomy · result freeze |
| **M5** | Open Source & Research Transition | 01.09 | reproducibility · GitHub/HF release · Research Question consolidation · Publication Go/No-Go |

---

# 👥 Research Tracks

Everyone works together in W1–W4; afterward, participants split into tracks according to interest and capability.

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

Tracks are not fixed job assignments.

Participants can move between tracks when needed and review one another's experiments.

---

# 🧭 Milestone Principles

Even if the schedule becomes compressed, we try to preserve the following:

| Item | Why |
|---|---|
| **W2 Hardware Order** | Secure enough time for real-world experiments |
| **W4 Evaluation Freeze** | Ensure fair comparison across conditions |
| **Baseline A** | Provide the reference needed to evaluate C/D |
| **Repeated Trials** | Separate chance outcomes from reproducible performance |
| **Failure Logs** | Essential for analyzing causes of the Sim-to-Real gap |

---

# 🔁 Research Extension

The goal of the 12-week Core is

> **Reproducible Sim-to-Real experiments + a public repository**

.

But research preparation does not suddenly begin after the cohort ends.

Starting in **October 2026**, we explore Seed Papers, related research, labs, public code, and major venues.

> **Core Project → Open Source → Joint Research → arXiv → Research Community**

If the Core produces meaningful and reproducible results, we review a **Publication Go/No-Go** decision at W14.

Interested participants may continue afterward as a joint research team.

---

# 🔍 Research Preparation — Start Now

Seed Papers are not a list of papers assigned one per person.

They are **starting points** for discovering Research Questions.

Each participant can explore the following flow within their area of interest.

> **Seed Paper → Question → Related Papers → Authors → Lab → Code → Our Experiment**

When you find research that interests you, check the following:

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

Representative starting point:

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

Throughout the project, we continuously review recent work from the following communities.

- ICRA
- CoRL
- RSS
- IEEE-RAS Humanoids
- related workshops

Keywords of interest:

`Legged Locomotion` · `Humanoid` · `Sim-to-Real` ·  
`Domain Randomization` · `Actuator Modeling` ·  
`System Identification` · `Robust Control` ·  
`Failure Recovery` · `Physical AI` · `Robot Foundation Models`

We do not fix a permanent list of papers.

As new research appears, we add it to the Seed Papers.

---

# 🔎 Find Your Research Question

We value **discovering one good question** more than perfectly explaining a single paper.

Examples:

> Does applying more Domain Randomization always improve real-world performance?

> If we model delay in low-cost servos accurately, can we reduce the amount of randomization needed?

> Can we automatically classify conditions where a policy succeeds in simulation but fails on a real robot?

> Is the variance observed across 10 runs of the same policy itself part of the Sim-to-Real gap?

When a question emerges, we follow it to find new papers.

---

# 📝 My Research Interest

Participants can record their research interests in `docs/literature/`.

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

Research Questions may change at any time.

---

# 🧪 From Paper to Experiment

Paper study should not end with slides.

> **Read → Question → Reproduce → Modify → Experiment → Measure → Share**

It is okay if a paper's results cannot be reproduced.

Possible causes of failed reproduction include

- environment
- dependency
- hardware
- actuator
- training setting
- undocumented assumption

Recording which of these caused the failure is itself a meaningful result.

---

# 🚀 January 2027 — Joint Research Sprint

If the Core results are strong enough, **January 2027 will be an intensive joint-research period**.

Participation is optional.

| Period | Focus | Output |
|---|---|---|
| **01.01–01.09** | Freeze Core results · Publication Go/No-Go · team formation | Research Question / Contributions |
| **01.10–01.16** | missing experiments · repeated Sim/Real trials | Final experimental data |
| **01.17–01.23** | statistics · Sim↔Real gap · failure taxonomy · Related Work | Figures / Tables |
| **01.24–01.31** | joint writing · internal review · external feedback | **arXiv manuscript** |

Research contributions can take many forms.

**RL / Reward / DR / Actuator Modeling / Hardware / Experiments / Data Analysis / Failure Analysis / Visualization / Literature / Writing**

Co-authorship and author order will be discussed by the joint research team based on **actual research contributions**, not mere participation.

---

# 📄 February 2027 — arXiv Target

## 🎯 Target: February 2027 — arXiv Preprint

Tentative research direction:

> **Measuring and Reducing the Sim-to-Real Gap in Low-Cost Biped Locomotion**

Possible contribution candidates:

1. **Low-cost Biped Sim-to-Real Evaluation Protocol**
2. **Baseline / Reward / Domain Randomization / Actuator Modeling Controlled Comparison**
3. **Quantitative Sim↔Real Gap Measurement**
4. **Real-world Failure-mode Analysis**
5. **Reproducible Open-source Code, Logs and Hardware Information**

However, we do not decide the contributions in advance.

> **Only findings supported by experiments will be developed into research claims.**

---

# 🎓 Workshop & Conference Path

We do not wait until **February 2027** to start looking for Workshops or Conferences.

From the beginning of the project, we track relevant research and venues together.

Communities of interest:

- ICRA
- CoRL
- RSS
- IEEE-RAS Humanoids
- Robot Learning / Sim-to-Real / Embodied AI / Physical AI Workshops

The flow is:

> **Paper → Authors → Lab → Venue → CFP → Our Research**

After February 2027, we will review the actual CFPs available at that time together with our research results and consider follow-up submission to a **Workshop / Conference that fits the topic, maturity, and schedule**.

arXiv can be a starting point for the next stage of research, not the end.

---

# 🌎 Global Research Exchange

We may initiate **Research Conversations** with domestic and international professors, researchers, and industry experts working in related fields.

Rather than one-way invited talks, we aim for the following format:

> **Guest Research Talk → Our Progress → Research Questions → Discussion → Feedback**

We also ask researchers questions.

> *Is this a meaningful research question?*

> *What experiment are we missing?*

> *How should we measure the Sim-to-Real gap?*

> *What would make this result publishable?*

Depending on their level of involvement, external researchers may participate as

**Guest Researcher / Research Collaborator / Advisor**

and contribute to research questions, experimental design, result interpretation, or follow-up joint research.

---

# 🤖 From Paper to Research Community

When we read a paper, we also explore its authors and labs.

> **Paper → Researcher → Lab → Community → Conversation → New Research Question**

International robotics conferences and Workshops are not only places to submit papers; they are also **places to meet researchers directly and discover new questions**.

We plan to use ICRA 2027 in Seoul as an opportunity for this research-community experience.

We can identify researchers and labs behind papers of interest in advance and participate in relevant sessions / posters / workshops.

After each event, we share what we learned through an internal **Research Review / Teach-back** and connect it to follow-up experiments.

---

# 🗓️ Research & Publication Roadmap

| Period | Stage | Target |
|---|---|---|
| **2026.10** | Explore Seed Papers · literature / labs / venues | Research Questions |
| **2026.11** | A/B/C/D Simulation experiments | Controlled comparison |
| **2026.12** | Real robot · repeated trials · failure analysis | Sim↔Real results |
| **Late 2026.12** | Open-source release | Reproducible repository |
| **2027.01** | **Joint Research Sprint** | experiments + analysis + writing |
| **2027.02** | **arXiv target** | Public preprint |
| **After 2027.02** | Review current CFPs + research results | Workshop / Conference challenge |
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

The actual team structure will be adjusted based on participation and the W4 interest survey.

More important than filling a fixed number of roles is **sharing experiments and knowledge so the work does not depend on a single person**.

---

# 🧑‍🤝‍🧑 How We Work

> **Explore → Question → Design → Build → Test → Measure → Improve → Share**

Our operating principles:

- 🧪 **Start small.**
- ❓ **Start experiments from questions.**
- 📖 **Record both success and failure.**
- 🔁 **Aim for reproducible results.**
- 🤝 **Review one another's experiments.**
- 🌱 **Choose your depth according to your own pace and interests.**
- 🌍 **Share results as Open Source whenever possible.**

This project does not assume that the person who spends the most time is the best Runner.

We value **consistently asking, experimenting, documenting, and sharing** more.

---

# 🔗 GitHub Workflow

### Issues

```text
[WXX][track] Task
```

Example:

```text
[W06][sim] Train condition B policy
```

### Branches

```text
wXX/track/short-description
```

### Pull Requests

Link the relevant Issue.

```text
Closes #NN
```

Whenever possible, merge after review by at least one person.

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

Expected outputs:

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

Not every participant is required to write a paper.

Completing the Core alone provides

> **Learn → Build → Simulate → Train → Deploy → Measure → Open Source**

a complete Robot Learning experience.

Participants who want to go deeper can continue with

> **Research Question → Additional Experiments → Joint Research → arXiv → Workshop / Conference → Research Community**

.

And when another question emerges during that process, the next project begins.

> **The goal is not just to make a robot walk.  
> The goal is to understand why it walks, why it fails, and what we can learn from both.**

---

# 🌱 How to Engage

Even people outside the cohort can participate through public sessions, Issues, and Pull Requests.

We especially welcome contributions in:

- reward function experiments
- new terrain / perturbation conditions
- actuator characterization
- reproducibility tests
- documentation
- literature / open-source implementation discovery

See `CONTRIBUTING.md` for detailed contribution guidelines.

---

# 🙏 Acknowledgement

This project is conducted as part of the **Pseudo-Lab Open Academy**.

We hope that openly sharing our questions and trial-and-error while learning together
will contribute to Pseudo-Lab's **Serendipity Revolution**.

Sim2Real-Walking-Robot is developed as part of Pseudo-Lab's open research community.

Special thanks to all contributors and to the open-source Robot Learning community.

---

# 📄 License

MIT License
