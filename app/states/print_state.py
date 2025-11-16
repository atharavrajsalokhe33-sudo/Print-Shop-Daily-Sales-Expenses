import reflex as rx
from typing import TypedDict, Literal, cast
import datetime
import time
import logging
import json
import urllib.parse

TransactionType = Literal["print", "expense", "cash"]


class Transaction(TypedDict):
    id: float
    timestamp: str
    type: TransactionType
    description: str
    amount: float
    customer_name: str
    customer_phone: str
    customer_email: str


DEFAULT_TRANSACTIONS = [
    {
        "id": 1718883600.0,
        "timestamp": "2024-06-20",
        "type": "print",
        "description": "Color Print (5 pages)",
        "amount": 50.0,
        "customer_name": "John Doe",
        "customer_phone": "1234567890",
        "customer_email": "john.doe@example.com",
    },
    {
        "id": 1718883660.0,
        "timestamp": "2024-06-20",
        "type": "expense",
        "description": "Paper Ream",
        "amount": -550.0,
        "customer_name": "",
        "customer_phone": "",
        "customer_email": "",
    },
    {
        "id": 1718883720.0,
        "timestamp": "2024-06-21",
        "type": "print",
        "description": "B&W 1-Side (20 pages)",
        "amount": 40.0,
        "customer_name": "Jane Smith",
        "customer_phone": "0987654321",
        "customer_email": "jane.smith@example.com",
    },
]


