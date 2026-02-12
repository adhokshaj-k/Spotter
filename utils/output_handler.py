"""
Output Handler Module
Handles saving results in multiple formats (JSON, XML, TXT)
"""

import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom


class OutputHandler:
    """Handles output formatting and file saving"""
    
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def save(self, data, filename, format_type="json"):
        """
        Save data to file in specified format
        
        Args:
            data: Data to save
            filename: Base filename (without extension)
            format_type: Output format (json, xml, txt)
        
        Returns:
            str: Path to saved file
        """
        if format_type == "json":
            return self._save_json(data, filename)
        elif format_type == "xml":
            return self._save_xml(data, filename)
        elif format_type == "txt":
            return self._save_txt(data, filename)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _save_json(self, data, filename):
        """Save data as JSON"""
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filepath
    
    def _save_xml(self, data, filename):
        """Save data as XML"""
        filepath = os.path.join(self.output_dir, f"{filename}.xml")
        
        # Create root element
        root = ET.Element('SpotterResults')
        
        # Convert dict to XML
        self._dict_to_xml(root, data)
        
        # Pretty print XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        return filepath
    
    def _save_txt(self, data, filename):
        """Save data as formatted text"""
        filepath = os.path.join(self.output_dir, f"{filename}.txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("SPOTTER RECONNAISSANCE REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            self._write_dict_as_text(f, data)
        
        return filepath
    
    def _dict_to_xml(self, parent, data):
        """Recursively convert dictionary to XML elements"""
        if isinstance(data, dict):
            for key, value in data.items():
                # Sanitize key for XML
                key = str(key).replace(' ', '_').replace('-', '_')
                
                if isinstance(value, list):
                    list_elem = ET.SubElement(parent, key)
                    for item in value:
                        item_elem = ET.SubElement(list_elem, 'item')
                        self._dict_to_xml(item_elem, item)
                elif isinstance(value, dict):
                    child = ET.SubElement(parent, key)
                    self._dict_to_xml(child, value)
                else:
                    child = ET.SubElement(parent, key)
                    child.text = str(value)
        else:
            parent.text = str(data)
    
    def _write_dict_as_text(self, f, data, indent=0):
        """Recursively write dictionary as formatted text"""
        indent_str = "  " * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    f.write(f"{indent_str}{key}:\n")
                    self._write_dict_as_text(f, value, indent + 1)
                elif isinstance(value, list):
                    f.write(f"{indent_str}{key}:\n")
                    for i, item in enumerate(value, 1):
                        if isinstance(item, dict):
                            f.write(f"{indent_str}  [{i}]\n")
                            self._write_dict_as_text(f, item, indent + 2)
                        else:
                            f.write(f"{indent_str}  - {item}\n")
                else:
                    f.write(f"{indent_str}{key}: {value}\n")
        else:
            f.write(f"{indent_str}{data}\n")
