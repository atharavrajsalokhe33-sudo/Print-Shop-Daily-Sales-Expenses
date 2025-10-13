import reflex as rx
from app.components.login_form import login_form


def login() -> rx.Component:
    """The login page."""
    return rx.el.main(
        rx.el.div(login_form(), class_name="flex items-center justify-center"),
        class_name="font-['Montserrat'] bg-gray-50 min-h-screen p-4",
    )