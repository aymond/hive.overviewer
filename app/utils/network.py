import subprocess
import platform
import socket
import paramiko
from typing import Tuple

def check_host_status(address: str, port: int = 22) -> Tuple[bool, str]:
    """
    Check if a host is online by attempting both a ping and an SSH port check.
    
    Args:
        address: The hostname or IP address to check
        port: The SSH port to check (default: 22)
        
    Returns:
        Tuple[bool, str]: (is_online, detailed_message)
    """
    # First try a basic ping
    try:
        # Determine the ping command based on the platform
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', address]
        
        # Run ping command with a timeout
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        ping_successful = True
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        ping_successful = False
    except Exception:
        ping_successful = False

    # Then check if the SSH port is open
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((address, port))
        port_open = (result == 0)
        sock.close()
    except Exception:
        port_open = False

    # Try to establish a basic SSH connection
    ssh_connectable = False
    if port_open:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Only try to connect for a short time
            ssh.connect(address, port=port, timeout=5, banner_timeout=5)
            ssh_connectable = True
            ssh.close()
        except Exception:
            ssh_connectable = False

    # Determine status and message based on checks
    if ssh_connectable:
        return True, "Host is online and SSH is accessible"
    elif port_open:
        return True, "Host is online but SSH authentication failed"
    elif ping_successful:
        return True, "Host is online but SSH port is closed"
    else:
        return False, "Host appears to be offline" 