# CMPE 273 – Week 1 Lab 1: Your First Distributed System

Spring 2026

---

## Lab Goal
Build a tiny locally distributed system with two independent services that communicate over the network, include basic logging, and demonstrate independent failure.

---

## What I Built

### Service A (Echo API) — Port 8080
Endpoints:
- `GET /health` → `{"status":"ok"}`
- `GET /echo?msg=hello` → `{"echo":"hello"}`

### Service B (Client Service) — Port 8081
Endpoints:
- `GET /health` → `{"status":"ok"}`
- `GET /call-echo?msg=hello`
  - Calls Service A `/echo`
  - Uses a timeout when calling Service A
  - Returns HTTP **503** if Service A is unavailable
  - Logs request details and errors

---

## How to Run Locally (Python)

### Prerequisites
- Python 3.10+
- Git

### Setup
```bash
git clone https://github.com/ShefaliSaini1204/cmpe273-week1-lab1
cd cmpe273-week1-lab1/python-http
python3 -m venv .venv
source .venv/bin/activate
pip install flask requests


### python service_a.py
