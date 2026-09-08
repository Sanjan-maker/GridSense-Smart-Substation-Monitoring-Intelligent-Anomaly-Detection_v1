# GridSense – Smart Substation Monitoring & Intelligent Anomaly Detection

> A Python-based prototype for simulating power-system operating conditions, detecting electrical faults using engineering rules, and identifying abnormal operating behaviour using machine learning.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Scikit-learn](https://img.shields.io/badge/ML-Scikit--learn-orange)
![Status](https://img.shields.io/badge/Status-Prototype-success)
![Domain](https://img.shields.io/badge/Domain-Smart%20Grid%20%26%20Substation-blueviolet)

---

## Overview

GridSense is an industrial-inspired smart substation monitoring prototype built to explore how electrical measurements can be monitored, validated, and analyzed using a combination of traditional rule-based engineering logic and machine learning.

The system simulates electrical operating parameters such as voltage, current, frequency, power factor, active power, and reactive power. These measurements are evaluated under both normal and controlled fault conditions.

Two complementary detection approaches are used:

1. **Rule-Based Monitoring** – Detects known electrical threshold violations such as overvoltage, undervoltage, overcurrent, underfrequency, and overfrequency.
2. **Machine Learning-Based Anomaly Detection** – Uses an Isolation Forest trained on normal operating data to identify multivariate behaviour that deviates from expected system operation.

The objective of this project is not to represent a production-grade substation control system. Instead, it serves as a learning-oriented engineering prototype demonstrating concepts related to:

- Power-system monitoring
- Electrical fault scenarios
- Intelligent anomaly detection
- Event logging
- Engineering validation
- Automated testing
- Smart substation concepts

---

# Problem Statement

Modern electrical systems generate large volumes of operational measurements. Traditional monitoring systems often rely on predefined thresholds to detect abnormal conditions.

For example:

- Voltage exceeding a configured limit may indicate an overvoltage condition.
- Current exceeding a safe operating range may indicate overcurrent.
- Frequency deviation may indicate instability in the power system.

While threshold-based monitoring is effective for known and well-defined conditions, some abnormal behaviour may involve combinations of multiple parameters that are difficult to capture using individual rules alone.

GridSense explores a hybrid monitoring approach:

```text
Electrical Measurements
        │
        ▼
┌───────────────────────┐
│  Monitoring Engine    │
└───────────────────────┘
        │
        ├───────────────┐
        ▼               ▼
Rule-Based          ML-Based
Alarm Engine        Anomaly Detection
        │               │
        └───────┬───────┘
                ▼
         Monitoring Result
                │
                ▼
           Event Logging
