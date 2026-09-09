# INFO 5356 — Lab 1: Introduction to Reachy Mini

## Course Info
- Course: INFO 5356-030 Introduction to Human-Robot Interaction
- Term: Fall 2026
- Assignment: Lab 1 — Introduction to Reachy Mini

## Team Members
- Yifan Luo yl4389
- Jiaxin Shen js3996

## Project Overview
This repository contains our team's work for Lab 1, which introduces the Reachy Mini
platform. The lab covers installing Reachy Mini Control, running community applications
in MuJoCo simulation, building a custom Reachy Mini application (`team_greeting_app`),
and investigating failure modes through systematic testing.

## Repository Structure
```text
├── README.md
├── .gitignore
├── apps/
│   └── team_greeting_app/ # 4.3 Create a Reachy Mini application 
└── report/                # all the Deliverables
```

# INFO 5356 — Lab 1: Introduction to Reachy Mini

## Course Info
- Course: INFO 5356-030 Introduction to Human-Robot Interaction
- Term: Fall 2026
- Assignment: Lab 1 — Introduction to Reachy Mini

## Team Members
- Yifan Luo yl4389
- Jiaxin Shen js3996

## Project Overview
This repository contains our team's work for Lab 1, which introduces the Reachy Mini
platform. The lab covers installing Reachy Mini Control, running community applications
in MuJoCo simulation, building a custom Reachy Mini application (`team_greeting_app`),
and investigating failure modes through systematic testing.

## Repository Structure
```text
├── README.md
├── .gitignore
├── apps/
│   └── team_greeting_app/ # 4.3 Create a Reachy Mini application
└── report/                # all the Deliverables
```

---

## Part 1: Create a Team GitHub Repository

**Deliverables (3 points):**
- Team repository with complete structure, well-documented README, `.gitignore`, reproducible instructions, and team commit history.
- The final repository contains no credentials, placeholder submission text, unrelated files, or broken run instructions.

---

## Part 2: Install Reachy Mini Control

### Installation Record

- Operating System / Architecture: Windows 11 64-bit
- Reachy Mini Control version: Wireless, App v0.9.34, Daemon v1.10.0
- Installation process: Followed the official installation steps as outlined in the
  lab handout. Downloaded the Windows installer from the Reachy Mini website and
  ran the on-screen setup.
- Issue encountered: The installation got stuck for an extended period during the
  Python environment setup step ("Setting up Python environment...").
- Resolution: Restarted the application, after which the installation completed
  successfully. No further issues were encountered.

### Additional Observations

- Robot demeanor during initial interaction: curiosity, shy
- Controller: some controller inputs did not register movement — noticeable input lag or no response

### Deliverables (2 points)

- Screenshot showing Reachy Mini Control connected to Simulation Beta with the MuJoCo window visible: *(insert screenshot)*
- Screenshot showing the selected application running, with its name and author recorded below: *(insert screenshot)*
  - Application name: *Reachy Phone Home (`reachy_phone_home`)*
  - Author: *itsMarco-G*

---

## Part 3: Run an App in Simulation Mode

### 3.1 One-Sentence Prediction

> **Prediction Statement:**
> "When the user steps out of the camera's field of view, the system processes a missing target input, decides that communication with 'home' has failed, and outputs a sad head-droop with slow, flattened antenna lowers alongside a static disconnect audio cue."

**Application tested:** Reachy Phone Home (`reachy_phone_home`), author itsMarco-G — https://huggingface.co/spaces/itsMarco-G/reachy_phone_home

### 3.2 Observe One Complete Interaction — Analysis

#### Notes Summary & Interaction Comparison
- **Expected Interaction**: The application was predicted to detect smartphone usage dynamically via computer vision (CV) and immediately trigger noticeable auditory and kinematic feedback when the user holds or puts away their phone.
- **Observed User Action & Divergence**:
  - **Limited CV Sensitivity**: The object detection model lacked high-level sensitivity — it could not differentiate subtle intermediate phone poses or discern active phone usage. The system only registered state changes when the phone was held completely vertical (in use) or laid entirely flat (away).
  - **Missing Auditory Feedback**: The application provided no audio cues to notify the user when the phone was detected or released.
  - **Visibility & Visual Attention Clash**: When users were actively looking down at or using their phones, they missed the robot's visual movement interactions entirely. Without audio cues or large-scale physical gestures, the feedback loop broke because user attention was directed away from the simulated viewport.

