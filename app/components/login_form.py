import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    """The login form component."""
    return rx.el.div(
        rx.el.h2("Welcome Back", class_name="text-2xl font-bold text-gray-800"),
        rx.el.p("Sign in to access your dashboard.", class_name="text-gray-500 mb-6"),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email",
                    html_for="email",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    placeholder="user@print.com",
                    id="email",
                    type="email",
                    name="email",
                    required=True,
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    html_for="password",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    placeholder="••••••••",
                    id="password",
                    type="password",
                    name="password",
                    required=True,
                    class_name="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-4 w-4 mr-2"),
                    AuthState.error_message,
                    class_name="flex items-center text-sm text-red-600 bg-red-100 p-3 rounded-lg mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                "Sign In",
                rx.icon("arrow-right", class_name="ml-2"),
                type="submit",
                class_name="w-full p-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition-colors shadow-lg hover:shadow-purple-300/50 flex items-center justify-center",
            ),
            on_submit=AuthState.login,
        ),
        class_name="bg-white p-8 rounded-2xl border border-gray-200/80 shadow-lg w-full max-w-md",
    )