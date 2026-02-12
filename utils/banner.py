"""
Banner Module
Displays ASCII art banner for Spotter
"""

from colorama import Fore, Style


def print_banner():
    """Print Spotter ASCII banner"""
    banner = f"""
{Fore.CYAN}
   _____ ____  ____  ______________________
  / ___// __ \\/ __ \\/_  __/_  __/ ____/ __ \\
  \\__ \\/ /_/ / / / / / /   / / / __/ / /_/ /
 ___/ / ____/ /_/ / / /   / / / /___/ _, _/ 
/____/_/    \\____/ /_/   /_/ /_____/_/ |_|  
{Style.RESET_ALL}
{Fore.GREEN}Modular Reconnaissance Framework v1.0{Style.RESET_ALL}
{Fore.YELLOW}Automated Enumeration & Vulnerability Scanner{Style.RESET_ALL}
{Fore.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
    """
    print(banner)
