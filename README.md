# mozichem-ai

# MoziChem-AI

MoziChem-AI is a premium web-based platform that supercharges your chemical engineering workflows. It combines advanced thermodynamic models, phase equilibrium tools, and reaction analysis with a clean and intuitive user interface.

Whether you’re performing VLE/LLE calculations, Gibbs energy minimization, or reaction feasibility studies, MoziChem-AI helps you get results faster and smarter — right from your browser.

It also integrates seamlessly with a local agent for heavy computations, ensuring both speed and data privacy. This hybrid architecture allows you to run state-of-the-art models without sending sensitive data to the cloud.

---

### ✨ Features

- 🌐 **Modern Web UI**  
  Beautiful, responsive interface hosted on [www.mozichem-ai.com](https://www.mozichem-ai.com)

- 🧪 **Thermodynamic Modeling**  
  Support for equations of state (Peng-Robinson, SRK) and activity models (NRTL, UNIQUAC)

- 🔥 **Phase Equilibrium Tools**  
  - VLE, LLE, VLLE, and SLE calculations  
  - Multicomponent diagram generation  

- ⚡ **Local Agent Integration**  
  - Securely connect to your own machine for heavy computations  
  - Supports offline workflows with the `mozichem-agent`

- 🤖 **AI-Powered Assistance**  
  Suggests parameters, predicts feasibility, and helps automate repetitive tasks.

- 📊 **Visualization Tools**  
  Generate phase diagrams, Txy/Pxy plots, and more directly in your browser.

- 🔐 **Privacy-First Design**  
  Sensitive data stays on your machine when using the local agent.

---

### 📦 Components

- **MoziChem-AI UI:** Angular frontend (hosted)  
- **MoziChem-Agent:** Python backend package for local calculations  
- **Cloud APIs (Optional):** For light/preview computations

---

### 🚀 Get Started

1. Install the local agent:
   ```bash
   pip install mozichem-ai
  ```
