"""Allow ``python -m ddi_toolkit``. Educational use only; not for clinical decisions."""

import sys

from .cli import main

sys.exit(main())
