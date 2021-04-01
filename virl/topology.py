import xml.etree.ElementTree as ET
import os
from urllib.request import urlopen


class VIRL_Topology:
    """Represent VIRL topology file"""

    def __init__(self, virl_filename):
        """Initiate new VIRL topology
        Args:
            virl_filename (str): Full path of the VIRL topology file
        """
        self.virl_filename = virl_filename


    def get_nodes_list(self):
        """Get nodes from VIRL topology file"""
        nodes_list = list()
        # Check if XML is valid
        try:
            virl_tree = ET.parse(self.virl_filename)
            virl_root = virl_tree.getroot()
        except:
            print("[ERROR] This is not a valid VIRL topology file")
        # Parse XML topology looking for nodes
        for xml_item in virl_root:
            if xml_item.tag == "{http://www.cisco.com/VIRL}node":
                # Get node global parameters
                node_name = xml_item.attrib["name"]
                node_type = xml_item.attrib["type"]
                node_subtype = xml_item.attrib["subtype"]
                node_location = xml_item.attrib["location"]
                node_ifaces = list()
                # Parse XML looking for : node config, node interfaces mapping
                for item in xml_item:
                    if item.tag == "{http://www.cisco.com/VIRL}extensions":
                        for subitem in item:
                            if subitem.attrib == {'key': 'config', 'type': 'string'}:
                                node_config = subitem.text  # Collect IOS configuration
                            elif subitem.attrib == {'key': 'static_ip', 'type': 'String'}:
                                node_ip = subitem.text
                    elif item.tag == "{http://www.cisco.com/VIRL}interface":
                        node_ifaces.append(VIRL_node_iface(item.attrib.get("id",""), item.attrib.get("name","")))
                nodes_list.append(VIRL_node(node_name, node_type, \
                    node_subtype, node_location, node_config, node_ifaces, node_ip))
        return nodes_list


class VIRL_node:
    """VIRL node"""

    def __init__(self, name, node_type, subtype, location, config, interfaces, ip_address):
        """Initiate VIRL node

        Args:
            node_params (dict): VIRL node parameters ordered in dict
        """
        self.name = name
        self.node_type = node_type
        self.subtype = subtype
        self.location = location
        self.config = config
        self.interfaces = interfaces
        self.ip_address = ip_address


class VIRL_node_iface:
    def __init__(self, iface_id, iface_name):
        self.iface_id = iface_id
        self.iface_name = iface_name
