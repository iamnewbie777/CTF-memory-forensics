### How to use it

1. **Save the file**  
   ```bash
   mkdir -p scripts
   curl -o scripts/volwrap.py https://your‑server/volwrap.py   # or copy‑paste the code above
   chmod +x scripts/volwrap.py
   ```

2. **Make sure the Volatility binary is on your `$PATH`** (or give the absolute path via 
`--volatility`).  
   The script automatically detects whether you are dealing with Volatility 2 (`-f`) or 
Volatility 3 (`-d`).

3. **Run a command** – examples:

   ```bash
   # List processes from a RAM dump (Volatility 3)
   python scripts/volwrap.py pslist -i mem.dmp -p "Win10x64_1809" --volatility ./vol.py

   # Show network connections (Volatility 2)
   python scripts/volwrap.py netscan -i mem.raw -c "-p 80" --volatility ./vol.py
   ```

4. **Add your own custom arguments** – any extra arguments you place after `-c/--command-args` 
are passed verbatim to the underlying Volatility command, giving you full flexibility while 
keeping the wrapper convenient.

---

**That’s it!**  
Drop the script into `scripts/`, make it executable, and you now have a quick‑triage helper for 
the most common Volatility tasks. Happy forensics!

