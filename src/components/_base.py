"""
Base class for components.
"""

from abc import ABC, abstractmethod
import os

# typing imports
import torch
from typing import Dict, Any
from src.config._base import BaseComponentConfig


class BaseComponent(ABC):
    """
    Base class for components. There are two types of components:
    1. Simple components: these are components that are a single weight, activation or gradient
        tensor from a given layer; e.g. the weight matrix of a layer, or the gradients of the loss
        wrt. the activations of a single weight matrix.
    2. Compound components: these are components that are made up of multiple single components.
        For example, the OV-Circuit is a compound component that is made up of the value and
        output projection layers.
    """

    def __init__(self, training_config: Dict[str, Any]):
        self.training_config = training_config

    def get_model_prefix(self, data: Dict[str, Any]) -> str:
        """
        Simple helper function to get the model prefix from the checkpoint activation keys.

        The model prefix is the part of the key that is common to all of the layers in the model.

        For example, if we have the following list of layer names:
        ```
        {
            "model.0.weight": torch.Tensor,
            "model.1.weight": torch.Tensor,
        }
        ```

        The model prefix is "model.".
        """

        # NOTE: this should be the same for activations and weights
        _activation_layernames = list(data["activations"].keys())

        return os.path.commonprefix(_activation_layernames)

    def check_component_config(self, component_config: BaseComponentConfig) -> None:
        """
        Check the component config; components should specify the required keys in the component
        config by overriding this method. NOTE: by default, all components require a data type;
        i.e. whether the component is an activation, weight, or gradient.

        Args:
            component_config: BaseComponentConfig -- the component configuration.
        """
        assert (
            component_config.data_type is not None
        ), "Data type must be specified in component config"

    @abstractmethod
    def __call__(
        self,
        checkpoint_states: Dict[str, Dict[str, torch.Tensor]],
        component_config: BaseComponentConfig,
    ) -> Dict[str, torch.Tensor]:
        """
        Generate a component. For compound components, this will likely involve some form of matrix
        multiplication of different activations, weights, or gradients to produce a desired
        component. For simple components, this will just return the activations, weights,
        or gradients for the given layers.

        Args:
            checkpoint_states: Dict[str, Dict[str, torch.Tensor]] -- the checkpoint states for
                a given checkpoint.
            component_config: BaseComponentConfig -- the component configuration.

        Returns:
            Dict[str, torch.Tensor] -- a dictionary mapping layer names to the component at that layer; i.e.
                {
                    "model.0.component_name": torch.Tensor,
                    "model.1.component_name": torch.Tensor,
                }
        """

        self.check_component_config(component_config)
