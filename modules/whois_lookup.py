"""
WHOIS Lookup Module
Performs WHOIS lookups to gather domain registration information
"""

import whois
from datetime import datetime


class WhoisLookup:
    """WHOIS information gathering module"""
    
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        
    def lookup(self):
        """
        Perform WHOIS lookup
        
        Returns:
            dict: WHOIS information
        """
        self.logger.info(f"Performing WHOIS lookup for {self.target}")
        
        results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'whois_data': {}
        }
        
        try:
            w = whois.whois(self.target)
            
            # Extract relevant information
            results['whois_data'] = {
                'domain_name': self._safe_get(w, 'domain_name'),
                'registrar': self._safe_get(w, 'registrar'),
                'creation_date': self._format_date(self._safe_get(w, 'creation_date')),
                'expiration_date': self._format_date(self._safe_get(w, 'expiration_date')),
                'updated_date': self._format_date(self._safe_get(w, 'updated_date')),
                'name_servers': self._safe_get(w, 'name_servers'),
                'status': self._safe_get(w, 'status'),
                'emails': self._safe_get(w, 'emails'),
                'org': self._safe_get(w, 'org'),
                'address': self._safe_get(w, 'address'),
                'city': self._safe_get(w, 'city'),
                'state': self._safe_get(w, 'state'),
                'country': self._safe_get(w, 'country'),
                'registrant_postal_code': self._safe_get(w, 'registrant_postal_code'),
            }
            
            self.logger.success(f"WHOIS lookup completed for {self.target}")
            
        except Exception as e:
            self.logger.error(f"WHOIS lookup failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _safe_get(self, whois_obj, key):
        """Safely get attribute from WHOIS object"""
        try:
            value = getattr(whois_obj, key, None)
            
            # Handle lists
            if isinstance(value, list):
                # Return first non-None value or the whole list
                if value:
                    return value[0] if len(value) == 1 else value
                return None
            
            return value
            
        except:
            return None
    
    def _format_date(self, date_value):
        """Format date value to ISO string"""
        if date_value is None:
            return None
        
        try:
            if isinstance(date_value, list):
                date_value = date_value[0]
            
            if hasattr(date_value, 'isoformat'):
                return date_value.isoformat()
            
            return str(date_value)
            
        except:
            return str(date_value)
