import reflex as rx
from app.states.print_state import PrintState


def _form_button(text: str, form_type: str) -> rx.Component:
    return rx.el.button(
        text,
        on_click=lambda: PrintState.set_form_type(form_type),
        class_name=rx.cond(
            PrintState.form_type == form_type,
            "px-4 py-2 text-sm font-semibold text-white bg-purple-600 rounded-lg shadow-sm",
            "px-4 py-2 text-sm font-semibold text-gray-700 bg-white rounded-lg border border-gray-200 hover:bg-gray-50",
        ),
        type="button",
    )


def _print_form_fields() -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Color Print", value="color"),
            rx.el.option("B&W 1-Side", value="bw_1_side"),
            rx.el.option("B&W 2-Side", value="bw_2_side"),
            name="print_type",
            on_change=PrintState.set_print_type,
            class_name="w-full p-3 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.el.input(
            name="pages",
            placeholder="Number of Pages",
            type="number",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.el.input(
            name="note",
            placeholder="Write a note (optional)",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.cond(
            PrintState.print_type == "color",
            rx.el.input(
                name="amount",
                placeholder="Total Amount (₹)",
                type="number",
                step="0.01",
                class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
            ),
            rx.fragment(),
        ),
        class_name="flex flex-col gap-4",
    )


def _expense_form_fields() -> rx.Component:
    return rx.el.div(
        rx.el.input(
            name="description",
            placeholder="Write a note (e.g., Ink, Paper)",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        rx.el.input(
            name="amount",
            placeholder="Amount (₹)",
            type="number",
            step="0.01",
            class_name="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
        ),
        class_name="flex flex-col gap-4",
    )


def transaction_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Add New Transaction", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    _form_button("Print Job", "print"),
                    _form_button("Expense", "expense"),
                    class_name="flex gap-2 p-1 bg-gray-100 rounded-xl w-fit mb-6",
                ),
                rx.match(
                    PrintState.form_type,
                    ("print", _print_form_fields()),
                    ("expense", _expense_form_fields()),
                    _print_form_fields(),
                ),
                rx.el.button(
                    rx.match(
                        PrintState.form_type,
                        ("print", "Add Print Job"),
                        ("expense", "Record Expense"),
                        "Submit",
                    ),
                    rx.icon("arrow-right", class_name="ml-2"),
                    type="submit",
                    class_name="w-full mt-6 p-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors shadow-lg hover:shadow-purple-300/50 flex items-center justify-center",
                ),
                class_name="flex flex-col gap-4",
            ),
            on_submit=PrintState.add_transaction,
            reset_on_submit=True,
            class_name="w-full",
        ),
        class_name="bg-white p-8 rounded-2xl border border-gray-200/80 shadow-sm w-full max-w-lg",
    )