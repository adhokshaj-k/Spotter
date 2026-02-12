"""
Service Detection Module
Detects services running on open ports using banner grabbing and fingerprinting
"""

import socket
import ssl
import re
from datetime import datetime


class ServiceDetector:
    """Service detection and banner grabbing module"""
    
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        
    def detect(self, ports=None):
        """
        Detect services on specified ports
        
        Args:
            ports: List of ports to check (if None, uses common ports)
        
        Returns:
            dict: Service detection results
        """
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
        
        self.logger.info(f"Detecting services on {len(ports)} ports")
        
        results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'services': []
        }
        
        for port in ports:
            service_info = self._detect_service(port)
            if service_info:
                results['services'].append(service_info)
                self.logger.info(f"Detected {service_info['service']} on port {port}")
        
        results['total_services'] = len(results['services'])
        
        return results
    
    def _detect_service(self, port):
        """Detect service on a specific port"""
        try:
            # Check if port is open
            if not self._is_port_open(port):
                return None
            
            # Get banner
            banner = self._grab_banner(port)
            
            # Analyze banner
            service_info = {
                'port': port,
                'state': 'open',
                'service': self._identify_service(port, banner),
                'banner': banner,
                'version': self._extract_version(banner)
            }
            
            return service_info
            
        except Exception as e:
            self.logger.debug(f"Error detecting service on port {port}: {str(e)}")
            return None
    
    def _is_port_open(self, port):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _grab_banner(self, port):
        """Grab banner from service"""
        banner = ""
        
        try:
            # Try standard banner grab
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, port))
            
            # For HTTP/HTTPS, send HTTP request
            if port in [80, 8080, 8000, 8888]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
            elif port in [443, 8443]:
                # Wrap with SSL for HTTPS
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    ssock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                    banner = ssock.recv(1024).decode('utf-8', errors='ignore')
                    return banner
            
            # Receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
        except Exception as e:
            self.logger.debug(f"Banner grab failed for port {port}: {str(e)}")
        
        return banner.strip()
    
    def _identify_service(self, port, banner):
        """Identify service based on port and banner"""
        # Port-based identification
        port_services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6379: 'Redis',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt',
            27017: 'MongoDB'
        }
        
        # Banner-based identification
        if banner:
            banner_lower = banner.lower()
            
            if 'ssh' in banner_lower:
                return 'SSH'
            elif 'ftp' in banner_lower:
                return 'FTP'
            elif 'smtp' in banner_lower or 'mail' in banner_lower:
                return 'SMTP'
            elif 'http' in banner_lower or 'apache' in banner_lower or 'nginx' in banner_lower:
                return 'HTTP'
            elif 'mysql' in banner_lower:
                return 'MySQL'
            elif 'postgresql' in banner_lower or 'postgres' in banner_lower:
                return 'PostgreSQL'
            elif 'redis' in banner_lower:
                return 'Redis'
            elif 'mongodb' in banner_lower or 'mongo' in banner_lower:
                return 'MongoDB'
        
        # Fall back to port-based identification
        return port_services.get(port, 'Unknown')
    
    def _extract_version(self, banner):
        """Extract version information from banner"""
        if not banner:
            return 'Unknown'
        
        # Common version patterns
        patterns = [
            r'(\d+\.\d+\.\d+)',  # x.x.x
            r'(\d+\.\d+)',        # x.x
            r'[vV]ersion[:\s]+([^\s]+)',
            r'[vV]([0-9.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, banner)
            if match:
                return match.group(1)
        
        # Return first line of banner if no version found
        first_line = banner.split('\n')[0][:50]
        return first_line if first_line else 'Unknown'
