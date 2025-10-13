import reflex as rx
from app.states.print_state import PrintState, Transaction


def _invoice_transaction_item(transaction: Transaction) -> rx.Component:
    is_selected = PrintState.invoice_selected_transactions.contains(transaction["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=is_selected,
                on_change=lambda _: PrintState.toggle_invoice_transaction(
                    transaction["id"]
                ),
                class_name="h-5 w-5 rounded text-purple-600 border-gray-300 focus:ring-purple-500 cursor-pointer",
            ),
            rx.el.div(
                rx.el.p(
                    transaction["description"], class_name="font-semibold text-gray-800"
                ),
                rx.el.p(transaction["timestamp"], class_name="text-sm text-gray-500"),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.p(
            f"₹{transaction['amount']:.2f}",
            class_name=rx.cond(
                transaction["amount"] > 0,
                "font-semibold text-green-600",
                "font-semibold text-red-600",
            ),
        ),
        class_name="flex justify-between items-center p-4 border-b border-gray-100",
    )


def invoice_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Create Invoice", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Select transactions to generate a downloadable invoice.",
            class_name="text-gray-500 mt-1 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Invoice Details", class_name="text-xl font-bold mb-4"),
                rx.el.input(
                    placeholder="Customer Name (Optional)",
                    on_change=PrintState.set_invoice_customer_name,
                    default_value=PrintState.invoice_customer_name,
                    class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500",
                ),
                rx.el.input(
                    placeholder="Invoice Number (Optional)",
                    on_change=PrintState.set_invoice_number,
                    default_value=PrintState.invoice_number,
                    class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm flex flex-col gap-4",
            ),
            rx.el.div(
                rx.el.h2("Select Transactions", class_name="text-xl font-bold mb-4"),
                rx.el.div(
                    rx.foreach(
                        PrintState.recent_transactions, _invoice_transaction_item
                    ),
                    class_name="max-h-96 overflow-y-auto bg-white rounded-2xl border border-gray-200/80 shadow-sm",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Total:",
                    rx.el.span(
                        f" ₹{PrintState.invoice_total:.2f}",
                        class_name="font-bold text-2xl ml-2",
                    ),
                    class_name="text-lg text-gray-600 font-medium",
                ),
                rx.el.button(
                    "Generate & Download Invoice",
                    rx.icon("download", class_name="ml-2"),
                    on_click=PrintState.generate_invoice,
                    disabled=PrintState.invoice_selected_transactions.length() == 0,
                    class_name="w-full mt-4 p-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
        ),
        class_name="w-full",
    )