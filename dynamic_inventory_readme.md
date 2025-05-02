
# Dynamic Inventory Generator - README

## Overview

This script generates a dynamic Ansible inventory file from a CSV file containing host information. It checks if the ports specified for each host are open using Nmap and generates an inventory in YAML format that can be used directly by Ansible.

Additionally, if any hosts are unreachable or have closed ports, they are recorded in a separate CSV file for further investigation.

## Features

- **Dynamic Inventory Generation**: The script reads host information from a CSV file and creates a dynamic YAML inventory file for Ansible.
- **Port Checking**: It uses Nmap to check if the specified ports are open on each host.
- **Unreachable Hosts Logging**: If hosts are unreachable (i.e., their ports are closed or unreachable), their details are saved in a separate CSV file.
- **Customizable SSH Credentials**: The script supports setting custom SSH credentials and sudo password for accessing hosts.

## Requirements

- Python 3.x
- `nmap` library (for port scanning)
- `pyyaml` library (for YAML output)
- `csv` and `re` (standard Python libraries)

You can install the required libraries using `pip`:

```bash
pip install python-nmap pyyaml
```

## Usage

### Input CSV Format

The script expects a CSV file with the following columns:

- `BPO NAME`: Name of the BPO or group (used to create the group in the inventory).
- `Primary IP`: IP address of the primary server.
- `Primary Port`: Port of the primary server.
- `Secondary IP`: IP address of the secondary server.
- `Secondary Port`: Port of the secondary server.

Example:

```csv
BPO NAME,Primary IP,Primary Port,Secondary IP,Secondary Port
Group A,192.168.1.1,22,192.168.1.2,22
Group B,192.168.2.1,22,, 
```

### Running the Script

Run the script with the input CSV file as an argument:

```bash
python dynamic_inventory.py /path/to/hosts.csv
```

If no file path is provided, it defaults to `./hosts.csv`.

### Output

1. **YAML Inventory File**: A dynamic inventory in YAML format will be created with the following structure:

```yaml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    ansible_python_interpreter: /usr/bin/python3
    ansible_ssh_user: yourUserName
    ansible_ssh_password: yourPassword
    ansible_become_pass: yourSudoPassword
    ansible_become_method: sudo
    ansible_become: true
    ansible_become_ask_pass: false
  children:
    group_A:
      hosts:
        group_A_host:
          ansible_host: 192.168.1.1
          ansible_port: 22
    group_B:
      hosts:
        group_B_host:
          ansible_host: 192.168.2.1
          ansible_port: 22
```

The YAML file is named based on the input CSV file, with a `.yml` extension.

2. **Unreachable Hosts CSV**: If any hosts are unreachable (due to closed ports or network issues), their details are written to a separate CSV file. The CSV file will have the same name as the input file with `_unreachable` appended to it:

```csv
BPO NAME,Primary IP,Primary Port,Secondary IP,Secondary Port
Group C,192.168.3.1,22,192.168.3.2,22
```

### Customizing SSH Credentials

You can customize the SSH credentials for Ansible in the `inventory['all']['vars']` section:

```python
'inventory': {
    'vars': {
        'ansible_ssh_user': 'yourUserName',
        'ansible_ssh_password': 'yourPassword',
        'ansible_become_pass': 'yourSudoPassword',
        # other variables
    }
}
```

Ensure the credentials are correctly set before running the script.

## Script Details

### Key Functions

1. **`sanitize(name)`**: Sanitizes the BPO group name to make it suitable for use in YAML (replaces non-alphanumeric characters with underscores).
   
2. **`is_port_open(ip, port)`**: Uses Nmap to check if the specified port on a host is open.

3. **`generate_inventory(input_file)`**: Main function that processes the CSV file, performs port checks, and generates the inventory YAML file.

### Example Execution

For an input CSV file `hosts.csv`:

```csv
BPO NAME,Primary IP,Primary Port,Secondary IP,Secondary Port
Group A,192.168.1.1,22,192.168.1.2,22
Group B,192.168.2.1,22,,
```

Running the script will generate the following files:

1. **`hosts.yml`** (dynamic inventory for Ansible)
2. **`hosts_unreachable.csv`** (CSV file with unreachable hosts, if any)

```bash
python dynamic_inventory.py hosts.csv
```

Output:

```
✅ Inventory written to: hosts.yml
🎉 All hosts reachable and added.
```

If any hosts are unreachable:

```
⚠️  Unreachable IPs written to: hosts_unreachable.csv
```

## Conclusion

This script automates the process of creating dynamic Ansible inventory files from a CSV list of hosts. It checks the accessibility of the servers by testing open ports and saves unreachable hosts separately for easy tracking. You can customize SSH credentials and log in with your specified username and password.
