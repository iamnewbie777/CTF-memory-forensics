# CTF Memory forensics framework
A practical, step‑by‑step workflow for solving memory‑forensics challenges in Capture‑the‑Flag 
(CTF) competitions. 
Suitable for Windows, Linux, and macOS memory dumps.
---

## 📚  Overview

This repository documents a repeatable **memory‑forensics workflow** that blends 
incident‑response best practices with CTF‑specific shortcuts.  
It is organized into six major phases:

1. **Preparation & Tool‑chain Setup**  
2. **Collection & Imaging**  
3. **Initial Triage (Fast‑Look)**  
4. **Deep Dive – Structured Analysis**  
5. **Verification & Reporting**  
6. **Quick Reference Cheat‑Sheet (Volatility 3)**  

---

## 🔧  Preparation & Tool‑chain Setup  

| Goal | Typical Tools / Frameworks |
|------|----------------------------|
| Reproducible environment | Docker / VM image with Volatility 3, Rekall, Python, Git |
| Static analysis of challenge files | `binwalk`, `7zip`, `file`, `strings`, `exiftool`, 
`bulk_extractor` |
| Memory acquisition knowledge | Understand OS (Win10, Ubuntu, macOS) and dump formats (`.raw`, 
`.rawE01`, `.mem`) |
| Version‑control of scripts | Git (e.g., `CTF‑memory‑analysis` repo) |

---

## 📦  Collection & Imaging  

1. **Identify the memory source** – live RAM, page‑file, hibernation file, full disk, etc.  
2. **Validate the dump** – compute SHA‑256, compare with supplied checksum, verify OS version.  
3. **Preserve the original** – keep a write‑protected copy (`dump.raw.orig`). Work only on a 
duplicate.

*CTF tip*: Some challenges give a partial dump (e.g., first 64 MiB). Note the limitation in your 
write‑up.

---

## 🔎  Initial Triage (Fast‑Look)

| Step | What you do | Typical commands / plugins |
|------|-------------|----------------------------|
| Identify the OS | Look at PE/ELF/Mach‑O signatures or OS section. | `vol -f dump.raw 
windows.info` (Volatility 3) |
| List processes / threads | Quick glance at active processes, command lines, thread stacks. | 
`vol -f dump.raw windows.pslist` → `windows.pslist` |
| Extract obvious strings | Search for flag fragments, URLs, base64 blobs. | `strings -a 
dump.raw | grep -i flag` or `windows.strings` |
| Detect anomalies | Unexpected modules, hidden processes, process‑in‑process techniques. | `vol 
-f dump.raw windows.modules` or `windows.heaptrack` |

If anything looks promising, move on to deeper analysis.

---

## 🕵️  Deep Dive – Structured Analysis  

### A. Process‑Based Exploration  

| Sub‑step | Goal | Volatility 3 plugins (Windows) | Rekall equivalents |
|----------|------|------------------------------|--------------------|
| Process list | Identify executables, PID, command line. | `windows.pslist`, `windows.cmdline` 
| `rekall -f dump.raw linux.pslist` |
| Memory map | See loaded DLLs, drivers, mapped files. | `windows.modulelist`, 
`windows.mapslist` | `rekall -f dump.raw linux.maps` |
| Thread stack traces | Look for suspicious API calls (`VirtualAlloc`, `WriteProcessMemory`, 
etc.). | `windows.threadstacks` | `rekall -f dump.raw linux.threadstacks` |
| Hidden/ghost processes | Detect unloaded processes that still have memory pages. | 
`windows.heaptrack`, `windows.hidden_processes` | `rekall -f dump.raw linux.hidden` |

**Typical CTF clues**  
* Suspicious command line (e.g., `powershell -enc …`).  
* DLL loaded from `%TEMP%` or a user‑writable folder.  
* Thread repeatedly calling `ntdll!NtWriteVirtualMemory` → possible code injection.

### B. Artifact Extraction  

| Artifact | Why it matters in CTF | Extraction method |
|----------|----------------------|-------------------|
| Registry hives (`SYSTEM`, `SOFTWARE`) | May hold credentials, keys, or the flag. | `vol -f 
dump.raw windows.registry` → parse with `reglookup` or export to JSON. |
| SAM/LSA secrets | Password hashes or clear‑text secrets. | `vol -f dump.raw windows.malfind` + 
`windows.dumpfiles` for `SAM`, `lsav`. |
| Network sockets / connections | C2 traffic may contain the flag or a key. | `vol -f dump.raw 
windows.netstat` |
| Strings (quick search) | Fast way to spot flag fragments. | `vol -f dump.raw windows.strings | 
grep -i flag` |
| Timeline (optional) | Correlate events with process activity. | `vol -f dump.raw 
windows.timeline` |

---

## 📊  Quick Reference Cheat‑Sheet (Volatility 3)

```bash
# 1️⃣  Basic info
vol -f dump.raw windows.info

# 2️⃣  Process list + command lines
vol -f dump.raw windows.pslist
vol -f dump.raw windows.cmdline

# 3️⃣  Modules / loaded DLLs
vol -f dump.raw windows.modules

# 4️⃣  Network connections
vol -f dump.raw windows.netstat

# 5️⃣  Registry hive
vol -f dump.raw windows.registry

# 6️⃣  Strings (quick search)
vol -f dump.raw windows.strings | grep -i flag

# 7️⃣  Timeline (if needed)
vol -f dump.raw windows.timeline
```

*Rekall equivalents* replace `windows.` with `linux.` or `macos.` and use the appropriate plugin 
names (e.g., `rekall -f dump.raw linux.pslist`).

---

## 🎯  TL;DR – The “CTF Memory‑Forensics” Framework  

1. **Prep** – reproducible env, tools, version‑control.  
2. **Collect & Verify** – acquire a clean dump, hash it, keep a copy.  
3. **Fast‑Look** – OS ID, process list, obvious strings.  
4. **Deep Dive** – process‑by‑process memory maps, thread stacks, hidden artifacts (registry, 
network, files, secrets).  
5. **Extract & Correlate** – pull out flags, decode, tie to timeline events.  
6. **Validate & Report** – double‑check the flag, write a clear, reproducible write‑up.

---

## 📂  Repository Structure (suggested)

```
ctf-memory-forensics/
│
├─ README.md                # ← this file
├─ docs/                    # optional: detailed walkthroughs, screenshots
│   └─ example_challenge/  # example dump + analysis notes
├─ scripts/                 # optional: helper Python/ Bash scripts
│   └─ parse_vol.py
└─ .gitignore               # ignore large dump files, virtualenv, etc.
```

---

## 🚀  Getting Started

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/<YOUR_USERNAME>/ctf-memory-forensics.git
cd ctf-memory-forensics

# Install Volatility 3 (Python 3.9+ recommended)
python -m venv venv
source venv/bin/activate
pip install volatility3

# Run a quick sanity check on a sample dump
vol -f samples/example.raw windows.info
```

Feel free to open an issue or submit a pull request if you improve the framework!

---

**Happy hunting!** 🎉🧠🚩
