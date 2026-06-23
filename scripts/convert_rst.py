#!/usr/bin/env python3
"""One-shot migration: convert the Sphinx .rst sources to Docusaurus Markdown.

For each source file:
  1. preprocess Sphinx roles in the raw RST (guilabel/ref/doc/code)
  2. run pandoc (rst -> gfm) to get pipe tables and fenced code
  3. post-process the Markdown:
       - GitHub alert blockquotes -> Docusaurus :::admonitions
       - generic `.. admonition::` div -> :::note
       - image paths -> absolute /_static/...
  4. add frontmatter (title from the first H1, sidebar_position)

`download` and `install` are NOT handled here: they use dynamic version data
and are authored by hand as .mdx. Legacy files (NS7 migration) are excluded.
"""

import json
import os
import re
import subprocess
import sys

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(SRC_DIR, "docs", "administrator-manual")

# folder -> (label, position)
CATEGORIES = {
    "about": ("About", 1),
    "installation": ("Installation", 2),
    "monitoring": ("Monitoring", 3),
    "system": ("System", 4),
    "network": ("Network", 5),
    "users-objects": ("Users and objects", 6),
    "firewall": ("Firewall", 7),
    "security": ("Security", 8),
    "vpn": ("VPN", 9),
    "high-availability": ("High Availability", 10),
    "advanced-cli": ("Advanced (CLI)", 11),
    "best-practices": ("Best practices", 12),
}

# rst basename (no ext) -> (folder, position within folder)
MAPPING = {
    "introduction": ("about", 1),
    "release_notes": ("about", 2),
    # installation: download + install are authored as .mdx separately
    "system_requirements": ("installation", 1),
    "remote_access": ("installation", 4),
    "setup_wizard": ("installation", 5),
    "monitoring": ("monitoring", 1),
    "netify_informatics": ("monitoring", 2),
    "subscription": ("system", 1),
    "remote_support": ("system", 2),
    "backup": ("system", 3),
    "updates": ("system", 4),
    "storage": ("system", 5),
    "reset_recovery": ("system", 6),
    "controller": ("system", 7),
    "network": ("network", 1),
    "dns_dhcp": ("network", 2),
    "routing": ("network", 3),
    "multiwan": ("network", 4),
    "hotspot": ("network", 5),
    "reverse_proxy": ("network", 6),
    "qos": ("network", 7),
    "users_databases": ("users-objects", 1),
    "objects": ("users-objects", 2),
    "port_forward": ("firewall", 1),
    "nat": ("firewall", 2),
    "firewall_rules": ("firewall", 3),
    "connections": ("firewall", 4),
    "zones_and_policies": ("firewall", 5),
    "content_filter": ("security", 1),
    "threat_shield_ip": ("security", 2),
    "threat_shield_dns": ("security", 3),
    "dpi_filter": ("security", 4),
    "flashstart": ("security", 5),
    "ips": ("security", 6),
    "openvpn_roadwarrior": ("vpn", 1),
    "openvpn_tunnels": ("vpn", 2),
    "ipsec_tunnels": ("vpn", 3),
    "wireguard": ("vpn", 4),
    "ha_overview_features_limitations": ("high-availability", 1),
    "ha_setup_and_management": ("high-availability", 2),
    "ha_maintenance_troubleshooting": ("high-availability", 3),
    "avahi": ("advanced-cli", 1),
    "ddns": ("advanced-cli", 2),
    "dns_over_http": ("advanced-cli", 3),
    "smtp": ("advanced-cli", 4),
    "snmp": ("advanced-cli", 5),
    "custom_openvpn_tunnel": ("advanced-cli", 6),
    "logs": ("advanced-cli", 7),
    "speedtest": ("advanced-cli", 8),
    "ups": ("advanced-cli", 9),
    "wol": ("advanced-cli", 10),
    "checkmk": ("advanced-cli", 11),
    "victoria_logs": ("advanced-cli", 12),
    "uci": ("advanced-cli", 13),
    "troubleshooting": ("best-practices", 1),
}

ALERT_MAP = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "info",
    "WARNING": "warning",
    "CAUTION": "warning",
    "DANGER": "danger",
}


