"""
PWCCA (Projection Weighted Canonical Correlation Analysis) is a comparative metric for comparing
how similar two sets of activations are between two different checkpoints.
"""

# Typing imports
import torch

from lib.svcca.pwcca import compute_pwcca
from src.config._base import BaseComponentConfig
from src.metrics._registry import register_metric
from src.metrics.base import BaseComparativeMetric
from src.utils.exceptions import InvalidComponentError


@register_metric("pwcca")
class PWCCAMetric(BaseComparativeMetric):
    """
    This metric computes the PWCCA of the given data.

    PWCCA is a variant of the Canonical Correlation Analysis (CCA) that uses projection weights to
    compute the similarity between two sets of activations.

    Reference: https://arxiv.org/abs/1806.05759
    """

    def validate_component(self, component_config: BaseComponentConfig) -> bool:
        """
        The PWCCA metric is only valid for activations.
        """
        if component_config.data_type not in ["activations"]:
            raise InvalidComponentError(
                f"PWCCA metric only supports activations, not {component_config.data_type} "
                f"(component: {component_config.component_name})."
            )

    def compute_metric(
        self,
        source_component_layer_data: torch.Tensor,
        target_component_layer_data: torch.Tensor,
    ) -> float:
        """
        Computes the PWCCA of the given data.
        """

        # transforming the data to numpy
        np_source_component_layer_data = source_component_layer_data.to(
            dtype=torch.float32
        ).numpy()
        np_target_component_layer_data = target_component_layer_data.to(
            dtype=torch.float32
        ).numpy()

        pwcca_metric, _, _ = compute_pwcca(
            np_source_component_layer_data, np_target_component_layer_data, epsilon=1e-6
        )

        return float(pwcca_metric)
