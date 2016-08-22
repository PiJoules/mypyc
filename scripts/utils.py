# -*- coding: utf-8 -*-

"""
Script utility functions.
"""

import logging
import sys

LOGGER = logging.getLogger(__name__)


def base_parse_args(parser):
    """Base argument parser decorator."""
    parser.add_argument("filename", help=".pc file to compile.")

    # Logging/debugging
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Logging verbosity. More verbose means more "
                        "logging info.")

    args = parser.parse_args()

    # Configure logger
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s",
                        stream=sys.stderr)
    if args.verbose == 1:
        LOGGER.setLevel(logging.INFO)
    elif args.verbose == 2:
        LOGGER.setLevel(logging.DEBUG)

    return args

