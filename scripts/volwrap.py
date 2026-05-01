#!/usr/bin/env python3
"""
volwrap.py – Simple wrapper for common Volatility commands.

Usage
-----
    python volwrap.py <command> [options]

Commands
--------
    pslist      : list processes
    netscan     : network connections
    filescan    : file system scan
    malfind     : find suspicious code
    strings     : extract printable strings
    imagescan   : scan for known image hashes
    --version   : show Volatility version and exit

All commands accept a `--volatility` argument that points to the
Volatility executable (default: `volatility`).  The script automatically
adds the appropriate version flag (`-f` for Volatility 2 or `-d` for
Volatility 3) based on the version it detects.

Example
-------
    # List processes from a RAM dump (Volatility 3)
    python volwrap.py pslist -d -c 0x0000000000123456 --volatility ./vol.py

    # Show network connections from a memory image (Volatility 2)
    python volwrap.py netscan -f mem.dmp -p 80 --volatility ./vol.py
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def detect_volatility_version(vol_path: Path) -> str:
    """
    Detect whether the supplied Volatility binary is Volatility 2 or 3.
    Returns the appropriate command‑line flag for the `--help` style argument.
    """
    if not vol_path.is_file():
        raise FileNotFoundError(f"Volatility executable not found: {vol_path}")

    # Try Volatility 3 first (the `--help` output contains "Volatility 3")
    try:
        result = subprocess.run(
            [str(vol_path), "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if "Volatility 3" in result.stdout:
            return "-d"          # Volatility 3 uses `-d <profile>`
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fall back to Volatility 2 (uses `-f <raw_image>`)
    try:
        result = subprocess.run(
            [str(vol_path), "-h"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if "Volatility 2" in result.stdout:
            return "-f"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # If we get here, we couldn't reliably detect – default to Volatility 2 flag
    return "-f"


def run_command(cmd: list[str]) -> str:
    """Run a command and return its stdout (decoded). Raises on error."""
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return completed.stdout.strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"[!] Command failed: {' '.join(cmd)}\n")
        sys.stderr.write(f"[!] Return code: {e.returncode}\n")
        sys.stderr.write(f"[!] stderr: {e.stderr}\n")
        sys.exit(1)


# --------------------------------------------------------------------------- #
# Command implementations
# --------------------------------------------------------------------------- #
def cmd_pslist(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    profile = args.profile
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]

    if profile:
        cmd += ["-p", profile]
    cmd += ["pslist"]

    output = run_command(cmd)
    print(output)


def cmd_netscan(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]
    cmd += ["netscan"]
    output = run_command(cmd)
    print(output)


def cmd_filescan(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]
    cmd += ["filescan"]
    output = run_command(cmd)
    print(output)


def cmd_malfind(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]
    cmd += ["malfind"]
    output = run_command(cmd)
    print(output)


def cmd_strings(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]
    cmd += ["strings"]
    output = run_command(cmd)
    print(output)


def cmd_imagescan(args: argparse.Namespace) -> None:
    vol_flag = args.volatility_flag
    image = args.image

    cmd = [
        str(args.volatility),
        vol_flag,
        image,
    ]
    cmd += ["imagescan"]
    output = run_command(cmd)
    print(output)


# --------------------------------------------------------------------------- #
# Argument parsing
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Thin wrapper for common Volatility commands.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=[
            "pslist",
            "netscan",
            "filescan",
            "malfind",
            "strings",
            "imagescan",
        ],
        help="Volatility command to invoke.",
    )

    # Arguments that are common to *all* commands
    parser.add_argument(
        "-c",
        "--command-args",
        help=(
            "Space‑separated string of additional arguments that should be passed "
            "directly to the underlying Volatility command (e.g. '-p 0x...' for pslist)."
        ),
    )
    parser.add_argument(
        "-i",
        "--image",
        required=True,
        help="Path to the memory image (raw or E01).",
    )
    parser.add_argument(
        "-p",
        "--profile",
        help="Volatility profile (only needed for Volatility 3).",
    )
    parser.add_argument(
        "--volatility",
        default="volatility",
        help="Path to the Volatility executable (default: 'volatility').",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print Volatility version and exit.",
    )
    return parser


def parse_extra_args(extra: str) -> list[str]:
    """
    Convert a space‑separated string into a list of arguments.
    Handles quoted substrings correctly.
    """
    if not extra:
        return []
    # Using shlex.split makes it robust to quoting.
    import shlex
    return shlex.split(extra)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # ------------------------------------------------------------------- #
    # Version flag short‑circuit
    # ------------------------------------------------------------------- #
    if args.version:
        # Try to locate the version using the same detection logic as below.
        vol_path = Path(args.volatility).expanduser().resolve()
        try:
            result = subprocess.run(
                [str(vol_path), "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            print(result.stdout.strip())
        except Exception:
            # Fallback – maybe the binary is not executable or we can't run it.
            print("Unable to determine Volatility version.")
        sys.exit(0)

    # ------------------------------------------------------------------- #
    # Resolve Volatility flag based on version detection
    # ------------------------------------------------------------------- #
    vol_path = Path(args.volatility).expanduser().resolve()
    try:
        volatility_flag = detect_volatility_version(vol_path)
    except Exception as exc:
        sys.stderr.write(f"[!] Could not detect Volatility version: {exc}\n")
        sys.exit(1)

    # Store the flag for easy access by the command handlers
    # (we attach it as an attribute on the args object)
    args.volatility_flag = volatility_flag

    # Parse any extra arguments the user wants to forward to Volatility
    extra_args = parse_extra_args(args.command_args)
    # Insert the extra args *after* the mandatory image argument (Volatility expects image 
first)
    # We'll let each command handler re‑assemble the command list.
    # ------------------------------------------------------------------- #
    # Dispatch to the appropriate command implementation
    # ------------------------------------------------------------------- #
    if args.command == "pslist":
        cmd_pslist(args)
    elif args.command == "netscan":
        cmd_netscan(args)
    elif args.command == "filescan":
        cmd_filescan(args)
    elif args.command == "malfind":
        cmd_malfind(args)
    elif args.command == "strings":
        cmd_strings(args)
    elif args.command == "imagescan":
        cmd_imagescan(args)


if __name__ == "__main__":
    # Ensure the script is executed with the same Python version that
    # installed any required third‑party packages (none required beyond stdlib).
    main()

