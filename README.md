# Spotter - Modular Reconnaissance Framework

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**A powerful CLI-based automated enumeration and scanning framework for security professionals**

</div>

## Overview

Spotter is a modular reconnaissance framework designed for automated vulnerability assessment and penetration testing. It provides a comprehensive suite of tools for network enumeration, service detection, and information gathering.

## Features

### Modular Architecture
- **Port Scanner** - Fast multi-threaded port scanning with nmap integration
- **Service Detector** - Banner grabbing and service fingerprinting
- **Subdomain Discovery** - DNS enumeration, brute force, and certificate transparency
- **WHOIS Lookup** - Domain registration and ownership information
- **DNS Enumeration** - Comprehensive DNS record gathering (A, AAAA, MX, NS, TXT, SOA, CNAME, PTR)

### Structured Output
- **JSON** - Machine-readable format for automation
- **XML** - Structured hierarchical output
- **TXT** - Human-readable formatted reports

### Key Capabilities
- ✅ Automated enumeration workflow
- ✅ Concurrent scanning for improved performance
- ✅ Detailed logging with colored output
- ✅ Customizable scan parameters
- ✅ Multiple output formats
- ✅ Verbose debugging mode

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- nmap (optional, for advanced port scanning)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/adhokshaj-k/Spotter.git
cd Spotter
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install nmap (optional but recommended)**
```bash
# Kali Linux / Debian / Ubuntu
sudo apt-get install nmap

# macOS
brew install nmap

# Windows
# Download from https://nmap.org/download.html
```

## Usage

### Basic Syntax
```bash
python spotter.py -t <target> [options]
```

### Quick Start Examples

#### Full Reconnaissance Scan
```bash
python spotter.py -t example.com --full
```

#### Port Scanning
```bash
# Scan common ports (1-1000)
python spotter.py -t example.com --port-scan

# Scan all ports
python spotter.py -t example.com --port-scan -p 1-65535

# Scan specific ports
python spotter.py -t example.com --port-scan -p 80,443,8080,8443
```

#### Service Detection
```bash
# Detect services on common ports
python spotter.py -t example.com --service-detect

# Detect services on specific ports
python spotter.py -t example.com --service-detect --specific-ports 80,443,22
```

#### Subdomain Discovery
```bash
# Use default wordlist
python spotter.py -t example.com --subdomain-discovery

# Use custom wordlist
python spotter.py -t example.com --subdomain-discovery -w /path/to/wordlist.txt
```

#### DNS Enumeration
```bash
python spotter.py -t example.com --dns-enum
```

#### WHOIS Lookup
```bash
python spotter.py -t example.com --whois
```

### Advanced Usage

#### Multiple Modules
```bash
# Run port scan and service detection
python spotter.py -t example.com --port-scan --service-detect

# Run DNS enum and subdomain discovery
python spotter.py -t example.com --dns-enum --subdomain-discovery
```

#### Custom Output
```bash
# Save as XML
python spotter.py -t example.com --full -o xml

# Save as TXT
python spotter.py -t example.com --full -o txt

# Custom output directory
python spotter.py -t example.com --full --output-dir /path/to/results
```

#### Verbose Mode
```bash
# Enable detailed logging
python spotter.py -t example.com --full -v
```

## Command-Line Options

### Required Arguments
| Option | Description |
|--------|-------------|
| `-t, --target` | Target domain or IP address |

### Module Selection
| Option | Description |
|--------|-------------|
| `--full` | Run all reconnaissance modules |
| `--port-scan` | Run port scanning module |
| `--service-detect` | Run service detection module |
| `--subdomain-discovery` | Run subdomain discovery module |
| `--whois` | Run WHOIS lookup module |
| `--dns-enum` | Run DNS enumeration module |

### Module-Specific Options
| Option | Description |
|--------|-------------|
| `-p, --ports` | Port range for scanning (default: 1-1000) |
| `--scan-type` | Port scan type: syn, tcp, udp (default: syn) |
| `-w, --wordlist` | Wordlist file for subdomain discovery |
| `--specific-ports` | Specific ports for service detection (comma-separated) |

### Output Options
| Option | Description |
|--------|-------------|
| `-o, --output-format` | Output format: json, xml, txt (default: json) |
| `--output-dir` | Output directory for results (default: results) |
| `--no-save` | Don't save results to file |

### General Options
| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable verbose output |
| `-h, --help` | Show help message |

## Project Structure

```
Spotter/
├── spotter.py              # Main CLI entry point
├── main.py                 # Legacy script
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── LICENSE                # License file
├── modules/               # Reconnaissance modules
│   ├── __init__.py
│   ├── port_scanner.py    # Port scanning module
│   ├── service_detector.py # Service detection module
│   ├── subdomain_discovery.py # Subdomain enumeration
│   ├── whois_lookup.py    # WHOIS information gathering
│   └── dns_enum.py        # DNS record enumeration
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── logger.py          # Colored logging
│   ├── output_handler.py  # Output formatting
│   └── banner.py          # ASCII banner
└── results/               # Output directory (auto-created)
```

## Module Details

### Port Scanner
- **nmap integration** for fast, accurate scanning
- **Custom TCP/UDP scanner** as fallback
- **Multi-threaded** concurrent scanning
- **Service name resolution** for common ports

### Service Detector
- **Banner grabbing** from open ports
- **Version fingerprinting** from service banners
- **SSL/TLS support** for HTTPS services
- **Protocol detection** for various services

### Subdomain Discovery
- **DNS brute forcing** with customizable wordlists
- **Zone transfer attempts** (AXFR)
- **Certificate transparency** log checking
- **Concurrent subdomain testing**

### WHOIS Lookup
- **Domain registration** information
- **Registrar details**
- **Name server** information
- **Contact information** (when available)

### DNS Enumeration
- **Multiple record types**: A, AAAA, MX, NS, TXT, SOA, CNAME, PTR
- **Comprehensive DNS** information gathering
- **Error handling** for missing records

## Output Examples

### JSON Output
```json
{
  "port_scan": {
    "target": "example.com",
    "scan_type": "syn",
    "open_ports": [
      {
        "port": 80,
        "protocol": "tcp",
        "state": "open",
        "service": "http"
      }
    ]
  }
}
```

### Results Directory
```
results/
├── example_com_20260212_172530.json
├── example_com_20260212_172530.xml
└── example_com_20260212_172530.txt
```

## Legal Disclaimer

**IMPORTANT**: This tool is designed for authorized security testing and educational purposes only.

- ⚠️ Only scan systems you own or have explicit permission to test
- ⚠️ Unauthorized scanning may be illegal in your jurisdiction
- ⚠️ The authors are not responsible for misuse of this tool

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Adhokshaj K**
- GitHub: [@adhokshaj-k](https://github.com/adhokshaj-k)

## Acknowledgments
- Built for educational and professional security testing purposes

---

<div align="center">

</div>
