# 🌿 LEAF_TEOM

> **잎의 진동수 변화로 도시 가로수의 미세먼지 부담을 측정하는 비파괴 시스템**

[

![Status](https://img.shields.io/badge/status-research--in--progress-yellow)

]()
[

![Python](https://img.shields.io/badge/python-3.11-blue)

]()
[

![License](https://img.shields.io/badge/license-research--only-lightgrey)

]()

---

## 🎯 연구 개요

도시 가로수는 미세먼지를 흡수하며 도시 공기를 정화하지만,
PM이 잎 표면에 쌓이면서 광합성 효율이 떨어지고 잎이 병들어가는
**악순환**에 놓여 있습니다.

LEAF_TEOM은 EPA가 인증한 **TEOM(Tapered Element Oscillating Microbalance)**
원리를 식물 잎에 응용합니다.
잎의 고유진동수가 PM 침착으로 인해 어떻게 변하는지 측정해
**가로수 한 그루가 받는 PM 부담을 정량화**합니다.

### 핵심 아이디어

캔틸레버 빔의 고유진동수:

$$
f = \frac{1}{2\pi}\sqrt{\frac{k}{m}}
$$

PM이 잎에 침착되면 질량 m이 증가 → 고유진동수 f 감소.
정규화 차분 측정:

$$
\frac{\Delta f}{f} = -\frac{1}{2}\frac{\Delta m}{m}
$$

---

## 🛠️ 시스템 구조