import reflex as rx
from app.states.print_state import PrintState


def payment_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Online Payments", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Scan the QR code or use the UPI details below to make a payment.",
            class_name="text-gray-500 mt-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Scan to Pay",
                    class_name="text-lg font-semibold text-gray-700 mb-4 text-center",
                ),
                rx.el.image(
                    src=PrintState.business_qr_code_url,
                    alt="Business Payment QR Code",
                    class_name="w-64 h-64 mx-auto rounded-lg border border-gray-300 shadow-md",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Or use UPI Details",
                    class_name="text-lg font-semibold text-gray-700 mb-4",
                ),
                rx.el.div(
                    rx.el.p("UPI ID:", class_name="font-medium text-gray-600"),
                    rx.el.p(
                        PrintState.business_upi_id,
                        class_name="font-mono text-purple-600 bg-purple-50 px-2 py-1 rounded",
                    ),
                    class_name="flex justify-between items-center py-2 border-b",
                ),
                rx.el.div(
                    rx.el.p("UPI Number:", class_name="font-medium text-gray-600"),
                    rx.el.p(
                        PrintState.business_upi_number,
                        class_name="font-mono text-purple-600 bg-purple-50 px-2 py-1 rounded",
                    ),
                    class_name="flex justify-between items-center py-2",
                ),
                class_name="w-full",
            ),
            class_name="bg-white p-8 rounded-2xl border border-gray-200/80 shadow-sm w-full max-w-sm mt-8",
        ),
        class_name="w-full flex flex-col items-center",
    )