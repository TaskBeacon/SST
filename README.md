# Stop-Signal Task (SST) – PsyFlow Version

This task implements a Stop-Signal paradigm (SST) to assess inhibitory control mechanisms. Participants are asked to respond to left- or right-pointing arrows, but on some trials, they must inhibit their response when a red arrow appears. The task is built using the [PsyFlow](https://taskbeacon.github.io/psyflow/) framework.



## Task Overview

Participants are instructed to respond as quickly and accurately as possible to directional arrows by pressing the left or right arrow keys. Occasionally, a red arrow appears after a short delay, signaling participants to withhold their response.

The task uses an adaptive staircase procedure to dynamically adjust the stop-signal delay (SSD) to maintain approximately 50% successful inhibition on stop trials.



## Task Flow

| Step        | Description |
|-|-|
| Instruction | A textbox (`instruction_text`) presents task instructions in Chinese. The participant presses the **space bar** to start. |
| Fixation    | A fixation cross "+" is shown before each trial. |
| Go Trial    | A white arrow points left or right. Participant should respond by pressing the matching arrow key. |
| Stop Trial  | A red arrow appears after a delay (SSD); participant must inhibit their response. |
| Feedback    | If no response is made on a go trial, a warning feedback is displayed. |
| Block Break | After each block, performance summaries are shown with options to rest. |
| Goodbye     | A final thank-you screen and task termination.



## Configuration Summary

All key settings are defined in `config/config.yaml`.

### Subject Info (`subinfo_fields`)
Participants register with:
- **Subject ID** (three-digit number from 101–999)
- **Session name**
- **Experimenter**
- **Gender** (Male or Female)

Localized prompts are available via `subinfo_mapping`.



### Window Settings (`window`)
- Resolution: `1920 × 1080`
- Units: `deg`
- Fullscreen: `True`
- Monitor: `testMonitor`
- Background color: `gray`



### Stimuli (`stimuli`)
| Stimulus Name         | Type    | Description |
|-|-|-|
| `fixation`            | `text`  | Central fixation cross "+" |
| `go_left`, `go_right` | `shape` | White arrows indicating response direction |
| `stop_left`, `stop_right` | `shape` | Red arrows indicating stop signal |
| `no_response_feedback`| `textbox` | Feedback message for missed go responses |
| `instruction_text`    | `textbox` | Pre-task instruction screen |
| `block_break`         | `textbox` | Mid-task break screen |
| `good_bye`            | `textbox` | Final thank-you screen |
| `iti_stim`            | `text`   | Blank screen during ITI |



### Timing (`timing`)
| Phase                | Duration |
|-|-|
| Fixation             | 0.5–0.8 seconds (randomized) |
| Go stimulus duration | 1.0 second |
| No-response feedback | 0.8 seconds |
| ITI                  | 0.5–0.8 seconds (randomized) |



### Triggers (`triggers`)
The following event triggers are sent for synchronization (e.g., EEG, MEG):

| Event                | Code |
|-|-|
| Experiment start     | 98 |
| Experiment end       | 99 |
| Block start          | 100 |
| Block end            | 101 |
| Fixation onset       | 1 |
| Go onset             | 10 |
| Go response          | 11 |
| Go miss              | 12 |
| Pre-stop response    | 23 |
| On-stop response     | 24 |
| Post-stop response   | 25 |
| No-response feedback onset | 30 |



### Adaptive Controller (`controller`)
The SST uses a staircase tracking algorithm to adjust stop-signal delay (SSD).

| Parameter               | Value |
|-|-|
| Initial SSD             | 0.25 seconds |
| Step Size               | 0.05 seconds |
| Minimum SSD             | 0.05 seconds |
| Maximum SSD             | 0.5 seconds |
| Target Success Rate     | 50% (1-up/1-down staircase method) |

The staircase controller increases or decreases the SSD based on whether the participant successfully inhibits their response.


## Running the Task

```python
python main.py
```
