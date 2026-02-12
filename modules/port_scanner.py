"""
Port Scanner Module
Performs port scanning using nmap integration and custom TCP/UDP scanning
"""

import socket
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class PortScanner:
    """Port scanning module with multiple scan types"""
    
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.open_ports = []
        
    def scan(self, ports="1-1000", scan_type="syn"):
        """
        Main scan method
        
        Args:
            ports: Port range (e.g., "1-1000" or "80,443,8080")
            scan_type: Type of scan (syn, tcp, udp)
        
        Returns:
            dict: Scan results with open ports and details
        """
        self.logger.info(f"Scanning ports {ports} on {self.target} using {scan_type} scan")
        
        results = {
            'target': self.target,
            'scan_type': scan_type,
            'port_range': ports,
            'timestamp': datetime.now().isoformat(),
            'open_ports': [],
            'scan_method': 'nmap' if self._check_nmap() else 'custom'
        }
        
        # Try nmap first, fall back to custom scanner
        if self._check_nmap() and scan_type == "syn":
            results['open_ports'] = self._nmap_scan(ports)
        else:
            results['open_ports'] = self._custom_scan(ports, scan_type)
        
        results['total_open_ports'] = len(results['open_ports'])
        
        self.logger.success(f"Found {results['total_open_ports']} open ports")
        return results
    
    def _check_nmap(self):
        """Check if nmap is available"""
        try:
            subprocess.run(['nmap', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("nmap not found, using custom scanner")
            return False
    
    def _nmap_scan(self, ports):
        """Perform nmap scan"""
        try:
            self.logger.info("Using nmap for port scanning")
            
            # Build nmap command
            cmd = [
                'nmap',
                '-p', ports,
                '-T4',  # Aggressive timing
                '--open',  # Only show open ports
                '-oX', '-',  # XML output to stdout
                self.target
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Parse nmap XML output
            return self._parse_nmap_output(result.stdout)
            
        except subprocess.TimeoutExpired:
            self.logger.error("nmap scan timed out")
            return []
        except Exception as e:
            self.logger.error(f"nmap scan failed: {str(e)}")
            return []
    
    def _parse_nmap_output(self, xml_output):
        """Parse nmap XML output"""
        import xml.etree.ElementTree as ET
        
        open_ports = []
        
        try:
            root = ET.fromstring(xml_output)
            
            for port in root.findall('.//port'):
                state = port.find('state')
                if state is not None and state.get('state') == 'open':
                    port_id = port.get('portid')
                    protocol = port.get('protocol')
                    
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else 'unknown'
                    
                    open_ports.append({
                        'port': int(port_id),
                        'protocol': protocol,
                        'state': 'open',
                        'service': service_name
                    })
            
        except ET.ParseError as e:
            self.logger.error(f"Failed to parse nmap output: {str(e)}")
        
        return open_ports
    
    def _custom_scan(self, ports, scan_type):
        """Custom port scanner using raw sockets"""
        self.logger.info("Using custom port scanner")
        
        # Parse port range
        port_list = self._parse_port_range(ports)
        
        # Scan ports concurrently
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {
                executor.submit(self._scan_port, port, scan_type): port 
                for port in port_list
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    self.logger.info(f"Port {result['port']} is open")
        
        return sorted(open_ports, key=lambda x: x['port'])
    
    def _parse_port_range(self, ports):
        """Parse port range string into list of ports"""
        port_list = []
        
        for part in ports.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                port_list.extend(range(start, end + 1))
            else:
                port_list.append(int(part))
        
        return port_list
    
    def _scan_port(self, port, scan_type):
        """Scan a single port"""
        try:
            if scan_type in ['tcp', 'syn']:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                result = sock.connect_ex((self.target, port))
                sock.close()
                
                if result == 0:
                    return {
                        'port': port,
                        'protocol': 'tcp',
                        'state': 'open',
                        'service': self._get_service_name(port)
                    }
            
            elif scan_type == 'udp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                
                try:
                    sock.sendto(b'', (self.target, port))
                    sock.recvfrom(1024)
                    sock.close()
                    
                    return {
                        'port': port,
                        'protocol': 'udp',
                        'state': 'open',
                        'service': self._get_service_name(port)
                    }
                except socket.timeout:
                    # UDP port might be open (no response)
                    sock.close()
                    return None
                
        except Exception:
            pass
        
        return None
    
    def _get_service_name(self, port):
        """Get common service name for port"""
        common_ports = {
            20: 'ftp-data', 21: 'ftp', 22: 'ssh', 23: 'telnet',
            25: 'smtp', 53: 'dns', 80: 'http', 110: 'pop3',
            143: 'imap', 443: 'https', 445: 'smb', 3306: 'mysql',
            3389: 'rdp', 5432: 'postgresql', 5900: 'vnc', 8080: 'http-proxy',
            8443: 'https-alt', 27017: 'mongodb', 6379: 'redis'
        }
        
        return common_ports.get(port, 'unknown')
