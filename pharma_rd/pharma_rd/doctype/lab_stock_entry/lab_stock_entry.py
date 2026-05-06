import frappe
from frappe.model.document import Document

class LabStockEntry(Document):
    def on_submit(self):
        self.update_lab_item_stock()

    def on_cancel(self):
        self.update_lab_item_stock(cancel=True)

    def update_lab_item_stock(self, cancel=False):
        qty = self.quantity
        if self.entry_type == "Stock Out":
            qty = -qty
        
        if cancel:
            qty = -qty

        item = frappe.get_doc("Lab Item", self.item)
        new_stock = (item.current_stock or 0) + qty
        item.db_set("current_stock", new_stock)
        
        if new_stock < (item.min_stock or 0):
            frappe.msgprint(f"Warning: {item.item_name} is below minimum stock level ({new_stock} remaining).", indicator="orange")
