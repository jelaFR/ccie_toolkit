from yaml import load, Loader

class CMLLab:
    ID_LABEL_MAPPING = dict()

    def __init__(self, cml_lab_file=""):
        # Get file and values
        self.cml_lab_file = cml_lab_file
        self._parse_cml_yaml()

        # Extract content of the yaml file
        self._set_lab_attributes()  # Set CML lab attributes
        self.links_list = self._get_infos_in_list(self.cml_content.get("links",""), CMLLinks)  # Get params from YAML file for links
        self.nodes_list = self._get_infos_in_list(self.cml_content.get("nodes",""), CMLNodes)  # Get params from YAML file for nodes

    def display_nodes(self):
        message = f"[INFO] CML Lab {getattr(self, 'title', '')} nodes list"
        print(f"{'#'*len(message)}\n{message}\n{'#'*len(message)}")
        for node_id, node in enumerate(self.nodes_list):
            print(f"{node_id}. {getattr(node, 'label', '')}")

    def _set_lab_attributes(self):
        try:
            for key, value in self.cml_content.get("lab","").items():
                setattr(self, key, value)
        except:
            raise CMLInvalidFileError()

    def _id_to_label(self):
        if not CMLLab.ID_LABEL_MAPPING.get(self.id):
            CMLLab.ID_LABEL_MAPPING[self.id] = self.label

    def _set_attribs(self, item_params):
        for key, value in item_params.items():
            setattr(self, key, value)

    def _parse_cml_yaml(self):
        try:
            yaml_file = open(self.cml_lab_file, "r")
        except:
            raise CMLReadError()
        setattr(self, "cml_content", load(yaml_file, Loader=Loader))

    def _get_infos_in_list(self, list_name, object_type):
        object_list = list()
        for items in list_name:
            object_list.append(object_type(items))
        return object_list

    def __str__(self):
        class_name = self.__class__.__name__  #Polymorphism practice
        return f"Object: {class_name}"

    def __repr__(self):  # Duck typing practice
        class_name = self.__class__.__name__
        if hasattr(self, "title"):  # This is a CML LAB
            return f'CML_Lab:{getattr(self, "title", "")}'
        elif hasattr(self, "node_definition"):  # This is a CML node
            return f'CML_node:{getattr(self, "label", "")}'
        elif hasattr(self, "i1"):  # This is a CML Link
            node1_id = self.ID_LABEL_MAPPING.get(getattr(self, "n1"))
            node1_iface = self.ID_LABEL_MAPPING.get(getattr(self, "i1"))
            node2_id = self.ID_LABEL_MAPPING.get(getattr(self, "n2"))
            node2_iface = self.ID_LABEL_MAPPING.get(getattr(self, "i2"))
            return f'CML_link: {node1_id}({node1_iface}) <-> {node2_id}({node2_iface})'
        elif hasattr(self, "type"):  # This is an interface from CML node
            return f'CML_node iface:{getattr(self, "label","")}'


class CMLLinks(CMLLab):
    def __init__(self, links_params):
        # Initiate link variables
        self._set_attribs(links_params)


class CMLNodes(CMLLab):
    def __init__(self, nodes_params):
        # Initiate node variables
        self._set_attribs(nodes_params)
        self.ifaces_list = self._get_infos_in_list(getattr(self, "interfaces", ""), CMLIface)
        self._id_to_label()


class CMLIface(CMLNodes):
    def __init__(self, nodes_iface_params):
        self._set_attribs(nodes_iface_params)
        self._id_to_label()


""" Exceptions """
class CMLReadError:
    def __init__(self):
        print(f"[ERROR] CMLReadError -> Unable to open YAML file")
        exit(0)

class CMLInvalidFileError:
    def __init(self):
        print(f"[ERROR] CMLInvalidFileError -> This YAML file is not a valid Cisco CML configuration file")
        exit(0)
