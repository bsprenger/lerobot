from lerobot.common.utils.utils import init_logging
from lerobot.scripts.train import train

if __name__ == "__main__":
    # from pyinstrument import Profiler
    # import gym_pybullet_drones

    # import lerobot.common.envs.configs as env_configs

    # env = gym.make("gym_pybullet_drones/Hover-v0")
    # obs, info = env.reset()
    # print("here")
    init_logging()
    # with Profiler() as p:
    train()
    # with open("output.html", "w") as f:
    #     f.write(p.output_html())


# from dataclasses import dataclass
# from typing import Optional

# from draccus.choice_types import ChoiceRegistry, ChoiceRegistryBase, PluginRegistry


# @dataclass
# class DynamicRegistry(ChoiceRegistryBase):
#     discover_packages_path: str | None = None

#     def __post_init__(self):
#         # Store the current class's registry if it exists
#         registry = getattr(self.__class__, "_choice_registry", {})

#         # Create new class with proper base
#         if self.discover_packages_path is not None:
#             new_base = PluginRegistry
#             # Create new class inheriting from PluginRegistry
#             new_cls = type(
#                 self.__class__.__name__,
#                 (PluginRegistry,),
#                 {
#                     "_choice_registry": registry,
#                     "discover_packages_path": self.discover_packages_path,
#                     "_did_discover_packages": False,
#                     **{k: v for k, v in self.__class__.__dict__.items() if not k.startswith("__")},
#                 },
#             )
#         else:
#             new_base = ChoiceRegistry
#             # Create new class inheriting from ChoiceRegistry
#             new_cls = type(
#                 self.__class__.__name__,
#                 (ChoiceRegistry,),
#                 {
#                     "_choice_registry": registry,
#                     **{k: v for k, v in self.__class__.__dict__.items() if not k.startswith("__")},
#                 },
#             )

#         # Change the instance's class to the new class
#         self.__class__ = new_cls


# @dataclass
# class MyRegistry(DynamicRegistry):
#     some_config: str = "default"


# # Usage as ChoiceRegistry:
# registry1 = MyRegistry()  # Will behave like ChoiceRegistry

# # Usage as PluginRegistry:
# registry2 = MyRegistry(discover_packages_path="my.plugins")  # Will behave like PluginRegistry


# # Both will maintain their registered subclasses
# @MyRegistry.register_subclass("test")
# class TestClass:
#     pass


# """
# This solution:

# Creates a dynamic registry that transforms itself during initialization
# Preserves all class attributes and methods during transformation
# Maintains the registry of choices across transformations
# Requires no modifications to existing ChoiceRegistry or PluginRegistry classes
# Allows for seamless usage of either registry type based on initialization
# The class will act exactly like a ChoiceRegistry or PluginRegistry after initialization, including all their respective behaviors and features.
# """
