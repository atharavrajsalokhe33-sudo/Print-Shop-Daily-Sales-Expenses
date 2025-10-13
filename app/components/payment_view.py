import reflex as rx
from app.states.print_state import PrintState


def _cash_form_fields() -> rx.Component:
    return rx.el.div(
        rx.el.input(
            name="description",
            placeholder="Write a note (optional)",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.el.input(
            name="amount",
            placeholder="Amount (₹)",
            type="number",
            step="0.01",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.el.div(
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name="cash_direction",
                    value="in",
                    default_checked=True,
                    class_name="mr-2 h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500",
                ),
                "Cash In (Revenue)",
                class_name="flex items-center text-sm text-gray-700",
            ),
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name="cash_direction",
                    value="out",
                    class_name="mr-2 h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500",
                ),
                "Cash Out (Cost)",
                class_name="flex items-center text-sm text-gray-700",
            ),
            class_name="flex gap-6 mt-2",
        ),
        class_name="flex flex-col gap-4",
    )


def payment_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Cash Transactions", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Quickly record cash income or expenses.",
            class_name="text-gray-500 mt-1 mb-8",
        ),
        rx.el.div(
            rx.el.form(
                _cash_form_fields(),
                rx.el.button(
                    "Record Cash",
                    rx.icon("arrow-right", class_name="ml-2"),
                    type="submit",
                    class_name="w-full mt-6 p-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors shadow-lg hover:shadow-purple-300/50 flex items-center justify-center",
                ),
                on_submit=PrintState.add_cash_transaction_from_payment_view,
                reset_on_submit=True,
                class_name="w-full",
            ),
            class_name="bg-white p-8 rounded-2xl border border-gray-200/80 shadow-sm w-full max-w-lg",
        ),
        class_name="w-full flex flex-col items-center",
    )