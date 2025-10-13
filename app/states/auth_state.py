import reflex as rx

USERS: dict[str, str] = {
    "user1@print.com": "password123",
    "user2@print.com": "password456",
}


class AuthState(rx.State):
    """The authentication state."""

    in_session: bool = rx.LocalStorage(False, name="in_session")
    error_message: str = ""

    @rx.event
    def login(self, form_data: dict):
        """Log the user in."""
        email = form_data.get("email", "").lower().strip()
        password = form_data.get("password", "")
        if email in USERS and USERS[email] == password:
            self.in_session = True
            self.error_message = ""
            return rx.redirect("/")
        else:
            self.in_session = False
            self.error_message = "Invalid email or password. Please try again."
            yield

    @rx.event
    def logout(self):
        """Log the user out."""
        self.in_session = False
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        """Check if the user is logged in and redirect if not."""
        if not self.in_session:
            return rx.redirect("/login")