#### What the Simulator Represents Well
- **Kinematic Smoothness**: MuJoCo accurately and smoothly renders Reachy Mini's multi-axis joint movements (head pitch/yaw and antenna articulation) once a detection state is triggered.
- **State Machine Consistency**: Discrete transitions between detecting states (`PHONE_IN_USE` vs. `PHONE_AWAY`) execute predictably without frame drops or software locks in simulation.
- **Pose Legibility**: Pre-configured poses and motion amplitudes are visually clean and clearly defined in the 3D rendering environment.

#### What the Simulator Cannot Establish
- **Real-World CV & Lighting Inconsistencies**: The simulation environment cannot account for real-world computer vision challenges such as variable ambient lighting, camera motion blur, partial occlusions, or awkward user angles that reduce CV model accuracy.
- **Multimodal Feedback & Audio Cues**: The digital environment cannot convey missing acoustic feedback or spatial audio cues that are essential for drawing a distracted user's attention back to the robot.
- **Attentional & Cognitive HRI Dynamics**: Software viewports cannot evaluate human visual focus or user distraction. In real-world HRI, a visual-only interaction fails if the user's primary visual attention is occupied by a secondary screen.

### 3.3 Teleoperation in Simulation Mode

*(fill in: describe teleoperating at least 2 expressive channels — e.g. head, body yaw, antennas — making small movements, observing pose, and returning to neutral; compare smooth vs. faster direct control)*

### Deliverables (3 points)

- Short clip showing the selected community app completing one interaction in simulation: *(insert clip)*
- Screenshot showing teleoperation of at least two expressive channels with the robot returned to neutral:(Curious)<img width="602" height="416" alt="image" src="https://github.com/user-attachments/assets/d788b9f0-31e2-4428-a2f8-dd6f55878c6e" /> (shy)<img width="611" height="429" alt="image" src="https://github.com/user-attachments/assets/85c5c909-3558-4aed-bf8b-50941f09774a" />
- Detailed observation describing the robot's intended interaction, the user's actual response, the robot's resulting behavior, and two limits for evaluating HRI: *(see 3.2 above — confirm this covers "two limits" explicitly, or add a short closing paragraph naming them)*

---

## Part 4: Create and Run an App in Simulation — `team_greeting_app`

### 4.2 Workspace Setup

| Item | Value |
|---|---|
| Operating system / architecture | macOS (arm64) / Windows via WSL2, Ubuntu 26.04.1 LTS (x86_64) |
| Python version | 3.12.14 |
| Reachy Mini SDK version | 1.10.0 |
| MuJoCo version | 3.3.0 |

### 4.3 Application Overview

`team_greeting_app` implements a three-stage "wake-up greeting" behavior:

1. **Orient** — head turns toward an implied user (yaw rotation)
2. **Greet** — head nods while antennas swing, repeating until `GREETING_DURATION_S` elapses
3. **Neutral** — head and antennas return to rest position

#### Requirements checklist

| Requirement | Status | Where in code |
|---|---|---|
| Extends `ReachyMiniApp`, implements `run(reachy_mini, stop_event)` | ✅ | `class TeamGreetingApp(ReachyMiniApp)`, `run()` |
| Coordinates ≥2 expressive channels | ✅ | head (yaw + pitch) and antennas |
| Three stages: orient → greet → neutral | ✅ | `_stage_orient`, `_stage_greet`, `_stage_neutral` |
| Checks `stop_event` during loops/waits, stops gracefully | ✅ | checked before/after each `goto_target` call in `_stage_greet`, plus `finally` block always returns to neutral |
| Timestamped markers per stage | ✅ | `_log()` prints `[{time.time():.2f}] STAGE: {stage}` |
| ≥2 named motion/timing parameters, documented units | ✅ | 6 parameters, all in degrees or seconds (see below) |
| No camera, microphone, cloud AI, personal data collection | ✅ | none used |

#### Named parameters (documented units)

| Parameter | Unit | Description |
|---|---|---|
| `ORIENT_HEAD_YAW_DEG` | degrees | head yaw angle during orient stage |
| `ORIENT_DURATION_S` | seconds | duration of orient motion |
| `GREETING_DURATION_S` | seconds | total duration of greeting behavior |
| `HEAD_TILT_DEG` | degrees | head nod amplitude during greeting |
| `ANTENNA_SWING_DEG` | degrees | antenna swing amplitude during greeting |
| `RETURN_DURATION_S` | seconds | duration of return-to-neutral motion |

### 4.4 MuJoCo Simulation Test

