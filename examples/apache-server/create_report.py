import sys
import xml.etree.ElementTree as ET

from typing import Tuple, List, Union

from pathlib import Path


class PortReport:
    def __init__(
        self,
        file_path: Path = Path("./scans/general_portscan.xml"),
        ports_to_inspect: List[int] = [80, 443],
    ) -> None:
        self.insecure_ports: List[str] = []

        _, root = self.get_xml_tree(file_path)
        port_list = root.findall("./host/ports/port")
        ports = list(
            filter(
                lambda port: int(port.attrib["portid"]) in ports_to_inspect,
                port_list,
            )
        )

        for port in ports:
            service: ET.Element = port.find("service")
            version: Union[str, None] = service.get("version")
            extra_info: Union[str, None] = service.get("extrainfo")

            if version is not None or extra_info is not None:
                port_number: str = port.get("portid")
                self.insecure_ports.append(port_number)

    def get_color_of_security_level(self) -> str:
        if self.insecure_ports:
            return "red"
        else:
            return "green"

    def get_xml_tree(self, filename: str) -> Tuple[ET.ElementTree, ET.Element]:
        """Returns an xml ElementTree and root Element for the file "filename".

        Args:
            filename (str): A path to a xml file.

        Returns:
            tree (ET.ElementTree): The ElementTree for the file.
            root (ET.Element): The root Element of the file.
        """
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
        except:
            sys.stderr.write(
                f"Invalid file name or the file { filename } doesn't exist.\n"
            )
            sys.exit(1)
        return tree, root


class SSLReport:
    def __init__(self, text_file: str = "sslyze.txt") -> None:
        self.succeded: Union[str, None] = True
        self.offending_tls_versions = []
        self.offending_ciphers = []

        failure_list: List[str] = []
        with open(text_file, "r") as file:
            line_array: List[str] = file.readlines()
            status, failure_list = self.get_status_and_problems(line_array)

        if status != "FAILED":
            # Exit the init function.
            return None

        for line in failure_list:
            split_line = line[2:].split(":", 1)

            failure_type = split_line.pop(0)
            failure_explanation = split_line.pop(0).strip()

            if failure_type == "tls_versions":
                self.offending_tls_versions = self.extract_offenses(failure_explanation)

            if failure_type == "ciphers":
                self.offending_ciphers = self.extract_offenses(failure_explanation)

    def extract_offenses(self, failure_text: str) -> List[str]:
        failure_text = failure_text.split("{")[1]
        failure_text = failure_text.split("}")[0]
        failure_text = failure_text.replace("'", "")

        problems = failure_text.split(", ")

        return problems

    def get_status_and_problems(
        self,
        line_array: List[str],
    ) -> List[str]:
        status: Union[str, None] = None
        problems: List[str] = []

        for line in line_array:
            if (
                line == "\n"
                or "COMPLIANCE AGAINST MOZILLA TLS CONFIGURATION" in line
                or (
                    'Checking results against Mozilla\'s "modern" configuration.'
                    in line
                )
                or "-----" in line
            ):
                continue

            line = line.strip()

            if line[0] != "*":
                status = line.split()[1]
                continue

            problems.append(line)

        return status, problems

    def get_color_of_security_level(self) -> str:
        if self.offending_tls_versions and self.offending_ciphers:
            return "red"
        elif self.offending_tls_versions or self.offending_ciphers:
            return "orange"
        else:
            return "green"


def determine_complete_security_level_color(
    port_security_level: str,
    tls_security_level: str,
) -> str:
    choice_dict = {
        "red": {
            "red": "red",
            "orange": "red",
            "green": "orange",
        },
        "orange": {
            "red": "red",
            "orange": "orange",
            "green": "orange",
        },
        "green": {
            "red": "orange",
            "orange": "orange",
            "green": "green",
        },
    }

    return choice_dict[port_security_level][tls_security_level]


if __name__ == "__main__":
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader("templates/"))

    template = env.get_template("index.html.j2")
    ports = PortReport("general_portscan.xml")
    ssl_report = SSLReport("sslyze.txt")

    print(
        template.render(
            complete_security_level=determine_complete_security_level_color(
                ports.get_color_of_security_level(),
                ssl_report.get_color_of_security_level(),
            ),
            port_security_level=ports.get_color_of_security_level(),
            ports=ports.insecure_ports,
            ssl_security_level=ssl_report.get_color_of_security_level(),
            tls_versions=ssl_report.offending_tls_versions,
            ciphers=ssl_report.offending_ciphers,
        )
    )
