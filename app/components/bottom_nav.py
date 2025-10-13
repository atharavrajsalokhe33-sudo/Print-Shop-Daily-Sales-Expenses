import reflex as rx
from app.states.print_state import PrintState


def _nav_button(icon: str, text: str, view: str) -> rx.Component:
    is_active = PrintState.active_view == view
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon, class_name=rx.cond(is_active, "text-purple-600", "text-gray-500")
            ),
            rx.el.span(
                text,
                class_name=rx.cond(
                    is_active,
                    "text-xs font-semibold text-purple-600",
                    "text-xs font-medium text-gray-500",
                ),
            ),
            class_name="flex flex-col items-center gap-1",
        ),
        on_click=PrintState.set_active_view(view),
        class_name="flex-1 p-2 rounded-lg",
    )


def bottom_nav() -> rx.Component:
    return rx.el.div(
        _nav_button("layout-dashboard", "Dashboard", "dashboard"),
        _nav_button("file-plus-2", "Add", "add"),
        _nav_button("indian-rupee", "Payments", "payment"),
        class_name="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-sm border-t border-gray-200 flex justify-around items-center p-2 z-50 md:hidden",
    )