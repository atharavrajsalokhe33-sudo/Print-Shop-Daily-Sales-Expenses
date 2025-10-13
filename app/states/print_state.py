import reflex as rx
from typing import TypedDict, Literal
import datetime
import time
import logging

TransactionType = Literal["print", "expense"]


class Transaction(TypedDict):
    id: float
    timestamp: str
    type: TransactionType
    description: str
    amount: float


class PrintState(rx.State):
    transactions: list[Transaction] = [
        {
            "id": 1718883600.0,
            "timestamp": "2024-06-20",
            "type": "print",
            "description": "Color Print (5 pages)",
            "amount": 50.0,
        },
        {
            "id": 1718883660.0,
            "timestamp": "2024-06-20",
            "type": "expense",
            "description": "Paper Ream",
            "amount": -550.0,
        },
        {
            "id": 1718883720.0,
            "timestamp": "2024-06-21",
            "type": "print",
            "description": "B&W 1-Side (20 pages)",
            "amount": 40.0,
        },
    ]
    form_type: TransactionType = "print"
    print_type: str = "color"
    show_toast: bool = False
    toast_message: str = ""
    toast_type: str = "success"

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

    @rx.event
    def set_form_type(self, type: TransactionType):
        self.form_type = type

    @rx.event
    def set_print_type(self, type: str):
        self.print_type = type

    @rx.event
    def add_transaction(self, form_data: dict):
        try:
            new_id = time.time()
            today_str = datetime.date.today().isoformat()
            if self.form_type == "print":
                pages = int(form_data.get("pages", 0))
                if pages <= 0:
                    yield rx.toast("Number of pages must be positive.", duration=3000)
                    return
                print_type = form_data["print_type"]
                amount = 0.0
                description = ""
                if print_type == "color":
                    amount = float(form_data["amount"])
                    description = f"Color Print ({pages} pages)"
                elif print_type == "bw_1_side":
                    amount = pages * 2.0
                    description = f"B&W 1-Side ({pages} pages)"
                elif print_type == "bw_2_side":
                    amount = pages * 3.0
                    description = f"B&W 2-Side ({pages} pages)"
                if amount <= 0:
                    yield rx.toast(
                        "Amount for color print must be positive.", duration=3000
                    )
                    return
                self.transactions.append(
                    {
                        "id": new_id,
                        "timestamp": today_str,
                        "type": "print",
                        "description": description,
                        "amount": amount,
                    }
                )
                yield rx.toast("Print job added successfully!", duration=3000)
            elif self.form_type == "expense":
                description = form_data.get("description", "").strip()
                amount = float(form_data.get("amount", 0))
                if not description or amount <= 0:
                    yield rx.toast(
                        "Expense description and positive amount are required.",
                        duration=3000,
                    )
                    return
                self.transactions.append(
                    {
                        "id": new_id,
                        "timestamp": today_str,
                        "type": "expense",
                        "description": description,
                        "amount": -amount,
                    }
                )
                yield rx.toast("Expense recorded successfully!", duration=3000)
        except (ValueError, KeyError) as e:
            logging.exception(f"Error: {e}")
            yield rx.toast(f"Invalid form data: {e}", duration=4000)

    @rx.event
    def delete_transaction(self, transaction_id: float):
        self.transactions = [t for t in self.transactions if t["id"] != transaction_id]
        yield rx.toast("Transaction deleted.", duration=3000)