def preprocess_rst(text):
    # guilabel -> bold (UI elements)
    text = re.sub(r":guilabel:`([^`]+)`", r"**\1**", text)
    # ref/doc with explicit text "Label <target>" -> keep the label text only
    text = re.sub(r":ref:`([^`<]*?)\s*<[^>]+>`", r"\1", text)
    text = re.sub(r":doc:`([^`<]*?)\s*<[^>]+>`", r"\1", text)
    # bare ref/doc -> plain text
    text = re.sub(r":ref:`([^`]+)`", r"\1", text)
    text = re.sub(r":doc:`([^`]+)`", r"\1", text)
    # code role -> inline code
    text = re.sub(r":code:`([^`]+)`", r"`\1`", text)
    return text


def convert_github_alerts(text):
    lines = text.split("\n")
    out = []
    i = 0
    alert_re = re.compile(r"^>\s*\[!([A-Z]+)\]\s*$")
    while i < len(lines):
        m = alert_re.match(lines[i])
        if m:
            kind = ALERT_MAP.get(m.group(1), "note")
            body = []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                stripped = re.sub(r"^>\s?", "", lines[i])
                body.append(stripped)
                i += 1
            # drop leading/trailing blank lines in body
            while body and body[0].strip() == "":
                body.pop(0)
            while body and body[-1].strip() == "":
                body.pop()
            out.append(f":::{kind}")
            out.append("")
            out.extend(body)
            out.append("")
            out.append(":::")
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def convert_generic_admonitions(text):
    # <div class="admonition"> ... </div>  ->  :::note (first line = title)
    def repl(match):
        inner = match.group(1).strip("\n")
        parts = [p for p in inner.split("\n")]
        # drop blank lines around
        content = [p for p in parts]
        while content and content[0].strip() == "":
            content.pop(0)
        title = content[0].strip() if content else ""
        rest = content[1:]
        while rest and rest[0].strip() == "":
            rest.pop(0)
        body = "\n".join(rest).strip()
        block = [":::note"]
        if title:
            block.append("")
            block.append(f"**{title}**")
        if body:
            block.append("")
            block.append(body)
        block.append("")
        block.append(":::")
        return "\n".join(block)

    return re.sub(
        r'<div class="admonition">\n(.*?)\n</div>',
        repl,
        text,
        flags=re.DOTALL,
    )


def fix_image_paths(text):
    text = text.replace("](../_static/", "](/_static/")
    text = text.replace("](_static/", "](/_static/")
    text = text.replace('src="../_static/', 'src="/_static/')
    text = text.replace('src="_static/', 'src="/_static/')
    return text


def derive_title(md):
    for line in md.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def convert_file(basename, folder, position):
    src = os.path.join(SRC_DIR, basename + ".rst")
    raw = open(src, encoding="utf-8").read()
    raw = preprocess_rst(raw)
    md = subprocess.run(
        ["pandoc", "-f", "rst", "-t", "gfm", "--wrap=none"],
        input=raw,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    md = convert_github_alerts(md)
    md = convert_generic_admonitions(md)
    md = fix_image_paths(md)
    # strip any leftover interpreted-text role attributes
    md = re.sub(r"\{\.interpreted-text[^}]*\}", "", md)

    title = derive_title(md) or basename.replace("_", " ").title()
    title_esc = title.replace('"', '\\"')
    frontmatter = f'---\ntitle: "{title_esc}"\nsidebar_position: {position}\n---\n\n'

    out_dir = os.path.join(DOCS_DIR, folder)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, basename + ".md")
    open(out_path, "w", encoding="utf-8").write(frontmatter + md.strip() + "\n")
    return out_path


def write_categories():
    for folder, (label, position) in CATEGORIES.items():
        d = os.path.join(DOCS_DIR, folder)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "_category_.json"), "w", encoding="utf-8") as f:
            json.dump(
                {"label": label, "position": position}, f, indent=2
            )
            f.write("\n")


def main():
    write_categories()
    count = 0
    for basename, (folder, position) in MAPPING.items():
        path = convert_file(basename, folder, position)
        count += 1
        print(f"  {basename}.rst -> {os.path.relpath(path, SRC_DIR)}")
    print(f"Converted {count} files.")


if __name__ == "__main__":
    main()
