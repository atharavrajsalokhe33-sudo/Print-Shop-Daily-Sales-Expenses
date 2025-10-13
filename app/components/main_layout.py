import reflex as rx
from app.states.print_state import PrintState
from app.components.bottom_nav import bottom_nav
from app.components.dashboard_header import dashboard_view
from app.components.transaction_list import transactions_view
from app.components.payment_view import payment_view


def main_layout() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.match(
                PrintState.active_view,
                ("dashboard", dashboard_view()),
                ("add", transactions_view()),
                ("payment", payment_view()),
                dashboard_view(),
            ),
            class_name="p-4 sm:p-6 lg:p-8 pb-24 md:pb-8",
        ),
        bottom_nav(),
        class_name="font-['Montserrat'] bg-gray-50 min-h-screen",
    )