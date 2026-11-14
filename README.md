# pping - by Alon Patrich (yes its a copy of ping)

A lightweight Python implementation of the Windows `ping` utility using raw ICMP sockets. Built from scratch with Python's standard library, `pping` crafts raw ICMP Echo Request packets, calculates 16-bit one's complement checksums, measures round-trip latency, and reports Windows-style ping statistics.

## Features

- **Pure Standard Library:** Uses only built-in Python modules (`socket`, `struct`, `sys`, `time`, `os`) with zero external dependencies.
- **Raw ICMP Packet Crafting:** Builds custom 8-byte ICMP headers (Type `8`, Code `0`) with process-based packet identifiers and sequence tracking.
- **Custom Checksum Calculation:** Implements 16-bit one's complement checksum verification.
- **Detailed Metrics:** Displays per-packet reply size, Round-Trip Time (RTT) in milliseconds, and Time-To-Live (TTL), followed by summary statistics (Sent, Received, Lost %, Min/Max/Average RTT).

## Prerequisites

- **Python 3.6+**
- **Administrator / Root Privileges:** Because `pping` uses raw sockets (`socket.SOCK_RAW`), your operating system requires elevated privileges to run it.

## Installation

Clone or download the script to your local machine:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

## Usage

Open a terminal with **Administrator** (Windows) or **root** (Linux/macOS) privileges and pass the target IP address as the argument:

```bash
# Windows (Run Command Prompt or PowerShell as Administrator)
python pping.py 8.8.8.8

# Linux / macOS
sudo python3 pping.py 8.8.8.8
```

### Example Output

```text
Pinging 8.8.8.8:
Reply from 8.8.8.8: bytes=25 time=14.32ms TTL=117
Reply from 8.8.8.8: bytes=25 time=13.89ms TTL=117
Reply from 8.8.8.8: bytes=25 time=14.10ms TTL=117
Reply from 8.8.8.8: bytes=25 time=13.95ms TTL=117

Ping statistics for 8.8.8.8:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 13.89ms, Maximum = 14.32ms, Average = 14.07ms
```

## Planned / Upcoming Flags

- `-n`: Customize the number of echo requests to send (currently defaults to `4`).
- `-l` / `-p`: Customize the send buffer/packet size in bytes.
- Domain name resolution (allowing hostnames like `google.com` in addition to raw IP addresses).

## Author & License

- **Author:** Alon Patrich
- **Copyright:** Patrich LTD by Alon Patrich
