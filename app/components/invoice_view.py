import reflex as rx
from app.states.print_state import PrintState, Transaction
from app.components.transaction_list import transaction_item


def invoice_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Transaction History", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "A log of all your recent earnings and expenses.",
            class_name="text-gray-500 mt-1 mb-8",
        ),
        rx.el.div(
            rx.cond(
                PrintState.recent_transactions.length() > 0,
                rx.foreach(PrintState.recent_transactions, transaction_item),
                rx.el.div(
                    rx.el.p("No transactions yet.", class_name="text-gray-500"),
                    class_name="flex justify-center items-center h-48 bg-white rounded-2xl border border-gray-200/80 shadow-sm",
                ),
            ),
            class_name="bg-white rounded-2xl border border-gray-200/80 shadow-sm overflow-hidden",
        ),
        class_name="w-full",
    )