import reflex as rx
from app.states.print_state import PrintState
from app.components.stat_card import stat_card


def dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"{PrintState.business_name}",
                class_name="text-3xl font-bold text-gray-800",
            ),
            rx.el.p(
                "Your business performance at a glance.",
                class_name="text-gray-500 mt-1",
            ),
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
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8",
        ),
        class_name="w-full",
    )