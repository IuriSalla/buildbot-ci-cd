import json
import os


MASTER_DIR = os.path.dirname(os.path.abspath(__file__))
_PRIMARY_INVENTORY = os.path.join(MASTER_DIR, "hosts.json")
_EXAMPLE_INVENTORY = os.path.join(MASTER_DIR, "hosts.json.example")
# Repositório: hosts.json costuma estar no .gitignore; clone usa o .example.
ANSIBLE_INVENTORY_JSON = (
    _PRIMARY_INVENTORY
    if os.path.isfile(_PRIMARY_INVENTORY)
    else (_EXAMPLE_INVENTORY if os.path.isfile(_EXAMPLE_INVENTORY) else _PRIMARY_INVENTORY)
)


def ansible_json_inventory_targets(
    inventory_path: str = ANSIBLE_INVENTORY_JSON,
) -> tuple[list[str], list[str]]:
    """
    Lê inventário Ansible em JSON no formato aninhado (ex.: all.children.grupo.hosts).
    Retorna duas listas separadas: grupos e hosts.
    """
    groups: list[str] = []
    hosts: list[str] = []
    seen_group: set[str] = set()
    seen_host: set[str] = set()

    if not os.path.isfile(inventory_path):
        return [], ["127.0.0.1"]

    with open(inventory_path, encoding="utf-8") as f:
        data = json.load(f)

    def walk(node: object) -> None:
        if not isinstance(node, dict):
            return

        h = node.get("hosts")  # type: ignore[assignment]
        if isinstance(h, dict):
            for hostname in h:
                if hostname not in seen_host:
                    seen_host.add(hostname)
                    hosts.append(hostname)

        children = node.get("children")  # type: ignore[assignment]
        if isinstance(children, dict):
            for group_name, child in children.items():
                if group_name not in seen_group:
                    seen_group.add(group_name)
                    groups.append(group_name)
                walk(child)

    root = data.get("all", data)
    walk(root)
    sorted_groups = sorted(groups)
    sorted_hosts = sorted(hosts) or ["127.0.0.1"]
    return sorted_groups, sorted_hosts


GROUP_CHOICES, HOST_CHOICES = ansible_json_inventory_targets()
