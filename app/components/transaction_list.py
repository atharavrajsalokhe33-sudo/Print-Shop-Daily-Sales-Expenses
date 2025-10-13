import reflex as rx
from app.states.print_state import PrintState, Transaction
from app.components.transaction_form import transaction_form


def transaction_item(transaction: Transaction) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(transaction["type"] == "print", "printer", "shopping-cart"),
                    size=20,
                    class_name="text-gray-500",
                ),
                class_name=rx.cond(
                    transaction["type"] == "print",
                    "p-3 bg-green-100 rounded-full",
                    "p-3 bg-red-100 rounded-full",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    transaction["description"], class_name="font-semibold text-gray-800"
                ),
                rx.el.p(transaction["timestamp"], class_name="text-sm text-gray-500"),
                class_name="flex-grow",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.p(
                rx.cond(
                    transaction["amount"] > 0,
                    f"+₹{transaction['amount']:.2f}",
                    f"-₹{abs(transaction['amount']):.2f}",
                ),
                class_name=rx.cond(
                    transaction["amount"] > 0,
                    "font-bold text-green-600",
                    "font-bold text-red-600",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", size=16),
                on_click=PrintState.delete_transaction(transaction["id"]),
                class_name="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors",
                type="button",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center p-4 border-b border-gray-100 hover:bg-gray-50/50 transition-colors",
    )


def transactions_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            transaction_form(),
            rx.el.div(
                rx.el.h2(
                    "Recent Transactions",
                    class_name="text-xl font-bold text-gray-800 mb-4",
                ),
                rx.el.div(
                    rx.cond(
                        PrintState.recent_transactions.length() > 0,
                        rx.foreach(PrintState.recent_transactions, transaction_item),
                        rx.el.div(
                            rx.el.p("No transactions yet.", class_name="text-gray-500"),
                            class_name="flex justify-center items-center h-32",
                        ),
                    ),
                    class_name="bg-white rounded-2xl border border-gray-200/80 shadow-sm overflow-hidden",
                ),
                class_name="w-full",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start",
        ),
        class_name="w-full",
    )