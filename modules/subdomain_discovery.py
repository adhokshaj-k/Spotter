"""
Subdomain Discovery Module
Discovers subdomains using DNS enumeration, brute force, and online sources
"""

import socket
import dns.resolver
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


class SubdomainDiscovery:
    """Subdomain discovery and enumeration module"""
    
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        self.found_subdomains = set()
        
    def discover(self, wordlist=None):
        """
        Discover subdomains
        
        Args:
            wordlist: Path to wordlist file (if None, uses default list)
        
        Returns:
            dict: Discovered subdomains
        """
        self.logger.info(f"Starting subdomain discovery for {self.target}")
        
        results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'subdomains': [],
            'methods_used': []
        }
        
        # Method 1: Common subdomains brute force
        self.logger.info("Brute forcing common subdomains...")
        results['methods_used'].append('brute_force')
        self._brute_force_subdomains(wordlist)
        
        # Method 2: DNS zone transfer attempt
        self.logger.info("Attempting DNS zone transfer...")
        results['methods_used'].append('zone_transfer')
        self._attempt_zone_transfer()
        
        # Method 3: Certificate transparency logs
        self.logger.info("Checking certificate transparency logs...")
        results['methods_used'].append('cert_transparency')
        self._check_cert_transparency()
        
        # Compile results
        for subdomain in sorted(self.found_subdomains):
            ip_address = self._resolve_subdomain(subdomain)
            results['subdomains'].append({
                'subdomain': subdomain,
                'ip_address': ip_address
            })
        
        results['total_found'] = len(results['subdomains'])
        self.logger.success(f"Found {results['total_found']} subdomains")
        
        return results
    
    def _brute_force_subdomains(self, wordlist=None):
        """Brute force subdomains using wordlist"""
        # Default common subdomains
        default_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'webdisk', 'ns', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'mx1',
            'mx2', 'imap', 'pop3', 'admin', 'portal', 'api', 'dev', 'staging', 'test',
            'vpn', 'remote', 'blog', 'shop', 'store', 'mobile', 'm', 'cdn', 'static',
            'assets', 'img', 'images', 'video', 'media', 'download', 'downloads', 'app',
            'apps', 'cloud', 'secure', 'login', 'sso', 'auth', 'support', 'help', 'docs',
            'documentation', 'wiki', 'forum', 'community', 'chat', 'beta', 'alpha', 'demo'
        ]
        
        # Load wordlist if provided
        if wordlist:
            try:
                with open(wordlist, 'r') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
            except Exception as e:
                self.logger.warning(f"Failed to load wordlist: {str(e)}, using defaults")
                subdomains = default_subdomains
        else:
            subdomains = default_subdomains
        
        # Test subdomains concurrently
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(self._test_subdomain, sub): sub 
                for sub in subdomains
            }
            
            for future in as_completed(futures):
                subdomain = future.result()
                if subdomain:
                    self.found_subdomains.add(subdomain)
                    self.logger.info(f"Found subdomain: {subdomain}")
    
    def _test_subdomain(self, subdomain):
        """Test if subdomain exists"""
        full_domain = f"{subdomain}.{self.target}"
        
        try:
            socket.gethostbyname(full_domain)
            return full_domain
        except socket.gaierror:
            return None
    
    def _attempt_zone_transfer(self):
        """Attempt DNS zone transfer (AXFR)"""
        try:
            # Get nameservers
            ns_records = dns.resolver.resolve(self.target, 'NS')
            
            for ns in ns_records:
                ns_address = str(ns)
                self.logger.debug(f"Attempting zone transfer from {ns_address}")
                
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_address, self.target))
                    
                    for name in zone.nodes.keys():
                        subdomain = f"{name}.{self.target}"
                        self.found_subdomains.add(subdomain)
                        self.logger.success(f"Zone transfer successful! Found: {subdomain}")
                        
                except Exception as e:
                    self.logger.debug(f"Zone transfer failed for {ns_address}: {str(e)}")
                    
        except Exception as e:
            self.logger.debug(f"Could not get nameservers: {str(e)}")
    
    def _check_cert_transparency(self):
        """Check certificate transparency logs"""
        try:
            url = f"https://crt.sh/?q=%.{self.target}&output=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for entry in data:
                    name_value = entry.get('name_value', '')
                    
                    # Parse subdomains from certificate
                    for subdomain in name_value.split('\n'):
                        subdomain = subdomain.strip()
                        
                        # Filter valid subdomains
                        if subdomain.endswith(self.target) and '*' not in subdomain:
                            self.found_subdomains.add(subdomain)
                            
        except Exception as e:
            self.logger.debug(f"Certificate transparency check failed: {str(e)}")
    
    def _resolve_subdomain(self, subdomain):
        """Resolve subdomain to IP address"""
        try:
            ip_address = socket.gethostbyname(subdomain)
            return ip_address
        except:
            return 'N/A'
