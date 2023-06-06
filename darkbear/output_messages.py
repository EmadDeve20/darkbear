# format of the reports_types:
# { name of a test function:  {type, description} }

reports_types = {
    "package_manager_test": {"type": "suspicious", "description": "this server does not have a package manager! maybe this is a not real Linux like cowrie"},
    "chrooted_test": {"type": "very suspicious", "description": "this is very suspicious because the current directory is chrooted!"},
}