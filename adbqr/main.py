import click
from . import pair_qr, pair_code, connect, reset, adb

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A command-line tool for pairing devices with ADB via QR code."""
    adb.get_adb_path()
    if ctx.invoked_subcommand is None:
        pair_qr.run()

@cli.command("pair")
def pair():
    """Pair with QR code."""
    pair_qr.run()

@cli.command("manual")
def manual():
    """Pair with pairing code."""
    pair_code.run()

@cli.command("connect")
def connect_cmd():
    """Connect to an already paired device."""
    connect.run()

@cli.command("reset")
def reset_cmd():
    """Disconnect all devices and restart the ADB server."""
    reset.run()

if __name__ == "__main__":
    cli()
