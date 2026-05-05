
## Cloud VMs Workflow  

### 1️⃣ Preparation  

- **Identify the VM** (instance ID, region, owner).  
- **Notify the cloud provider** (if required) and obtain any needed API keys or temporary 
credentials.  
- **Create a secure workspace** on your IR laptop (e.g., an encrypted folder, 
`~/ir/cloud_vm_<timestamp>`).  

### 2️⃣ Evidence Collection  

| Step | Action | Command / Tool | Notes |
|------|--------|----------------|-------|
| **2.1** | Capture VM metadata & configuration | Cloud provider CLI (`aws ec2 
describe-instances`, `gcloud compute instances describe`, Azure CLI) | Store JSON/YAML in 
`metadata/` |
| **2.2** | Export system logs (guest) | - Linux: `tar czf /tmp/logs.tar.gz /var/log`  <br> 
- Windows: zip `C:\Windows\System32\winevt\Logs` | Use the guest agent if available (e.g., 
AWS SSM, Azure VM Agent) |
| **2.3** | Take a **snapshot** (point‑in‑time) | Cloud console or CLI (`aws ec2 
create-snapshot`, `gcloud compute disks snapshot`) | Snapshot is the primary forensic image; 
keep the snapshot ID |
| **2.4** | Acquire **memory dump** (if agent permits) | - Linux: `sudo dd if=/dev/mem 
of=/tmp/memory.dump bs=1M`  <br> - Windows: `procdump -ma <pid> C:\temp\mem.dmp` | If no 
agent, consider a **live‑capture** using `LiME` (Linux) or `Volatility`‑compatible tools 
that run inside the VM |
| **2.5** | Collect **network capture** | `tcpdump -i eth0 -w /tmp/traffic.pcap` (Linux)  
<br> `netsh trace start capture=yes tracefile=C:\temp\traffic.etl` (Windows) | Limit capture 
duration (e.g., 5‑10 min) to stay within bandwidth limits |
| **2.6** | Gather **process & privilege** info | `ps -auxf` (Linux)  <br> `Get-Process | 
Format-List` (PowerShell)  <br> `whoami /all` (Windows) | Save to `processes/` |
| **2.7** | Extract **mounted filesystems** & **disk usage** | `df -h` (Linux)  <br> 
`Get-PSDrive` (PowerShell) | Record sizes; note any unusual mounts (e.g., `/tmp`, attached 
volumes) |
| **2.8** | Securely delete temporary files on the VM (if required) | `shred -u /tmp/*` 
(Linux)  <br> `cipher /w:C:` (Windows) | Do **not** delete evidence before you have saved it 
elsewhere. |

### 3️⃣ Post‑Collection  

- **Hash every artifact** (`sha256sum <file>` or `CertUtil -hashfile <file> SHA256`). Store 
hashes in `hashes.txt`.  
- **Document timestamps** (UTC) for each collection step.  
- **Upload** the evidence bundle to a secure, immutable storage (e.g., AWS S3 with Object 
Lock, Azure Blob with immutability policy).  

---  

