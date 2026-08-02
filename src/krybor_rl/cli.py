"""Compatibility imports for the original command-line module path."""

from __future__ import annotations

from .interfaces.cli import build_parser, main

__all__ = ["build_parser", "main"]
