import reflex as rx
from app.states.print_state import PrintState, Transaction
from app.components.transaction_list import transaction_item


def invoice_creation_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Create Invoice", class_name="text-xl font-bold text-gray-800"),
        rx.el.div(
            rx.el.input(
                placeholder="Customer Name *",
                on_change=PrintState.set_customer_name_for_invoice,
                required=True,
                class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                default_value=PrintState.customer_name_for_invoice,
            ),
            rx.el.input(
                placeholder="Invoice Number (optional)",
                on_change=PrintState.set_invoice_number,
                class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                default_value=PrintState.invoice_number,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Selected Total", class_name="text-sm text-gray-600"),
                rx.el.p(
                    f"₹{PrintState.selected_transactions_total:.2f}",
                    class_name="text-2xl font-bold text-purple-700",
                ),
                class_name="text-center md:text-left",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("download", class_name="mr-2"),
                    "Download Invoice",
                    on_click=PrintState.download_invoice,
                    disabled=PrintState.selected_transaction_ids.length() == 0,
                    class_name="flex items-center justify-center w-full px-4 py-3 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors shadow-sm disabled:bg-gray-300 disabled:cursor-not-allowed",
                ),
                rx.el.button(
                    rx.icon("message-circle", class_name="mr-2"),
                    "Share on WhatsApp",
                    on_click=PrintState.share_invoice_whatsapp,
                    disabled=PrintState.selected_transaction_ids.length() == 0,
                    class_name="flex items-center justify-center w-full px-4 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-colors shadow-sm disabled:bg-gray-300 disabled:cursor-not-allowed",
                ),
                class_name="flex flex-col md:flex-row gap-4",
            ),
            class_name="flex flex-col md:flex-row justify-between items-center gap-4 mt-6 p-4 bg-gray-100 rounded-xl",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200/80 shadow-sm mt-8",
    )


def invoice_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"{PrintState.business_name}",
                class_name="text-3xl font-bold text-gray-800",
            ),
            rx.el.p(
                "Select transactions to generate an invoice.",
                class_name="text-gray-500 mt-1 mb-8",
            ),
            invoice_creation_section(),
            class_name="w-full",
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
            class_name="bg-white rounded-2xl border border-gray-200/80 shadow-sm overflow-hidden mt-8",
        ),
        class_name="w-full",
    )