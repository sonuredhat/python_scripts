import csv
import os
import sys
import yaml
import nmap
import re

def sanitize(name):
    return re.sub(r'\W+', '_', name.strip())

def is_port_open(ip, port):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, str(port), arguments='-Pn')
        return nm[ip]['tcp'][int(port)]['state'] == 'open'
    except Exception:
        return False

def generate_inventory(input_file):
    base_name = os.path.splitext(input_file)[0]
    output_file = base_name + '.yml'
    unreachable_file = base_name + '_unreachable.csv'

    inventory = {
        'all': {
            'vars': {
                'ansible_ssh_common_args: \'-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\'',
                'ansible_python_interpreter': '/usr/bin/python3',
                'ansible_ssh_user': 'yourUserName',
                'ansible_ssh_password': 'yourPassword',
                'ansible_become_pass': 'yourSudoPassword',
                'ansible_become_method': 'sudo',
                'ansible_become': True,
                'ansible_become_ask_pass': False
            },
            'children': {}
        }
    }

    unreachable_rows = []

    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bpo_name = row.get('BPO NAME', '').strip()
            group = sanitize(bpo_name)
            host_entry = None

            for label in ['Primary', 'Secondary']:
                ip = row.get(f"{label} IP", '').strip()
                port = row.get(f"{label} Port", '').strip()
                if ip and port and is_port_open(ip, port):
                    host_key = f"{group}_host"
                    host_entry = {
                        host_key: {
                            'ansible_host': ip,
                            'ansible_port': int(port)
                        }
                    }
                    break  # Use first reachable IP

            if host_entry:
                if group not in inventory['all']['children']:
                    inventory['all']['children'][group] = {'hosts': {}}
                inventory['all']['children'][group]['hosts'].update(host_entry)
            else:
                unreachable_rows.append(row)

    # Write YAML inventory
    with open(output_file, 'w') as yamlfile:
        yaml.dump(inventory, yamlfile, sort_keys=False)
    print(f"✅ Inventory written to: {output_file}")

    # Write unreachable file
    if unreachable_rows:
        with open(unreachable_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(unreachable_rows)
        print(f"⚠️  Unreachable IPs written to: {unreachable_file}")
    else:
        print("🎉 All hosts reachable and added.")

if __name__ == "__main__":
    input_csv = sys.argv[1] if len(sys.argv) > 1 else './hosts.csv'
    generate_inventory(input_csv)
