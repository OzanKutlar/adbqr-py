import subprocess
import sys

from .adb import run_adb

HELP_MESSAGE = """\
\x1B[1mReset ADB\x1B[0m

This will disconnect all wireless devices and restart the ADB server.
Any active connections, including USB devices and running scrcpy
sessions, will be dropped.
"""

# Fixed, bounded sequence. Order matters: disconnect before killing the
# daemon so devices are cleanly dropped rather than abandoned.
_STEPS = (
    ("Disconnecting all devices", ["disconnect"]),
    ("Stopping ADB server", ["kill-server"]),
    ("Starting ADB server", ["start-server"]),
)


def _describe_failure(result: subprocess.CompletedProcess) -> str:
    """Pick the most useful output stream from a failed adb invocation."""
    for stream in (result.stderr, result.stdout):
        if stream and stream.strip():
            return stream.strip()
    return "no output from adb"


def _run_step(label: str, args: list[str]) -> bool:
    """Run a single adb command, printing its outcome. Returns success."""
    if not label or not args:
        raise ValueError("reset step requires a label and adb arguments")

    print(f"{label}...", end=" ", flush=True)

    try:
        result = run_adb(args)
    except (OSError, subprocess.SubprocessError) as exc:
        print("failed.")
        print(f"  Could not run adb: {exc}")
        return False

    # adb exits 0 for several conditions that are really failures, so the
    # output has to be checked as well as the return code.
    combined = f"{result.stdout or ''}{result.stderr or ''}".lower()
    if result.returncode != 0 or "error:" in combined:
        print("failed.")
        print(f"  ADB output: {_describe_failure(result)}")
        return False

    print("done.")
    return True


def run() -> None:
    """Disconnect every device and restart the ADB server."""
    print(HELP_MESSAGE)

    results = {}
    for label, args in _STEPS:
        # Every step is attempted even if an earlier one failed. Bailing
        # out early could leave the user with no running daemon at all.
        results[args[0]] = _run_step(label, args)

    if all(results.values()):
        print("\nADB server restarted successfully.")
        return

    if results.get("start-server"):
        print(
            "\nADB server is running, but some steps reported problems."
            " Re-run 'adbqr reset' if devices still misbehave."
        )
        return

    print(
        "\nFailed to start the ADB server. Check that your adb executable"
        " is valid and that no other process is holding port 5037."
    )
    sys.exit(1)
