import reflex as rx


def payment_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Online Payments", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Accept payments from your customers.", class_name="text-gray-500 mt-1"
        ),
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Amount (₹)",
                        html_for="payment_amount",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="payment_amount",
                        name="amount",
                        type="number",
                        step="0.01",
                        placeholder="Enter amount",
                        class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Customer Name",
                        html_for="customer_name",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="customer_name",
                        name="customer_name",
                        placeholder="e.g., John Doe",
                        class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Payment Description",
                        html_for="payment_description",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="payment_description",
                        name="description",
                        placeholder="e.g., Invoice #1234",
                        class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Generate Payment Link",
                    rx.icon("link", class_name="ml-2"),
                    type="submit",
                    class_name="w-full p-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors shadow-lg hover:shadow-purple-300/50 flex items-center justify-center",
                ),
                on_submit=lambda: rx.toast(
                    "This feature is a placeholder and not yet implemented."
                ),
                reset_on_submit=True,
            ),
            class_name="bg-white p-8 rounded-2xl border border-gray-200/80 shadow-sm w-full max-w-lg mt-8",
        ),
        class_name="w-full flex flex-col items-center",
    )