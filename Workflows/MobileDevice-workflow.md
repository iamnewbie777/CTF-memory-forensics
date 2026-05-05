## Mobile Devices Workflow  

### 1️⃣ Preparation  

- **Device model & OS version** (Android 13 / iOS 17, etc.).  
- **Obtain user consent** or a legal subpoena.  
- **Set up a write‑blocked USB‑OTG adapter** (if using a PC) or a **dedicated forensic 
tablet** with enough storage.  

### 2️⃣ Evidence Collection  

| Step | Action | Command / Tool | Notes |
|------|--------|----------------|-------|
| **2.1** | **Logical extraction** (quick, low‑impact) | - Android: `adb pull /data/media/0 /tmp/logical/` <br> - iOS: use **Cellebrite UFED**, **Magnet AXIOM**, or **iMazing** (requires device unlock) | Produces a folder of user‑visible files (photos, messages, app data). |
| **2.2** | **Full file‑system image** (if device is rooted/jail‑broken or you have physical access) | - Android: `dd if=/dev/block/mmcblk0 of=/tmp/full.img bs=4M` (requires root) <br> - iOS: **iOS‑image‑tool** (requires DFU mode) | Store image on external SSD; verify hash. |
| **2.3** | **Extract system logs** | - Android: `adb shell dumpsys > /tmp/dumpsys.txt` <br> - iOS: extract `logarchive` via **iOS Backup** (`ios_backup_extractor`) | Logs often contain network activity, app crashes, and timeline data. |
| **2.4** | **Capture network traffic** | - Android: `tcpdump -i wlan0 -w /tmp/traffic.pcap` (requires root) <br> - iOS: use a **packet capture** app (e.g., **Shark for Rootless iOS**) | Limit capture to 5‑10 min to avoid storage overflow. |
| **2.5** | **Collect installed app data** | - Android: `adb shell run-as <package> cp -a /data/data/<package> /tmp/app_<package>/` <br> - iOS: extract app container via backup or 
**iMazing** | Useful for malware analysis, credential dumping. |
| **2.6** | **Extract location & timestamp data** | Parse `LocationHistory.db` (Android) or `Significant Locations` (iOS) using **plaso** (`log2timeline`) | Generates a timeline CSV. |
| **2.7** | **Securely delete temporary files** (if policy requires) | `shred -u /tmp/*` (Linux) | Ensure no leftover plaintext artifacts. |

### 3️⃣ Post‑Collection  

- **Hash each image/file** (`sha256sum <file>`). Store hashes in `hashes.txt`.  
- **Create a timeline** (e.g., using `plaso`/`timeline‑builder`) from logs, file timestamps, 
and network captures.  
- **Upload** the evidence bundle to a tamper‑evident store (e.g., S3 with Object Lock, 
encrypted external drive).  

---  