Tested using two terminals with `reachy_mini_env` activated in both:
- Terminal 1: `reachy-mini-daemon --sim` (simulator/daemon)
- Terminal 2: `python main.py` → `Ctrl-C` to request stop

| Check | Result |
|---|---|
| All three behavioral stages visible | ✅ / ❌ *(fill in)* |
| Application exits cleanly | ✅ / ❌ *(fill in)* |
| No control loop remains running after stop | ✅ / ❌ *(fill in)* |
| Simulated robot returns to neutral | ✅ / ❌ *(fill in)* |
| Timestamped log markers match observed stages | ✅ / ❌ *(fill in)* |

**Screenshot / clip:** **

### 4.5 Iteration and Validation

#### Repeatability — 3 complete cycles in MuJoCo

| Cycle | Timestamp | Stages observed (orient → greet → neutral) | Behavior repeatable? | Notes |
|---|---|---|---|---|
| 1 | *(fill in)* | ✅ / ❌ | ✅ / ❌ | |
| 2 | *(fill in)* | ✅ / ❌ | ✅ / ❌ | |
| 3 | *(fill in)* | ✅ / ❌ | ✅ / ❌ | |

#### Stop-request testing (per stage)

| Stage interrupted | Stop method | Expected | Observed | Control loop left running? | Result |
|---|---|---|---|---|---|
| Orient | Ctrl-C | Robot halts orient motion, `finally` block returns to neutral | *(fill in)* | No / Yes | pass / fail |
| Greet | Ctrl-C | Loop exits at next `stop_event` check, returns to neutral | *(fill in)* | No / Yes | pass / fail |
| Neutral | Ctrl-C | App exits after final neutral hold | *(fill in)* | No / Yes | pass / fail |

#### Parameter variation

Four named parameters (`ORIENT_HEAD_YAW_DEG`, `ORIENT_DURATION_S`, `HEAD_TILT_DEG`, `ANTENNA_SWING_DEG`) were varied together to compare a subdued vs. expressive greeting style:

| | Parameter Set 1 (subtle) | Parameter Set 2 (expressive) |
|---|---|---|
| `ORIENT_HEAD_YAW_DEG` | 20.0° | 40.0° |
| `ORIENT_DURATION_S` | 2.0s | 1.0s |
| `GREETING_DURATION_S` | 4.0s | 4.0s |
| `HEAD_TILT_DEG` | 10.0° | 30.0° |
| `ANTENNA_SWING_DEG` | 12.0° | 50.0° |
| `RETURN_DURATION_S` | 2.0s | 2.0s |
| **Observed effect** | Motion is gentle and slow — head turns gradually, small nod, antennas sway lightly, smooth return to center. Reads as calm/subdued acknowledgment. | Head turn is much more pronounced, nod is larger, antennas swing more dramatically. Reads as an active, enthusiastic "I noticed you and I'm excited to greet you" behavior. |
| **Legibility** | *(fill in: e.g. "Easy to miss from a distance — the motion is subtle enough that a bystander might not register it as an intentional greeting.")* | *(fill in: e.g. "Clearly readable as an intentional greeting gesture even from across the room.")* |

#### Final candidate parameters and rationale

**Chosen for physical-robot transfer:** *(fill in — pick Set 1, Set 2, or a blended set, and justify)*

Suggested rationale framing (edit to match your actual choice and reasoning):

> We selected **Parameter Set 1 (subtle)** as our starting point for transfer to the physical robot. Set 2 is more expressive and legible in simulation, but it combines larger motion amplitudes (40° yaw, 30° head tilt, 50° antenna swing) with a *shorter* orient duration (1.0s vs. 2.0s) — meaning the head reaches a larger angle in less time, producing a notably higher angular velocity during orientation. This combination carries elevated risk on physical hardware: motor overshoot, mechanical stress, and momentum are not fully captured by MuJoCo's physics model, and Set 2's antenna swing (50°) in particular approaches a range where real servo torque and backlash could behave unpredictably. Starting with Set 1's smaller amplitudes and slower, 2.0s orient motion lets us validate motor behavior under load safely, then incrementally increase amplitude and speed toward Set 2's values only if the physical robot handles Set 1 without issue.

### Deliverables (5 points)

- [ ] Complete app source, `pyproject.toml`, and run instructions under `apps/team_greeting_app/`
- [ ] Screenshot and short clip showing all three stages with matching log markers in MuJoCo
- [ ] Simulation test record: 3 repeated cycles + stop-behavior table + parameter variation table (above)
- [ ] Rationale for final candidate parameters, including anticipated physical-robot risks (above)


