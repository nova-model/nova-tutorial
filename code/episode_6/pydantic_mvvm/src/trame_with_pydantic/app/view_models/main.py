"""Module for the main ViewModel."""

from typing import Any, Dict

from nova.mvvm.interface import BindingInterface

from ..models.settings import SettingsModel


class MainViewModel:
    """Viewmodel class, used to create data<->view binding and react on changes from GUI."""

    def __init__(self, _, binding: BindingInterface):
        self.settings = SettingsModel()
        self.settings_bind = binding.new_bind(self.settings, callback_after_update=self.process_settings_change)

    def process_settings_change(self, results: Dict[str, Any]) -> None:
        if results["error"]:
            print(f"error in fields {results['errored']}, model not changed")
        else:
            print(f"model fields updated: {results['updated']}")

    def update_view(self) -> None:
        self.settings_bind.update_in_view(self.settings)
