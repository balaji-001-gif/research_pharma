import frappe


def boot_session(bootinfo):
    """Inject Pharma R&D module configuration into the boot session."""
    bootinfo["pharma_rd"] = {
        "version": "0.0.1",
        "module": "Pharma R&D",
    }
