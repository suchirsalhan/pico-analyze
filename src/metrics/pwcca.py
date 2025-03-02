"""
PWCCA (Projection Weighted Canonical Correlation Analysis) is a comparative metric for comparing
how similar two sets of activations are between two different checkpoints.
"""

from src.metrics.base import BaseComparativeMetric, BaseMetricConfig, register_metric
from lib.svcca.pwcca import compute_pwcca

# Typing imports
import torch


@register_metric("pwcca")
class PWCCAMetric(BaseComparativeMetric):
    """
    This metric computes the PWCCA of the given data.

    PWCCA is a variant of the Canonical Correlation Analysis (CCA) that uses projection weights to
    compute the similarity between two sets of activations.

    Reference: https://arxiv.org/abs/1806.05759
    """

    def __init__(self, metric_config: BaseMetricConfig, *args):
        super().__init__(metric_config, *args)

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

        return compute_pwcca(
            np_source_component_layer_data, np_target_component_layer_data
        )
