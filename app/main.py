import subprocess
import sys
import os
import shutil
import tempfile
import ctypes

def setup_environment(command, args):
    """
    Sets up a chroot environment in a temporary directory and executes a command.
    Args:
        executable_path (str): Path to the binary to be executed.
        command (list): Command to execute inside the chroot environment.
    """
    # Create a temporary directory for the chroot environment
    chroot_dir = tempfile.mkdtemp()
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    libc.unshare(0x20000000)
    try:

        shutil.copy(command, chroot_dir)
        os.chroot(chroot_dir)

        # Execute the command inside the chroot jail
        command = os.path.join("/", os.path.basename(command))
        result = subprocess.run(
                [command, *args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        # Pipe the outputs (stdout and stderr) to the parent process
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)

        return_code = result.returncode
        return return_code

    finally:
        if os.path.exists(chroot_dir):
            shutil.rmtree(chroot_dir)


def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    return_code = setup_environment(command, args)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
