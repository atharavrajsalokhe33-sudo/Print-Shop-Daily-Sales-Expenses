import reflex as rx
from app.components.dashboard_header import dashboard_header
from app.components.transaction_form import transaction_form
from app.components.transaction_list import transaction_list


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            dashboard_header(),
            rx.el.div(
                transaction_form(),
                transaction_list(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start mt-12",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
        ),
        class_name="font-['Montserrat'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)