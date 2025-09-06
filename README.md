# Prompt Injection Lab

This repository contains a local lab environment for exploring **prompt injection** attacks against AI agents, inspired by the whitepaper: [Cybersecurity AI: Hacking the AI Hackers via Prompt Injection](https://arxiv.org/pdf/2508.21669).  

The lab uses Docker to simulate a vulnerable agent, a malicious server, and a listener. It also includes an optional LLM integration using **Ollama** with Llama 3.2.  

---

## Features

- Malicious webserver hosting an `index.html` payload.  
- Vulnerable agent that scrapes and executes injected commands.  
- Netcat listener for callbacks.  
- LLM-agent that connects to **Ollama** and processes injected content.  
- Modular Docker Compose setup for easy start/stop.  

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (allocate at least 6GB RAM in settings).  
- [Ollama](https://ollama.ai) (for LLM integration).  

---

## Quick Start

Clone this repository:

```bash
git clone https://github.com/aaronott/prompt-injection-lab.git
cd prompt-injection-lab
```

### Start the core lab (no LLM)

```bash
docker compose up -d malicious-server listener agent
```

- Malicious server runs a simple HTML payload.  
- Agent scrapes and executes the injected base64.  
- Listener waits for callbacks on port 4444.  

Attach to the listener:

```bash
docker attach pi_listener
# Use CTRL+P, CTRL+Q to detach
```

### Start with the LLM-Agent

First, bring up Ollama and the listener:

```bash
docker compose up -d ollama malicious-server listener
```

Pull the Llama 3.2 model into the container:

```bash
docker network connect prompt-injection-lab_default pi_ollama
docker exec -it pi_ollama bash -lc 'ollama pull llama3.2'
docker network disconnect prompt-injection-lab_default pi_ollama
```

Then launch the LLM-agent:

```bash
docker compose up -d llm-agent
docker attach pi_listener
```

---

## Screenshots

![Docker containers](Initial_docker_test.png)  
*Three containers running, with the listener waiting for callbacks.*  

![LLM agent running](docker_compose_up_llm-agent.png)  
*llm-agent container scraping and processing malicious HTML.*  

---

## Why This Lab?

This lab demonstrates how **AI agents can be exploited by prompt injection** when interacting with untrusted content—and how those same injections could be used to “hack back” malicious automations.  

It’s intentionally simple but offers a safe playground for exploring the security implications of AI in adversarial contexts.  

---


---

## Project Structure & What's Optional

This repo intentionally includes **some code that is not used in the default lab run**. I kept it to document the steps I took, and to give you jumping‑off points if you want to extend the lab.

```
.
├─ docker-compose.yml
├─ malicious-server/           # serves index.html with an embedded injection
│  ├─ Dockerfile
│  ├─ index.html
│  └─ server.py
├─ listener/                   # simple netcat listener on :4444
│  └─ Dockerfile
├─ agent/                      # NON‑LLM baseline agent (used in earliest setup)
│  ├─ Dockerfile
│  └─ agent.py
├─ llm-agent/                  # CURRENT agent that talks to Ollama (Llama 3.2)
│  ├─ Dockerfile
│  ├─ agent.py
│  └─ README.md                # reserved for future details
└─ cai-agent/                  # UNUSED placeholder (CAI was removed due to friction)
   └─ Dockerfile
```

### Which pieces run by default?
- **Used by default:** `malicious-server/`, `listener/`, `llm-agent/`, and the `ollama` service from `docker-compose.yml`.
- **Kept for reference / not used by default:**
  - `agent/` – the non‑LLM “baseline” agent used to validate the environment before adding an LLM.
  - `cai-agent/` – CAI integration stub. CAI connected to Ollama but did not execute actions reliably in this lab; left here so others can experiment.

### Why keep unused code?
- **Reproducibility:** documents the path taken (what worked, what didn’t).
- **Expandability:** gives you pre‑scaffolded places to add features (e.g., swap in a different agent framework, compare LLM vs non‑LLM behavior).
- **Teaching value:** shows an incremental approach—start simple, then introduce the LLM.

### Ideas for extending the unused pieces
- **`agent/` (non‑LLM):** add more deterministic decoders (base32/hex), simulate user prompts, or log/compare outcomes vs. the LLM agent.
- **`cai-agent/`:** wire up CAI actions/tooling and measure reliability vs. the lightweight agent; try different model endpoints.

### If you want to prune the repo
You can safely delete folders you don’t need (e.g., `cai-agent/` or `agent/`). Be sure to also remove their services (if present) from `docker-compose.yml`.

---
## Disclaimer

This project is for **educational and research purposes only**. Do not use it against systems you do not own or have explicit permission to test.  