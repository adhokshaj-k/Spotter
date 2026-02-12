"""
Logger Module
Provides colored logging functionality for Spotter
"""

from colorama import Fore, Style
from datetime import datetime


class Logger:
    """Custom logger with colored output"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def info(self, message):
        """Log info message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.CYAN}[{timestamp}] [*]{Style.RESET_ALL} {message}")
    
    def success(self, message):
        """Log success message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}[{timestamp}] [✓]{Style.RESET_ALL} {message}")
    
    def warning(self, message):
        """Log warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.YELLOW}[{timestamp}] [!]{Style.RESET_ALL} {message}")
    
    def error(self, message):
        """Log error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.RED}[{timestamp}] [✗]{Style.RESET_ALL} {message}")
    
    def debug(self, message):
        """Log debug message (only in verbose mode)"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{Fore.MAGENTA}[{timestamp}] [DEBUG]{Style.RESET_ALL} {message}")
    
    def critical(self, message):
        """Log critical message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.RED}{Style.BRIGHT}[{timestamp}] [CRITICAL]{Style.RESET_ALL} {message}")
