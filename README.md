<a href="https://www.linkedin.com/in/kavinkk-vlsi-embedded">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" width="100%" alt="Kavin K K. Embedded Systems, Hardware Security, RTOS, Applied Cryptography">
  </picture>
</a>

### Hi, I'm Kavin.

I'm an electronics engineer (B.Tech Electronics Engineering, VLSI, at Rashtriya Raksha University) who
works where firmware, digital logic and security meet.

**What ties the work together:** I test whether a hardware claim holds up against the real thing: a latency
claim against a logic analyzer, an error metric against real video encoders, and a redundancy countermeasure
against the physics of a glitch (that last one is work in progress).

I say what kind of result each number is. Two projects below ran on real hardware (Haptic-Sense and
PhyRand). The rest are simulation, synthesis or host-tested code, and are labelled that way. Where a number
appears, the repository says how it was produced and what has not been measured yet.

**Open to embedded firmware, RTOS, digital design and hardware-security roles.**
[Connect on LinkedIn](https://www.linkedin.com/in/kavinkk-vlsi-embedded)

## Projects

Three flagships and three supporting projects.

<p align="center">
  <a href="https://github.com/Kavin-Re/Haptic-Sense">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-haptic-sense-dark.svg">
      <img src="assets/card-haptic-sense-light.svg" width="49%" alt="Haptic-Sense: µT-Kernel 3.0 on STM32N6, 3.375 µs worst-case preemption latency (logic analyzer)">
    </picture>
  </a>
  <a href="https://github.com/Kavin-Re/GlitchSAT-Redundancy">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-glitchsat-dark.svg">
      <img src="assets/card-glitchsat-light.svg" width="49%" alt="GlitchSAT: fault analysis of gate-level netlists; the three reference designs need 1, 1 and 3 modelled bit flips under the single-bit model M0 (model results, not physical glitches)">
    </picture>
  </a>
</p>
<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-sad-paper-dark.svg">
      <img src="assets/card-sad-paper-light.svg" width="49%" alt="Approximate SAD: approximate compressor cells in an 8x8 SAD datapath, tested in the x264 and x265 encoders; co-authored manuscript, not yet published (repository private)">
    </picture>
  <a href="https://github.com/Kavin-Re/PhyRand">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-phyrand-dark.svg">
      <img src="assets/card-phyrand-light.svg" width="49%" alt="PhyRand: Zener-diode noise source on STM32F401RE, 7.9997 bits/byte Shannon entropy on a 1 MB capture computed by the repository's own analysis; the same capture fails chi-square; the source is unvalidated">
    </picture>
  </a>
</p>
<p align="center">
  <a href="https://github.com/Kavin-Re/FHSS-Link">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-fhss-link-dark.svg">
      <img src="assets/card-fhss-link-light.svg" width="49%" alt="FHSS-Link: frequency-hopping link study; a 16-bit LFSR hop schedule is broken after 8 to 9 observed hops, replaced by a keyed SipHash engine in Verilog (simulation and RTL)">
    </picture>
  </a>
  <a href="https://github.com/Kavin-Re/VCD-Studio">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/card-vcd-studio-dark.svg">
      <img src="assets/card-vcd-studio-light.svg" width="49%" alt="VCD-Studio: waveform viewer for VCD dumps in one offline HTML file">
    </picture>
  </a>
</p>

### Flagships

| Project | In one line | Status |
|---|---|---|
| [**Haptic-Sense**](https://github.com/Kavin-Re/Haptic-Sense) | Predictive obstacle-alert prototype for visually impaired users on an STM32N6570-DK running µT-Kernel 3.0. TRON Forum Programming Contest 2026, entry 34476. | **Hardware, measured. Frozen.** Worst-case preemption latency 3.375 µs (logic analyzer) and 4.19 µs (cycle counter, 30-minute soak). These time the task handoff, not sensor-to-motor latency. Benchtop prototype, urgency feedback only, no direction. |
| [**GlitchSAT**](https://github.com/Kavin-Re/GlitchSAT-Redundancy) | Open-source fault-analysis tool for gate-level netlists: finds the smallest number of modelled bit flips that defeat a protection, checks whether a protection survived synthesis, and explains the result in a teaching app. | **Model only.** Nothing was measured on hardware. The current model flips single bits independently, so it does not cover one glitch upsetting several flip-flops, or all copies, at once. Version 2.0 asks one question: does adding timing change the verdict on one real protected block? |
| **Approximate-SAD paper** | Research internship at NIT Delhi (summer 2026), co-authored manuscript: approximate compressor cells in a shared 8x8 SAD datapath for video motion estimation, synthesised and run inside the x264 and x265 encoders. | **Simulation, synthesis and real encoders.** Not yet published. The repository stays private until publication. |

### Supporting

| Project | In one line | Status |
|---|---|---|
| [**PhyRand**](https://github.com/Kavin-Re/PhyRand) | Zener-diode noise source on an STM32F401RE with Von Neumann debiasing, a health-tested key pipeline and a file vault. | **Hardware, source unvalidated.** A 1 MB capture has 7.9997 bits/byte Shannon entropy (computed with the repository's own analysis), and the same capture fails chi-square (p = 0.0009). The control run with the diode removed has not been done. |
| [**FHSS-Link**](https://github.com/Kavin-Re/FHSS-Link) | Frequency-hopping link study: link and attacker simulators, a keyed SipHash-2-4 hop engine in Verilog, a C reference, and the HopBench schedule benchmark. | **Simulation, RTL and host C. Frozen.** An attacker model recovers a 16-bit LFSR hop schedule after 8 or 9 observed hops (exhaustive over all 65,535 seeds); the keyed schedule stays at chance against that attacker. Nothing has run on a radio. |
| [**VCD-Studio**](https://github.com/Kavin-Re/VCD-Studio) | Waveform viewer for Verilog `.vcd` dumps in one offline HTML file, plus a standard-library script for toggle counts. | **Tool. Frozen.** Works on any `.vcd` in a browser with nothing installed. GTKWave and Surfer do more. |

Every other repository on this account is frozen or archived, and its README says which and why.

## What I build

| Area | What that has meant so far |
|---|---|
| **Hardware security** | A noise source built from Zener-diode breakdown with on-chip Von Neumann debiasing; a keyed SipHash-2-4 hop engine in Verilog checked against a Python model and with SymbiYosys; a fault-analysis tool that searches netlists for the fewest modelled bit flips that defeat a protection. |
| **Real-time firmware** | A four-task µT-Kernel 3.0 application on a Cortex-M55 with preemption latency measured two ways (logic analyzer and in-firmware cycle counter); a first bare-metal STM32F4 project that parses UART telemetry onto an OLED (its SD logging never worked); C99 protocol references with no dynamic allocation, tested under sanitizers on the host. |
| **Digital design and approximate computing** | Approximate SAD datapaths for video motion estimation, synthesised and tested inside real encoders; approximate adders and multipliers as bit-accurate Python models plus Verilog, compared exhaustively in Icarus Verilog. |
| **Edge ML on MCUs** | A small INT8 model trained in Edge Impulse and run on the STM32N6 Neural-ART NPU, backed by a deterministic safety rule. |
| **Tooling** | A single-file browser waveform viewer for VCD dumps, and serial capture and analysis scripts. |

## Tech stack

<table>
  <tr><td><b>Languages</b></td><td><img src="https://img.shields.io/badge/C-3a4654?style=flat-square&logo=c&logoColor=white" alt="C"> <img src="https://img.shields.io/badge/Python-3a4654?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Verilog-3a4654?style=flat-square" alt="Verilog"> <img src="https://img.shields.io/badge/Bash-3a4654?style=flat-square&logo=gnubash&logoColor=white" alt="Bash"></td></tr>
  <tr><td><b>MCUs &amp; boards</b></td><td><img src="https://img.shields.io/badge/STM32F4%20%28Cortex--M4%29-0b7a55?style=flat-square&logo=stmicroelectronics&logoColor=white" alt="STM32F4 (Cortex-M4)"> <img src="https://img.shields.io/badge/STM32N6%20%28Cortex--M55%20%2B%20NPU%29-0b7a55?style=flat-square&logo=stmicroelectronics&logoColor=white" alt="STM32N6 (Cortex-M55 + NPU)"></td></tr>
  <tr><td><b>RTOS &amp; firmware</b></td><td><img src="https://img.shields.io/badge/%C2%B5T--Kernel%203.0-a85d00?style=flat-square" alt="µT-Kernel 3.0"> <img src="https://img.shields.io/badge/STM32%20HAL-a85d00?style=flat-square" alt="STM32 HAL"> <img src="https://img.shields.io/badge/FatFS-a85d00?style=flat-square" alt="FatFS"> <img src="https://img.shields.io/badge/STM32CubeIDE-a85d00?style=flat-square" alt="STM32CubeIDE"></td></tr>
  <tr><td><b>RTL &amp; verification</b></td><td><img src="https://img.shields.io/badge/Icarus%20Verilog-0b7a55?style=flat-square" alt="Icarus Verilog"> <img src="https://img.shields.io/badge/Verilator-0b7a55?style=flat-square" alt="Verilator"> <img src="https://img.shields.io/badge/Yosys-0b7a55?style=flat-square" alt="Yosys"> <img src="https://img.shields.io/badge/SymbiYosys%20%28formal%29-0b7a55?style=flat-square" alt="SymbiYosys (formal)"> <img src="https://img.shields.io/badge/sky130%20synthesis%20estimates-0b7a55?style=flat-square" alt="sky130 synthesis estimates"></td></tr>
  <tr><td><b>Buses &amp; peripherals</b></td><td><img src="https://img.shields.io/badge/I2C-3a4654?style=flat-square" alt="I2C"> <img src="https://img.shields.io/badge/SPI-3a4654?style=flat-square" alt="SPI"> <img src="https://img.shields.io/badge/UART-3a4654?style=flat-square" alt="UART"> <img src="https://img.shields.io/badge/ADC-3a4654?style=flat-square" alt="ADC"> <img src="https://img.shields.io/badge/DMA-3a4654?style=flat-square" alt="DMA"></td></tr>
  <tr><td><b>Security &amp; crypto</b></td><td><img src="https://img.shields.io/badge/entropy%20analysis-0b7a55?style=flat-square" alt="entropy analysis"> <img src="https://img.shields.io/badge/Von%20Neumann%20debiasing-0b7a55?style=flat-square" alt="Von Neumann debiasing"> <img src="https://img.shields.io/badge/SipHash--2--4-0b7a55?style=flat-square" alt="SipHash-2-4"> <img src="https://img.shields.io/badge/side--channel%20analysis%20%28simulated%29-0b7a55?style=flat-square" alt="side-channel analysis (simulated)"> <img src="https://img.shields.io/badge/Fernet%20%28AES--128--CBC%20%2B%20HMAC%29-0b7a55?style=flat-square" alt="Fernet (AES-128-CBC + HMAC)"></td></tr>
  <tr><td><b>Edge ML</b></td><td><img src="https://img.shields.io/badge/Edge%20Impulse-a85d00?style=flat-square" alt="Edge Impulse"> <img src="https://img.shields.io/badge/TFLite%20INT8-a85d00?style=flat-square" alt="TFLite INT8"> <img src="https://img.shields.io/badge/ST%20Neural--ART-a85d00?style=flat-square" alt="ST Neural-ART"></td></tr>
  <tr><td><b>Host side</b></td><td><img src="https://img.shields.io/badge/FastAPI-3a4654?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"> <img src="https://img.shields.io/badge/NumPy-3a4654?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"> <img src="https://img.shields.io/badge/pySerial-3a4654?style=flat-square" alt="pySerial"> <img src="https://img.shields.io/badge/Linux-3a4654?style=flat-square&logo=linux&logoColor=white" alt="Linux"> <img src="https://img.shields.io/badge/Git-3a4654?style=flat-square&logo=git&logoColor=white" alt="Git"></td></tr>
</table>

## Currently

- Working on GlitchSAT 2.0: does adding timing change the verdict of a fault search on one real protected
  block? One design, one short technical note.
- Taking the co-authored approximate-SAD manuscript through to publication.
- Looking for a role in embedded systems, digital design or hardware security.

## Contact

- LinkedIn: [linkedin.com/in/kavinkk-vlsi-embedded](https://www.linkedin.com/in/kavinkk-vlsi-embedded)
- GitHub: open an issue on any repository above, and I will reply there.

<!--
Optional: live GitHub stats. These come from a third-party service (github-readme-stats), which can be
slow or rate-limited on its public instance. Remove the comment markers around this block to enable it.

<p align="center">
  <img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Kavin-Re&layout=compact&hide_border=true&theme=transparent" alt="Most used languages">
</p>
-->

<sub>Banner and project cards are SVG files generated by <a href="tools/build_assets.py"><code>tools/build_assets.py</code></a>. No trackers, no external fonts.</sub>
