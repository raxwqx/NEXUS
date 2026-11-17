import json
import socket
import unittest

import nexus


class ParsePortsTests(unittest.TestCase):
    def test_single_ports_and_ranges_are_sorted_and_deduplicated(self):
        self.assertEqual(nexus.parse_ports("443,22,80,22"), [22, 80, 443])
        self.assertEqual(nexus.parse_ports("80-82,81"), [80, 81, 82])

    def test_reversed_ranges_are_normalized(self):
        self.assertEqual(nexus.parse_ports("10-8"), [8, 9, 10])

    def test_whitespace_is_ignored(self):
        self.assertEqual(nexus.parse_ports(" 22 , 80 - 82 "), [22, 80, 81, 82])

    def test_invalid_inputs_raise_friendly_errors(self):
        for value in ("abc", "1-2-3", "", "   ", "0", "65536", "0-10", "1-999999"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    nexus.parse_ports(value)

    def test_service_names(self):
        self.assertEqual(nexus.service_name(22), "ssh")
        self.assertEqual(nexus.service_name(443), "https")
        self.assertEqual(nexus.service_name(65000), "")


class AddressTests(unittest.TestCase):
    def test_with_port_for_ipv4_and_ipv6(self):
        self.assertEqual(nexus.with_port(("127.0.0.1", 0), 80), ("127.0.0.1", 80))
        self.assertEqual(nexus.with_port(("::1", 0, 0, 0), 443), ("::1", 443, 0, 0))

    def test_resolve_localhost(self):
        family, sockaddr = nexus.resolve_target("localhost")
        self.assertIn(family, (socket.AF_INET, socket.AF_INET6))
        self.assertTrue(sockaddr[0])

    def test_unresolvable_target_has_clear_error(self):
        with self.assertRaises(ValueError) as context:
            nexus.resolve_target("this-host-should-not-exist.invalid")
        self.assertIn("cannot resolve", str(context.exception))


class ScanTests(unittest.TestCase):
    def test_scan_port_detects_open_and_closed_ports(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            open_port = server.getsockname()[1]

            _, is_open = nexus.scan_port(socket.AF_INET, ("127.0.0.1", 0), open_port, 0.5)
            self.assertTrue(is_open)

            # Bind another socket, then close it to obtain a likely closed port.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                probe.bind(("127.0.0.1", 0))
                closed_port = probe.getsockname()[1]
            _, is_open = nexus.scan_port(socket.AF_INET, ("127.0.0.1", 0), closed_port, 0.2)
            self.assertFalse(is_open)


class ReportTests(unittest.TestCase):
    def test_report_contains_service_labels_and_metadata(self):
        report = nexus.build_report(
            "example.test",
            "192.0.2.10",
            socket.AF_INET,
            [22, 80, 443],
            [22, 443],
            0.5,
            100,
            0.1234,
        )
        self.assertEqual(report["tool"], "NEXUS")
        self.assertEqual(report["version"], nexus.VERSION)
        self.assertEqual(report["address_family"], "IPv4")
        self.assertEqual(report["ports_requested"], 3)
        self.assertEqual(report["open_count"], 2)
        self.assertEqual(
            report["open_ports"],
            [
                {"port": 22, "service": "ssh"},
                {"port": 443, "service": "https"},
            ],
        )
        self.assertEqual(report["duration_seconds"], 0.123)
        json.dumps(report)

    def test_ipv6_report_family(self):
        report = nexus.build_report("::1", "::1", socket.AF_INET6, [80], [], 0.5, 10, 0.0)
        self.assertEqual(report["address_family"], "IPv6")


if __name__ == "__main__":
    unittest.main()
