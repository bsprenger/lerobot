from dataclasses import dataclass

from lerobot.common.envs.configs import EnvConfig
from lerobot.configs import parser

# class DynamicChoiceRegistry(ChoiceRegistryBase):
#     """
#     A flexible registry that combines features of both ChoiceRegistry and PluginRegistry.

#     This registry can operate in two modes:
#     1. With discovery: When provided with a discover_packages_path, it behaves like
#        PluginRegistry, automatically discovering and importing plugins
#     2. Without discovery: When no discover_packages_path is provided, it behaves like
#        a standard ChoiceRegistry with manual registration only

#     This approach allows for flexibility in extending the registry system without
#     having to choose between discovery and non-discovery models upfront.

#     Usage:
#     ```python
#     # Without discovery (like ChoiceRegistry)
#     @dataclasses.dataclass
#     class SimpleModelConfig(DynamicChoiceRegistry):
#         pass

#     SimpleModelConfig.register_subclass("simple_model", SimpleModelConfig)

#     # With discovery (like PluginRegistry)
#     @dataclasses.dataclass
#     class DiscoverableModelConfig(DynamicChoiceRegistry, discover_packages_path="my_package.plugins"):
#         pass
#     ```

#     This registry will only attempt to discover packages if a path has been provided.
#     """

#     _choice_registry: ClassVar[dict[str, Any]]
#     discover_packages_path: ClassVar[str | None]
#     _did_discover_packages: ClassVar[bool]

#     def __init_subclass__(cls, discover_packages_path: str | None = None, **kwargs):
#         super().__init_subclass__(**kwargs)
#         if not hasattr(cls, "_choice_registry"):
#             cls._choice_registry = {}
#         if not hasattr(cls, "discover_packages_path"):
#             cls.discover_packages_path = discover_packages_path
#         cls._did_discover_packages = False

#     @classmethod
#     def get_choice_class(cls, name: str) -> Any:
#         cls._discover_packages_if_needed()
#         return cls._choice_registry[name]

#     @classmethod
#     def get_known_choices(cls) -> dict[str, Any]:
#         cls._discover_packages_if_needed()
#         return cls._choice_registry

#     @classmethod
#     def _discover_packages_if_needed(cls):
#         """
#         Discovers packages only if discovery path is set and hasn't been done yet.
#         """
#         if cls._did_discover_packages or cls.discover_packages_path is None:
#             return

#         # Create a delegate class for discovery to avoid duplicating logic
#         # Then we let the delegate do the discovery, which will populate our shared registry
#         class _DiscoveryDelegate(PluginRegistry, discover_packages_path=cls.discover_packages_path):
#             _choice_registry = cls._choice_registry

#         _DiscoveryDelegate._discover_packages()

#         # Mark as discovered
#         cls._did_discover_packages = True


# @dataclass
# class EnvConfig(DynamicChoiceRegistry):
#     discover_packages_path: str | None = None

#     @property
#     def type(self) -> str:
#         return self.get_choice_name(self.__class__)


# @EnvConfig.register_subclass("gpt")
# @dataclass
# class GPTConfig:
#     pass


@dataclass
class TrainConfig:
    env: EnvConfig


@parser.wrap()
def main(cfg: TrainConfig):
    print(cfg)
    print(cfg.env.get_known_choices())
    print(cfg.env.get_choice_class("pybullet_drones"))


if __name__ == "__main__":
    main()
    # print(EnvConfig.get_known_choices())
    # print(EnvConfig.get_choice_class("gpt"))
