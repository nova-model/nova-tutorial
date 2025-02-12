"""Module for the main ViewModel."""

from asyncio import create_task, sleep
from threading import Thread
from typing import Any, Dict

from nova.mvvm.interface import BindingInterface

from ..models.main_model import MainModel


class MainViewModel:
    """Viewmodel class, used to create data<->view binding and react on changes from GUI."""

    def __init__(self, model: MainModel, binding: BindingInterface):
        self.model = model
        self.running = False

        # here we create a bind that connects ViewModel with View. It returns a communicator object,
        # that allows to update View from ViewModel (by calling update_view).
        # self.model will be updated automatically on changes of connected fields in View,
        # but one also can provide a callback function if they want to react to those events
        # and/or process errors.
        self.config_bind = binding.new_bind(self.model, callback_after_update=self.change_callback)
        self.running_bind = binding.new_bind()

    def change_callback(self, results: Dict[str, Any]) -> None:
        if results["error"]:
            print(f"error in fields {results['errored']}, model not changed")
        else:
            print(f"model fields updated: {results['updated']}")

    def update_view(self) -> None:
        self.config_bind.update_in_view(self.model)
        self.running_bind.update_in_view(self.running)

    def run_fractal(self) -> None:
        self.running = True
        self.update_view()

        # update_view won't take effect until this method returns a value, so we must offload this long-running task to
        # a background thread for our conditional rendering to work.
        fractal_tool_thread = Thread(target=self.run_fractal_in_background, daemon=True)
        fractal_tool_thread.start()

        # We also need to know when the tool is done running so that we can know when to update the view.
        create_task(self.monitor_fractal())

    def run_fractal_in_background(self) -> None:
        self.model.fractal.run_fractal_tool()
        self.running = False

    async def monitor_fractal(self) -> None:
        while self.running:
            await sleep(0.1)
        self.update_view()