class PrintState(rx.State):
    transactions_json: str = rx.LocalStorage(
        json.dumps(DEFAULT_TRANSACTIONS), sync=True, name="transactions"
    )
    form_type: TransactionType = "print"
    print_type: str = "color"
    active_view: str = "dashboard"
    business_name: str = "ColorCraft"
    business_upi_id: str = "your.business@upi"
    business_upi_number: str = "9876543210"
    business_qr_code_url: str = "/placeholder.svg"
    selected_transaction_ids: list[float] = []
    customer_name_for_invoice: str = ""
    invoice_number: str = ""

    def _get_transactions(self) -> list[Transaction]:
        try:
            return json.loads(self.transactions_json)
        except (json.JSONDecodeError, TypeError) as e:
            logging.exception(f"Error: {e}")
            return []

    def _save_transactions(self, transactions: list[Transaction]):
        self.transactions_json = json.dumps(transactions)

    @rx.var
    def transactions(self) -> list[Transaction]:
        return self._get_transactions()

    @rx.var
    def total_collection(self) -> float:
        return sum((t["amount"] for t in self.transactions if t["amount"] > 0))

    @rx.var
    def total_expenses(self) -> float:
        return abs(sum((t["amount"] for t in self.transactions if t["amount"] < 0)))

    @rx.var
    def net_balance(self) -> float:
        return self.total_collection - self.total_expenses

    @rx.var
    def today_collection(self) -> float:
        today_str = datetime.date.today().isoformat()
        return sum(
            (
                t["amount"]
                for t in self.transactions
                if t["amount"] > 0 and t["timestamp"] == today_str
            )
        )

    @rx.var
    def today_expenses(self) -> float:
        today_str = datetime.date.today().isoformat()
        return abs(
            sum(
                (
                    t["amount"]
                    for t in self.transactions
                    if t["amount"] < 0 and t["timestamp"] == today_str
                )
            )
        )

    @rx.var
    def recent_transactions(self) -> list[Transaction]:
        return sorted(self.transactions, key=lambda t: t["id"], reverse=True)

    @rx.var
    def selected_transactions(self) -> list[Transaction]:
        return [
            t for t in self.transactions if t["id"] in self.selected_transaction_ids
        ]

    @rx.var
    def selected_transactions_total(self) -> float:
        return sum((t["amount"] for t in self.selected_transactions))

    @rx.var
    def generate_invoice_text(self) -> str:
        if not self.customer_name_for_invoice or not self.selected_transactions:
            return ""
        inv_num = self.invoice_number.strip() or f"INV-{int(time.time())}"
        today_str = datetime.date.today().isoformat()
        header = f"{self.business_name}\n--------------------\nInvoice To: {self.customer_name_for_invoice}\nInvoice #: {inv_num}\nDate: {today_str}\n--------------------\n\n"
        items = """Items:
"""
        for item in self.selected_transactions:
            items += f"- {item['description']}: ₹{item['amount']:.2f}\n"
        footer = f"\n--------------------\nTotal Amount: ₹{self.selected_transactions_total:.2f}\n--------------------\nThank you for your business!\n"
        return header + items + footer

    @rx.event
    def set_active_view(self, view: str):
        self.active_view = view

    @rx.event
    def set_form_type(self, type: TransactionType):
        self.form_type = type

    @rx.event
    def set_print_type(self, type: str):
        self.print_type = type

    @rx.event
    def toggle_transaction_selection(self, transaction_id: float):
        if transaction_id in self.selected_transaction_ids:
            self.selected_transaction_ids.remove(transaction_id)
        else:
            self.selected_transaction_ids.append(transaction_id)

    @rx.event
    def download_invoice(self):
        if not self.generate_invoice_text:
            return rx.toast(
                "Please select transactions and enter a customer name.", duration=3000
            )
        inv_num = self.invoice_number.strip() or f"INV-{int(time.time())}"
        return rx.download(
            data=PrintState.generate_invoice_text.encode("utf-8"),
            filename=f"Invoice-{inv_num}-{self.customer_name_for_invoice}.txt",
        )

    @rx.event
    def share_invoice_whatsapp(self):
        if not self.generate_invoice_text:
            return rx.toast(
                "Please select transactions and enter a customer name.", duration=3000
            )
        phone_number = ""
        for t in self.selected_transactions:
            transaction = cast(Transaction, t)
            if transaction.get("customer_phone"):
                phone_number = transaction["customer_phone"]
                break
        message = urllib.parse.quote(self.generate_invoice_text)
        url = f"https://wa.me/{phone_number}?text={message}"
        return rx.redirect(url, external=True)

    @rx.event
    def add_transaction(self, form_data: dict):
        try:
            new_id = time.time()
            today_str = datetime.date.today().isoformat()
            transactions = self._get_transactions()
            if self.form_type == "print":
                pages_str = form_data.get("pages", "").strip()
                customer_name = form_data.get("customer_name", "").strip()
                if not customer_name:
                    yield rx.toast("Customer name is required.", duration=3000)
                    return
                if not pages_str:
                    yield rx.toast("Number of pages is required.", duration=3000)
                    return
                pages = int(pages_str)
                if pages <= 0:
                    yield rx.toast("Number of pages must be positive.", duration=3000)
                    return
                print_type = form_data["print_type"]
                note = form_data.get("note", "").strip()
                customer_phone = form_data.get("customer_phone", "").strip()
                customer_email = form_data.get("customer_email", "").strip()
                amount = 0.0
                base_description = ""
                if print_type == "color":
                    amount = float(form_data.get("amount", 0))
                    base_description = f"Color Print ({pages} pages)"
                elif print_type == "bw_1_side":
                    amount = pages * 2.0
                    base_description = f"B&W 1-Side ({pages} pages)"
                elif print_type == "bw_2_side":
                    amount = pages * 3.0
                    base_description = f"B&W 2-Side ({pages} pages)"
                elif print_type == "xerox_color":
                    amount = pages * 10.0
                    base_description = f"Xerox Color Copy ({pages} pages)"
                elif print_type == "xerox_bw":
                    amount = pages * 2.0
                    base_description = f"Xerox B&W Copy ({pages} pages)"
                description = (
                    f"{note}: {base_description}" if note else base_description
                )
                if amount <= 0:
                    yield rx.toast(
                        "Amount for print job must be positive.", duration=3000
                    )
                    return
                transactions.append(
                    {
                        "id": new_id,
                        "timestamp": today_str,
                        "type": "print",
                        "description": description,
                        "amount": amount,
                        "customer_name": customer_name,
                        "customer_phone": customer_phone,
                        "customer_email": customer_email,
                    }
                )
                self._save_transactions(transactions)
                yield rx.toast("Print job added successfully!", duration=3000)
            elif self.form_type == "expense":
                description = form_data.get("description", "").strip()
                amount = float(form_data.get("amount", 0))
                if not description or amount <= 0:
                    yield rx.toast(
                        "Expense note and positive amount are required.", duration=3000
                    )
                    return
                transactions.append(
                    {
                        "id": new_id,
                        "timestamp": today_str,
                        "type": "expense",
                        "description": description,
                        "amount": -amount,
                        "customer_name": "",
                        "customer_phone": "",
                        "customer_email": "",
                    }
                )
                self._save_transactions(transactions)
                yield rx.toast("Expense recorded successfully!", duration=3000)
        except (ValueError, KeyError) as e:
            logging.exception(f"Error: {e}")
            yield rx.toast(f"Invalid form data: {e}", duration=4000)

    @rx.event
    def delete_transaction(self, transaction_id: float):
        transactions = self._get_transactions()
        transactions = [t for t in transactions if t["id"] != transaction_id]
        self._save_transactions(transactions)
        yield rx.toast("Transaction deleted.", duration=3000)