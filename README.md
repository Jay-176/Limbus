# ☁️ Limbus AI Research Dashboard

**Limbus** is a fully decoupled, full-stack autonomous AI research terminal. It leverages live web scraping and the Google Gemini API to dynamically research topics, synthesize data, and generate fully cited Markdown reports in real-time.

![Limbus Dashboard](https://img.shields.io/badge/UI-Vercel_Inspired-black?style=flat-square&logo=vercel)
![Python](https://img.shields.io/badge/Backend-Python_3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688?style=flat-square&logo=fastapi)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4?style=flat-square&logo=google)

## ✨ Core Features

* **Live Deep-Web Scraping:** Bypasses basic search limitations by actively scraping and parsing live website text for real-time context.
* **Temporal Grounding:** Dynamically injects system datetime into the LLM context window to prevent temporal hallucinations.
* **Exponential Backoff:** Built-in fault tolerance. Automatically handles API traffic spikes (503 errors) by throttling and retrying rejected requests.
* **Client-Side State Management:** Utilizes `sessionStorage` for incognito-style memory, maintaining chat history during active sessions while protecting privacy upon tab closure.
* **Zero-Emoji Minimalist UI:** A bespoke, Vercel-inspired frontend built with Tailwind CSS and Material Symbols, featuring a custom SVG brand identity and an interactive developer portfolio modal.

## 🏗️ Architecture

Limbus operates on a decoupled Full-Stack architecture:
* **Frontend:** Pure HTML/JS with Tailwind CSS injected via CDN. Client-side Markdown parsing.
* **Backend:** Asynchronous Python API powered by **FastAPI**.
* **AI Engine:** `google-genai` SDK using the `gemini-2.5-flash` model.

