import typing

from dataclasses import dataclass

from PySide6.QtCore import QSettings


@dataclass
class PresetKey:
    name: str
    val_type: type
    value: typing.Any


class Preset:
    CONFIG_KEY_PRESET = "Preset"

    def __init__(self, filepath: str):
        self.settings = QSettings(filepath, QSettings.Format.IniFormat)

    def load(self, name: str, targets: list[PresetKey]):
        self.settings.beginGroup(f"{self.CONFIG_KEY_PRESET}_{name}")
        for target in targets:
            try:
                target.value = target.val_type(self.settings.value(target.name, target.value))
            except (ValueError, TypeError) as e:
                print(f"Failed to load preset {target.name} by {e}")
        self.settings.endGroup()

    def save(self, name: str, targets: list[PresetKey]):
        self.settings.beginGroup(f"{self.CONFIG_KEY_PRESET}_{name}")
        for target in targets:
            self.settings.setValue(target.name, target.value)
        self.settings.endGroup()

