import reflex as rx


def stat_card(
    icon: str, title: str, value: rx.Var[str | float], color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=24, class_name=f"text-{color}-500"),
            class_name="p-3 bg-white rounded-xl border border-gray-200 shadow-sm mb-4 w-fit",
        ),
        rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(f"₹{value:.2f}", class_name="text-3xl font-bold text-gray-800 mt-1"),
        class_name="bg-white/50 p-6 rounded-2xl border border-gray-200/80 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 flex-1 min-w-[200px]",
    )