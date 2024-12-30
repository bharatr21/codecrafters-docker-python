import subprocess
import sys
import os
import shutil
import tempfile

def setup_chroot_environment(command, args):
    """
    Sets up a chroot environment in a temporary directory and executes a command.
    Args:
        executable_path (str): Path to the binary to be executed.
        command (list): Command to execute inside the chroot environment.
    """
    # Create a temporary directory for the chroot environment
    chroot_dir = tempfile.mkdtemp()
    try:

        shutil.copy(command, chroot_dir)
        os.chroot(chroot_dir)

        # Execute the command inside the chroot jail
        command = os.path.join("/", os.path.basename(command))
        result = subprocess.run([command, *args], capture_output=True)

        # Pipe the outputs (stdout and stderr) to the parent process
        sys.stdout.write(result.stdout.decode("utf-8"))
        sys.stderr.write(result.stderr.decode("utf-8"))

        return_code = result.returncode
        return return_code

    finally:
        # Clean up the temporary directory
        if os.path.exists(chroot_dir):
            shutil.rmtree(chroot_dir)


def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    return_code = setup_chroot_environment(command, args)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
