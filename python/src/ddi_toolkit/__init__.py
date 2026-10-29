"""ddi_toolkit: calculators from *Drug–Drug Interactions in Drug Safety and Pharmacovigilance*.

Each calculator reproduces a worked calculation in the book (Dr. Hafez Selim)
and cites it. Educational use only: the calculators teach the reasoning in the
book with simplified static models. They do not predict what happens in an
individual and must not be used for dosing or any other clinical decision.

Every calculator takes keyword inputs and returns a dict of named outputs::

    >>> from ddi_toolkit import auc_ratio_inhibition
    >>> round(auc_ratio_inhibition(fm=0.9, fraction_inhibited=0.9)["auc_ratio"], 1)
    5.3
"""

__version__ = "1.0.0"

from .disproportionality import (  # noqa: E402
    four_stratum_expectations,
    information_component,
    omega_shrinkage,
    prr_ror,
)
from .epi import (  # noqa: E402
    absolute_risk,
    co_exposure_sensitivity,
    proportion_ratio,
    reporting_rate,
    rule_of_three,
)
from .liver import liver_injury_r_ratio  # noqa: E402
from .pk import (  # noqa: E402
    auc_mic,
    auc_ratio_inhibition,
    clearance_pathways,
    dose_adjusted_exposure,
    fm_ceiling,
    induction_auc_ratio,
    inhibition_from_auc_ratio,
    protein_binding_displacement,
)
from .qt import exposure_qtc_line, qt_correction  # noqa: E402
from .timing import (  # noqa: E402
    de_induction_remaining,
    exposure_rise_after_inhibition,
    residual_inhibition,
    time_to_steady_state,
    washout,
)
from .registry import CALCULATORS  # noqa: E402

__all__ = sorted(CALCULATORS) + ["CALCULATORS", "__version__"]
