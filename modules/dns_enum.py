"""
DNS Enumeration Module
Performs comprehensive DNS enumeration including various record types
"""

import dns.resolver
from datetime import datetime


class DNSEnumerator:
    """DNS enumeration and record gathering module"""
    
    def __init__(self, target, logger):
        self.target = target
        self.logger = logger
        
        # DNS record types to query
        self.record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR']
        
    def enumerate(self):
        """
        Enumerate DNS records
        
        Returns:
            dict: DNS enumeration results
        """
        self.logger.info(f"Enumerating DNS records for {self.target}")
        
        results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'records': {}
        }
        
        # Query each record type
        for record_type in self.record_types:
            records = self._query_record_type(record_type)
            if records:
                results['records'][record_type] = records
                self.logger.info(f"Found {len(records)} {record_type} record(s)")
        
        results['total_records'] = sum(len(v) for v in results['records'].values())
        
        self.logger.success(f"DNS enumeration completed. Found {results['total_records']} total records")
        
        return results
    
    def _query_record_type(self, record_type):
        """Query specific DNS record type"""
        records = []
        
        try:
            answers = dns.resolver.resolve(self.target, record_type)
            
            for rdata in answers:
                record_data = self._parse_record(record_type, rdata)
                if record_data:
                    records.append(record_data)
                    
        except dns.resolver.NoAnswer:
            self.logger.debug(f"No {record_type} records found")
        except dns.resolver.NXDOMAIN:
            self.logger.error(f"Domain {self.target} does not exist")
        except dns.resolver.Timeout:
            self.logger.warning(f"DNS query timeout for {record_type} records")
        except Exception as e:
            self.logger.debug(f"Error querying {record_type} records: {str(e)}")
        
        return records
    
    def _parse_record(self, record_type, rdata):
        """Parse DNS record data"""
        try:
            if record_type == 'A':
                return {
                    'type': 'A',
                    'address': str(rdata)
                }
            
            elif record_type == 'AAAA':
                return {
                    'type': 'AAAA',
                    'address': str(rdata)
                }
            
            elif record_type == 'MX':
                return {
                    'type': 'MX',
                    'priority': rdata.preference,
                    'exchange': str(rdata.exchange)
                }
            
            elif record_type == 'NS':
                return {
                    'type': 'NS',
                    'nameserver': str(rdata)
                }
            
            elif record_type == 'TXT':
                return {
                    'type': 'TXT',
                    'text': str(rdata)
                }
            
            elif record_type == 'SOA':
                return {
                    'type': 'SOA',
                    'mname': str(rdata.mname),
                    'rname': str(rdata.rname),
                    'serial': rdata.serial,
                    'refresh': rdata.refresh,
                    'retry': rdata.retry,
                    'expire': rdata.expire,
                    'minimum': rdata.minimum
                }
            
            elif record_type == 'CNAME':
                return {
                    'type': 'CNAME',
                    'target': str(rdata)
                }
            
            elif record_type == 'PTR':
                return {
                    'type': 'PTR',
                    'ptrdname': str(rdata)
                }
            
            else:
                return {
                    'type': record_type,
                    'data': str(rdata)
                }
                
        except Exception as e:
            self.logger.debug(f"Error parsing {record_type} record: {str(e)}")
            return None
