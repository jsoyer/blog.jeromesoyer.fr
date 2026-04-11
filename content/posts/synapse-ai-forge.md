---
title: "Synapse: Building a Modular AI Forge on Fedora 43"
date: 2026-03-25T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A deep dive into the automated provisioning of a high-performance AI node with RTX 5070 and Podman rootless."
categories: ["AI", "DevOps", "Fedora"]
tags: ["rtx5070", "podman", "ollama", "uv", "automation", "nvidia", "fedora"]
---

### Beyond the Chatbot
If you've followed this blog, you know my obsession with local-first systems. Running a basic LLM is easy. Building a **professional-grade AI infrastructure** that is reproducible, secure, and high-performance is a different story.

Enter **Synapse**: my dedicated AI forge. While my Macs handle the interfaces, Synapse is the heavy lifter. Built on **Fedora 43**, it’s designed to provide a "zero-trust" environment for training and inference.

### The Hardware Stack
To handle modern models (Llama 3, Mistral) with large contexts, I chose a balance of core count and VRAM:
*   **CPU:** AMD Ryzen 7 3700X (8c/16t)
*   **GPU:** NVIDIA RTX 5070 (**12GB VRAM**, Blackwell architecture)
*   **RAM:** 32GB DDR4
*   **Storage:** 1TB NVMe SSD

The RTX 5070 is the star here. Its Blackwell architecture allows for incredibly fast inference and quantization, making it the perfect heart for a local forge.

### Modular Provisioning: The 00-10 Architecture
I don't manually install tools. I've developed a modular provisioning system consisting of 11 scripts (numbered 00 to 10) that take a fresh Fedora install to a fully operational AI lab in minutes.

#### 1. System & GPU (Scripts 00-03)
This layer handles the "dirty work": updating system packages, configuring `firewalld`, and installing the NVIDIA driver stack. Crucially, it sets up the **Container Device Interface (CDI)**, which allows Podman to access the GPU without the complexity of traditional Docker runtimes.

#### 2. The Python Engine: `uv` (Scripts 04-05)
I’ve completely replaced `pip` and `conda` with **[`uv`](https://github.com/astral-sh/uv)**. It manages my **Python 3.12** environments with near-instant speed. Each AI task (Training, RAG, Serving) gets its own isolated environment, ensuring no dependency hell.

#### 3. Rootless Services (Scripts 06-08)
Security is paramount. Every AI service runs in **Podman rootless mode** via `podman-compose`:
*   **Ollama & vLLM:** High-performance inference engines.
*   **Qdrant:** My vector database for local knowledge storage.
*   **Open-WebUI:** The frontend for interacting with my models.
*   **Redis & Postgres:** For caching and state management.

#### 4. Observability & Forge Modes (Scripts 09-10)
I’ve implemented a **"Forge Mode"** utility. With 12GB of VRAM, I can't run everything at once. This tool allows me to switch profiles:
*   **`forge-mode chat`**: Starts Ollama and WebUI.
*   **`forge-mode training`**: Shuts down the UI to free up every MB of VRAM for **Unsloth** and fine-tuning.

### Why Fedora 43?
Fedora remains the best playground for AI because it ships with the latest kernels and drivers. It supports rootless Podman and the NVIDIA stack better than almost any other distro, fitting perfectly into the "Least Privilege" philosophy: **modern, secure, and fast.**

---
*Stay local. Stay secure. Live the Least Privilege Life.*
