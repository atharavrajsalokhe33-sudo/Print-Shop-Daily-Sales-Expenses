import reflex as rx
from app.states.print_state import PrintState, Transaction
from app.components.transaction_form import transaction_form


def transaction_item(transaction: Transaction) -> rx.Component:
    is_selected = PrintState.add_selected_transactions.contains(transaction["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=is_selected,
                on_change=lambda _: PrintState.toggle_add_transaction(
                    transaction["id"]
                ),
                class_name="h-5 w-5 rounded text-purple-600 border-gray-300 focus:ring-purple-500 cursor-pointer mr-4",
            ),
            rx.el.div(
                rx.icon(
                    rx.match(
                        transaction["type"],
                        ("print", "printer"),
                        ("expense", "shopping-cart"),
                        ("cash", "wallet"),
                        "dollar-sign",
                    ),
                    size=20,
                    class_name="text-gray-500",
                ),
                class_name=rx.cond(
                    transaction["amount"] > 0,
                    "p-3 bg-green-100 rounded-full",
                    "p-3 bg-red-100 rounded-full",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    transaction["description"], class_name="font-semibold text-gray-800"
                ),
                rx.el.div(
                    rx.cond(
                        transaction["customer_name"],
                        rx.el.div(
                            rx.icon("user", size=12, class_name="mr-1 text-gray-500"),
                            rx.el.span(
                                transaction["customer_name"],
                                class_name="text-xs text-gray-600",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.p(
                        transaction["timestamp"], class_name="text-sm text-gray-500"
                    ),
                    class_name="flex items-center gap-4",
                ),
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
                on_click=lambda: PrintState.delete_transaction(transaction["id"]),
                class_name="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name=rx.cond(
            is_selected,
            "flex justify-between items-center p-4 border-b border-gray-100 bg-purple-50/50 transition-colors",
            "flex justify-between items-center p-4 border-b border-gray-100 hover:bg-gray-50/50 transition-colors",
        ),
    )


def transactions_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            transaction_form(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Recent Transactions",
                        class_name="text-xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "Select print jobs to generate a quick invoice.",
                        class_name="text-gray-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Invoice Total:",
                        rx.el.span(
                            f" ₹{PrintState.add_invoice_total:.2f}",
                            class_name="font-bold text-2xl ml-2",
                        ),
                        class_name="text-lg text-gray-600 font-medium",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm flex flex-col gap-4 mb-6",
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