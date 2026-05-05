## Shared Tools & Tips  

| Category | Tool | Platform | Why It’s Useful |
|----------|------|----------|-----------------|
| **Disk/Filesystem Imaging** | `dd` | Linux/Windows (via Cygwin) | Simple, bit‑for‑bit copy; can limit size (`bs=4M`). |
| | `FTK Imager` | Windows | GUI, can create raw images, verify hashes. |
| **Memory Dump** | `LiME` (Linux) | Linux | Kernel module for live memory capture. |
| | `Volatility 3` | Cross‑platform | Analyzes dumps; also can generate lightweight dumps. |
| **Log Parsing** | `plaso` (`log2timeline`) | Cross‑platform | Generates unified timeline from many sources. |
| **Network Capture** | `tcpdump` | Linux/macOS | Powerful, filter‑able packet capture. |
| | `Wireshark` | Cross‑platform | GUI for deep packet inspection. |
| **Hashing** | `sha256sum` / `CertUtil` | Linux/Windows | Fast, widely accepted hash algorithm. |
| **Remote Collection** | `ssh` with `-w` (port forwarding) | Linux/Windows (WSL) | Allows running capture tools on the target without direct access. |
| **Immutable Storage** | Cloud object lock (S3, Azure Blob) | Cloud | Guarantees write‑once, read‑many compliance. |

### General Tips  

- **Always hash before moving data** – guarantees integrity.  
- **Document every command** (full command line, parameters, and version).  
- **Keep the evidence chain short** – each hop introduces risk; copy directly to final 
storage when possible.  
- **If storage is a bottleneck**, prioritize: (1) volatile data (memory, network), (2) logs, 
(3) key files, (4) full disk image (only if feasible).  
- **Use read‑only mounts** for the source drive to avoid accidental writes.  
- **Back up the hash list** (`hashes.txt`) on a separate medium; it’s part of the 
evidentiary record.  

---  

## References  

- NIST SP 800‑101 – *Guidelines for Email‑Based Evidence Collection*  
- SANS FOR500 – *Advanced Incident Response, Threat Hunting, and Digital Forensics*  
- **LiME** – Memory Acquisition for Linux: <https://github.com/Velocidex/LiME>  
- **Volatility 3** – <https://github.com/volatilityfoundation/volatility3>  
- **Plaso** – <https://github.com/diggap/plaso>  

---  

