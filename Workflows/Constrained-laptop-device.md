## Constrained Incident‑Response Laptop Workflow  

> **Assumption:** The laptop has limited RAM (≤4 GB), no external write‑blocked media, and 
may run only a minimal Linux distribution (e.g., Alpine, Ubuntu minimal).  

### 1️⃣ Preparation  

- **Create a read‑only mount** of the internal drive (if possible) using `mount -o ro`.  
- **Allocate a small temporary workspace** on the internal drive (e.g., 
`/tmp/ir_workspace`).  
- **Enable logging** for all commands (`script -c "bash" /tmp/ir_commands.log`).  

### 2️⃣ Evidence Collection  

| Step | Action | Command / Tool | Notes |
|------|--------|----------------|-------|
| **2.1** | **Collect system logs** | `journalctl --since "1 hour ago" > 
/tmp/ir_workspace/journal.log` (Linux) <br> `wevtutil qe System /f:text /c 1000 > 
/tmp/ir_workspace/wevt.log` (Windows) | Keep only the most recent relevant entries to stay 
within storage limits. |
| **2.2** | **Capture active processes** | `ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu > 
/tmp/ir_workspace/processes.txt` | Focus on high‑CPU or unknown processes. |
| **2.3** | **Dump memory (lightweight)** | **Linux:** `sudo dd if=/dev/mem 
of=/tmp/ir_workspace/memory.dump bs=1M count=512` (captures first 512 MiB) <br> **Windows:** 
`procdump -ma -s 500 -n 5 <pid> C:\temp\mem_500.exe` (captures up to 500 MiB) | If memory is 
too scarce, consider ** Volatility 3’s `linux.dump`** or **`winpmem`** with limited size. |
| **2.4** | **Collect network capture** (short, focused) | `tcpdump -i eth0 -w 
/tmp/ir_workspace/traffic.pcap -c 5000` (Linux) <br> `netsh trace start capture=yes 
tracefile=C:\temp\traffic.etl maxsize=20` (Windows) | Limit to 30 seconds or 5 k packets to 
avoid filling the disk. |
| **2.5** | **Extract key files** (e.g., recent documents, configuration) | `find / -type f 
-mtime -1 -size +1M -exec tar czf /tmp/ir_workspace/recent_files.tar.gz {} +` (Linux) <br> 
`Get-ChildItem -Path C:\Users\* -Recurse -File | Where-Object {$_.LastWriteTime -gt 
(Get-Date).AddHours(-6)} | Compress-Archive -DestinationPath C:\temp\recent_files.zip` 
(Windows) | Helps preserve user‑visible artefacts without imaging the whole disk. |
| **2.6** | **Hash all collected artefacts** | `sha256sum /tmp/ir_workspace/* > 
/tmp/ir_workspace/hashes.txt` | Store hashes on a separate, read‑only medium if possible 
(e.g., a small USB stick). |
| **2.7** | **Preserve chain‑of‑custody** | Record: date/time, collector name, tool 
versions, command line, and hash values in a **single** `README.md` file inside the 
workspace. | This file becomes the primary evidence log. |

### 3️⃣ Post‑Collection  

- **Copy the entire workspace** to a **write‑once** medium (e.g., a CD‑R, write‑protected 
USB) **or** to a remote, encrypted storage (e.g., SFTP with key‑based auth).  
- **Verify integrity** by re‑hashing the copied bundle and comparing with the original 
`hashes.txt`.  
- **Document** any limitations encountered (e.g., “memory dump limited to 512 MiB due to RAM 
constraints”).  

---  

