#!/bin/sh
set -e

# Requires the typer-cli package to be installed
# https://typer.tiangolo.com/typer-cli/
typer openopc2.cli utils docs --output CLI.md --name "openopc2 CLI"