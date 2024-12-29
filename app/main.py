import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())
    for line in process.stderr:
        print(line.strip(), file=sys.stderr)

    process.wait()
    return process.returncode 

def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    return_code = run_command([command] + args)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
