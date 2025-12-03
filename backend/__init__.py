# backend/__init__.py
# Thin wrapper to expose the main application factory.

from .app import create_app

__all__ = ["create_app"]
