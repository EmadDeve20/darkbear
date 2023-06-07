# format of the reports_types:
# { name of a test function:  {type, description} }

reports_types = {
    "package_manager_test": {"type": "suspicious", "description": "this server does not have a package manager! maybe this is a not real Linux like cowrie"},
    "chrooted_test": {"type": "very suspicious", "description": "this is very suspicious because the current directory is chrooted!"},
    "network_macaddress_test": {"type": "very suspicious", "description": "The physical address of the server's network ports is for the virtual machine! The Server is a virtual machine!"},
    "usb_virtual_machine_test": {"type": "suspicious", "description": "the some name of the USB device on the server has the word Virtual! so the server can be a Virtual Machine!"},
}