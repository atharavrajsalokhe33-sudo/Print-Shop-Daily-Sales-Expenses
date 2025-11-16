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
        rx.el.h1("History & Invoicing", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Review transaction history and generate downloadable invoices.",
            class_name="text-gray-500 mt-1 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Download Invoice", class_name="text-xl font-bold mb-4"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Customer Name (Overrides selection)",
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
                    class_name="bg-white p-6 rounded-t-2xl border-x border-t border-gray-200/80 shadow-sm flex flex-col gap-4",
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
                    rx.el.div(
                        rx.el.button(
                            "Copy to Clipboard",
                            rx.icon("copy", class_name="ml-2"),
                            on_click=PrintState.share_invoice,
                            disabled=PrintState.is_share_disabled,
                            class_name="w-full p-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Share via WhatsApp",
                                rx.icon("message-circle", class_name="ml-2"),
                                disabled=PrintState.is_share_disabled,
                                class_name="w-full p-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition-colors shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center",
                            ),
                            href=PrintState.whatsapp_share_url,
                            is_external=True,
                        ),
                        rx.el.button(
                            "Share",
                            rx.icon("share-2", class_name="ml-2"),
                            on_click=PrintState.web_share_invoice,
                            disabled=PrintState.is_share_disabled,
                            class_name="w-full p-3 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition-colors shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center",
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-4",
                    ),
                    class_name="bg-white p-6 rounded-b-2xl border-x border-b border-gray-200/80 shadow-sm",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Select Transactions for Invoice",
                    class_name="text-xl font-bold mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        PrintState.recent_transactions, _invoice_transaction_item
                    ),
                    class_name="max-h-[60vh] overflow-y-auto bg-white rounded-2xl border border-gray-200/80 shadow-sm",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start",
        ),
        class_name="w-full",
    )