# Stop-Signal Task (SST)

| Field                | Value                        |
|----------------------|------------------------------|
| Name                 | Stop-Signal Task (SST)       |
| Version              | main (1.0)                          |
| URL / Repository     | https://github.com/TaskBeacon/SST        |
| Short Description    | A response inhibition task measuring the ability to suppress prepotent motor responses |
| Created By           | Zhipeng Cao (zhipeng30@foxmail.com) |
| Date Updated         |2025/06/22                              |
| PsyFlow Version      | 0.1.0                             |
| PsychoPy Version     | 2025.1.1                             |
|Modality            | Behavior/EEG                |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

The Stop-Signal Task (SST) is a cognitive paradigm used to assess response inhibition—the ability to withhold an already-initiated action. In each trial, participants are instructed to respond to directional go stimuli (left or right arrows) by pressing the corresponding key. On a subset of trials, a red stop signal appears shortly after the go stimulus, indicating that the participant should inhibit their response. The delay between the go and stop signal (SSD) is adaptively adjusted to maintain a 50% stop success rate.

## 2. Task Flow

### Block-Level Flow

| Step                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Load Config                | Load YAML configuration for subject, task, timing, stimuli, and controller |
| Collect Subject Info       | Get subject ID, name, age, and gender                                      |
| Setup Triggers             | Initialize trigger sender (via loopback serial)                            |
| Initialize Window/Input    | Set up PsychoPy window and keyboard                                        |
| Load Stimuli               | Load all visual/text stimuli, convert instructions to audio                |
| Initialize Controller      | Create SSD controller from config                                          |
| Show Instructions          | Display instruction text + voice before starting                           |
| Loop Over Blocks           | For each of 3 blocks: run 70 trials with generated conditions               |
| Compute Block Feedback     | Show go hit rate and stop success rate per block                           |
| Show Goodbye               | Final message after task completion                                        |
| Save Data                  | Save full trial-level data to CSV                                          |
| Close                      | Close serial connection and PsychoPy window                                |

### Trial-Level Flow

| Step                | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Fixation            | Present fixation cross for 0.8–1.0s with trigger                            |
| Go Only Trial       | Present arrow; wait up to 1s for correct keypress; show feedback if none    |
| Stop Trial          | Present arrow for SSD duration; then switch to red stop signal              |
| Response Recording  | Capture whether responses occurred before or after stop signal              |
| Adaptive Update     | Adjust SSD based on stop success/failure                                    |

### Controller Logic

| Feature             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Type                | 1-up/1-down staircase adjusting stop-signal delay (SSD)                     |
| Target Success Rate | 50%                                                                         |
| Step Size           | ±0.05s                                                                      |
| Range               | 0.05–0.5s                                                                   |
| Condition Pooling   | Shared SSD across conditions                                                |
| Logging             | Logs SSD adjustment and performance to PsychoPy console                    |

## 3. Configuration Summary

### a. Subject Info

| Field       | Meaning                        |
|-------------|--------------------------------|
| subject_id  | Unique participant number (101–999) |
| subname     | Participant name (pinyin)      |
| age         | Age (5–60)                     |
| gender      | Gender (Male or Female)        |

### b. Window Settings

| Parameter             | Value         |
|-----------------------|---------------|
| size                  | [1920, 1080]  |
| units                 | deg           |
| screen                | 1             |
| bg_color              | gray          |
| fullscreen            | True          |
| monitor_width_cm      | 60            |
| monitor_distance_cm   | 72            |

### c. Stimuli

| Name                  | Type   | Description                                         |
|------------------------|--------|-----------------------------------------------------|
| fixation               | text   | White cross "+"                                     |
| go_left                | shape  | White left-pointing arrow                           |
| go_right               | shape  | White right-pointing arrow                          |
| stop_left              | shape  | Red left-pointing arrow                             |
| stop_right             | shape  | Red right-pointing arrow                            |
| no_response_feedback   | text   | Message shown if participant fails to respond       |
| block_break            | text   | Inter-block feedback with hit/stop accuracy         |
| instruction_text       | textbox| Full task instructions with keys and stop rule      |
| good_bye               | textbox| Final screen thanking participant                   |

### d. Timing

| Phase                       | Duration (s)        |
|-----------------------------|---------------------|
| fixation                    | random 0.8–1.0      |
| go stimulus (max duration)  | 1.0                 |
| stop signal delay (SSD)     | adaptive (0.05–0.5) |
| no-response feedback        | 0.8                 |

### e. Triggers

| Event                      | Code  |
|----------------------------|-------|
| exp_onset                  | 98    |
| exp_end                    | 99    |
| block_onset                | 100   |
| block_end                  | 101   |
| fixation_onset             | 1     |
| go_onset                   | 10    |
| go_response                | 11    |
| go_miss                    | 12    |
| pre_stop_response          | 23    |
| on_stop_response           | 24    |
| post_stop_response         | 25    |
| no_response_feedback_onset | 30    |

### f. Adaptive Controller

| Parameter          | Value    |
|--------------------|----------|
| initial_ssd        | 0.25     |
| min_ssd            | 0.05     |
| max_ssd            | 0.5      |
| step               | 0.05     |
| target_success     | 0.5      |
| condition_specific | False    |
| enable_logging     | True     |

## 4. Methods (for academic publication)

Participants completed a stop-signal task (SST) designed to evaluate response inhibition. The task consisted of **3 blocks**, each containing **70 trials**, resulting in a total of **210 trials**. On each trial, participants saw a directional arrow (left or right) and were instructed to press the corresponding key—“F” for left, “J” for right—as quickly and accurately as possible. On **25% of the trials**, the arrow changed color (white to red) shortly after its onset, signaling the participant to inhibit their response. The delay between the go stimulus and the stop signal—the stop-signal delay (SSD)—was controlled adaptively using a 1-up/1-down staircase procedure. The SSD increased after successful inhibition and decreased after failed inhibition, with a target success rate of 50%.Trials began with a fixation cross (0.8–1.0s), followed by a go arrow. On go trials, the arrow remained on screen for up to 1 second or until a keypress. If no response occurred, a warning message was presented. On stop trials, the red stop signal replaced the arrow after an SSD-determined delay. Responses were recorded for both go and stop phases. The SSD was adjusted per trial based on inhibition performance. Participants received a break after each block, displaying their hit rate on go trials and success rate on stop trials.

## 5. References

>Kok, A., Ramautar, J. R., De Ruiter, M. B., Band, G. P., & Ridderinkhof, K. R. (2004). ERP components associated with successful and unsuccessful stopping in a stop‐signal task. Psychophysiology, 41(1), 9-20.

>Casey, B. J., Cannonier, T., Conley, M. I., Cohen, A. O., Barch, D. M., Heitzeg, M. M., ... & Dale, A. M. (2018). The adolescent brain cognitive development (ABCD) study: imaging acquisition across 21 sites. Developmental cognitive neuroscience, 32, 43-54.