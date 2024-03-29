"""Defines an interface to a Unix package manager"""
import subprocess


class PackageManager:
    """Generic interface definition for a package manager"""

    def pkg_status(self, pkg_name):
        """Checks if a package is installed"""

    def list_pkgs(self):
        """Lists all installed packages"""


class Dpkg(PackageManager):
    """Debian package manager"""

    def pkg_status(self, pkg_name):
        """Checks if a package is installed"""
        cmd = ["/usr/bin/dpkg-query", "-W", "-f", "${status}", pkg_name]
        proc = subprocess.run(cmd, capture_output=True, check=False)
        return proc.stdout.decode('utf-8')

    def search_pkgs(self, pattern):
        """Searches for packages matching a pattern"""
        cmd = ["/usr/bin/dpkg-query", "-W", "-f", "${Package}\t${status}\n", pattern]
        proc = subprocess.run(cmd, capture_output=True, check=False)
        return proc.stdout.decode('utf-8')


    def list_pkgs(self):
        """Lists installed packages"""
        return self.search_pkgs("*")
