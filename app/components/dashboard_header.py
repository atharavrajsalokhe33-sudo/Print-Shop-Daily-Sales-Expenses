import reflex as rx
from app.states.print_state import PrintState
from app.states.auth_state import AuthState
from app.components.stat_card import stat_card


def dashboard_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Printing Business Dashboard",
                    class_name="text-3xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Track your daily and overall financial performance.",
                    class_name="text-gray-500 mb-8",
                ),
            ),
            rx.el.button(
                "Sign Out",
                rx.icon("log-out", class_name="ml-2 h-4 w-4"),
                on_click=AuthState.logout,
                class_name="flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-red-500 hover:bg-red-600 h-9 px-4 py-2",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            stat_card(
                icon="sun",
                title="Today's Collection",
                value=PrintState.today_collection,
                color="green",
            ),
            stat_card(
                icon="alert-triangle",
                title="Today's Expenses",
                value=PrintState.today_expenses,
                color="orange",
            ),
            stat_card(
                icon="trending-up",
                title="Total Collection",
                value=PrintState.total_collection,
                color="purple",
            ),
            stat_card(
                icon="trending-down",
                title="Total Expenses",
                value=PrintState.total_expenses,
                color="red",
            ),
            stat_card(
                icon="scale",
                title="Net Balance",
                value=PrintState.net_balance,
                color="blue",
            ),
            class_name="flex flex-wrap gap-6 mt-6",
        ),
        class_name="w-full",
    )