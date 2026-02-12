#!/usr/bin/env python3
"""
Spotter - Modular Reconnaissance Framework
A CLI-based automated enumeration and scanning tool
"""

import argparse
import sys
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import modules
from modules.port_scanner import PortScanner
from modules.service_detector import ServiceDetector
from modules.subdomain_discovery import SubdomainDiscovery
from modules.whois_lookup import WhoisLookup
from modules.dns_enum import DNSEnumerator
from utils.logger import Logger
from utils.output_handler import OutputHandler
from utils.banner import print_banner

class Spotter:
    """Main Spotter reconnaissance framework class"""
    
    def __init__(self, target, output_dir="results", verbose=False):
        self.target = target
        self.output_dir = output_dir
        self.verbose = verbose
        self.logger = Logger(verbose=verbose)
        self.results = {}
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def run_port_scan(self, ports="1-1000", scan_type="syn"):
        """Execute port scanning module"""
        self.logger.info(f"Starting port scan on {self.target}")
        scanner = PortScanner(self.target, self.logger)
        results = scanner.scan(ports=ports, scan_type=scan_type)
        self.results['port_scan'] = results
        return results
    
    def run_service_detection(self, ports=None):
        """Execute service detection module"""
        self.logger.info(f"Starting service detection on {self.target}")
        detector = ServiceDetector(self.target, self.logger)
        results = detector.detect(ports=ports)
        self.results['service_detection'] = results
        return results
    
    def run_subdomain_discovery(self, wordlist=None):
        """Execute subdomain discovery module"""
        self.logger.info(f"Starting subdomain discovery for {self.target}")
        discovery = SubdomainDiscovery(self.target, self.logger)
        results = discovery.discover(wordlist=wordlist)
        self.results['subdomain_discovery'] = results
        return results
    
    def run_whois_lookup(self):
        """Execute WHOIS lookup module"""
        self.logger.info(f"Starting WHOIS lookup for {self.target}")
        whois_lookup = WhoisLookup(self.target, self.logger)
        results = whois_lookup.lookup()
        self.results['whois'] = results
        return results
    
    def run_dns_enumeration(self):
        """Execute DNS enumeration module"""
        self.logger.info(f"Starting DNS enumeration for {self.target}")
        dns_enum = DNSEnumerator(self.target, self.logger)
        results = dns_enum.enumerate()
        self.results['dns_enumeration'] = results
        return results
    
    def run_full_scan(self):
        """Execute all reconnaissance modules"""
        self.logger.info(f"Starting full reconnaissance scan on {self.target}")
        
        # Run all modules
        self.run_whois_lookup()
        self.run_dns_enumeration()
        self.run_port_scan()
        self.run_service_detection()
        self.run_subdomain_discovery()
        
        return self.results
    
    def save_results(self, output_format="json"):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.target.replace('.', '_')}_{timestamp}"
        
        output_handler = OutputHandler(self.output_dir)
        filepath = output_handler.save(self.results, filename, output_format)
        
        self.logger.success(f"Results saved to: {filepath}")
        return filepath


def main():
    """Main CLI entry point"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Spotter - Modular Reconnaissance Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full scan with all modules
  python spotter.py -t example.com --full
  
  # Port scan only
  python spotter.py -t example.com --port-scan -p 1-65535
  
  # Service detection on specific ports
  python spotter.py -t example.com --service-detect --ports 80,443,8080
  
  # Subdomain discovery with custom wordlist
  python spotter.py -t example.com --subdomain-discovery -w wordlist.txt
  
  # Multiple modules with JSON output
  python spotter.py -t example.com --port-scan --dns-enum -o json
        """
    )
    
    # Target options
    parser.add_argument("-t", "--target", required=True, help="Target domain or IP address")
    
    # Module selection
    parser.add_argument("--full", action="store_true", help="Run all reconnaissance modules")
    parser.add_argument("--port-scan", action="store_true", help="Run port scanning module")
    parser.add_argument("--service-detect", action="store_true", help="Run service detection module")
    parser.add_argument("--subdomain-discovery", action="store_true", help="Run subdomain discovery module")
    parser.add_argument("--whois", action="store_true", help="Run WHOIS lookup module")
    parser.add_argument("--dns-enum", action="store_true", help="Run DNS enumeration module")
    
    # Module-specific options
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range for scanning (default: 1-1000)")
    parser.add_argument("--scan-type", choices=["syn", "tcp", "udp"], default="syn", help="Port scan type (default: syn)")
    parser.add_argument("-w", "--wordlist", help="Wordlist file for subdomain discovery")
    parser.add_argument("--specific-ports", help="Specific ports for service detection (comma-separated)")
    
    # Output options
    parser.add_argument("-o", "--output-format", choices=["json", "xml", "txt"], default="json", help="Output format (default: json)")
    parser.add_argument("--output-dir", default="results", help="Output directory for results (default: results)")
    
    # General options
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to file")
    
    args = parser.parse_args()
    
    # Validate target
    if not args.target:
        print(f"{Fore.RED}[!] Error: Target is required{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)
    
    # Check if at least one module is selected
    if not any([args.full, args.port_scan, args.service_detect, args.subdomain_discovery, args.whois, args.dns_enum]):
        print(f"{Fore.YELLOW}[!] Warning: No modules selected. Use --full or specify individual modules.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)
    
    # Initialize Spotter
    spotter = Spotter(
        target=args.target,
        output_dir=args.output_dir,
        verbose=args.verbose
    )
    
    try:
        # Run selected modules
        if args.full:
            spotter.run_full_scan()
        else:
            if args.whois:
                spotter.run_whois_lookup()
            
            if args.dns_enum:
                spotter.run_dns_enumeration()
            
            if args.port_scan:
                spotter.run_port_scan(ports=args.ports, scan_type=args.scan_type)
            
            if args.service_detect:
                ports = args.specific_ports.split(',') if args.specific_ports else None
                spotter.run_service_detection(ports=ports)
            
            if args.subdomain_discovery:
                spotter.run_subdomain_discovery(wordlist=args.wordlist)
        
        # Save results
        if not args.no_save:
            spotter.save_results(output_format=args.output_format)
        
        print(f"\n{Fore.GREEN}[✓] Reconnaissance completed successfully!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
