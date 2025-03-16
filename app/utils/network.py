import subprocess
import platform
import socket
import paramiko
from typing import Tuple

def check_host_status(address: str, port: int = 22) -> Tuple[bool, str]:
    """
    Check if a host is online by attempting a ping.
    
    Args:
        address: The hostname or IP address to check
        port: Unused parameter kept for backward compatibility
        
    Returns:
        Tuple[bool, str]: (is_online, detailed_message)
    """
    try:
        # Determine the ping command based on the platform
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', address]
        
        # Run ping command with a timeout
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        return True, "Host is online (ping successful)"
    except subprocess.TimeoutExpired:
        return False, "Host is offline (ping timeout)"
    except subprocess.CalledProcessError:
        return False, "Host is offline (ping failed)"
    except Exception as e:
        return False, f"Error checking host status: {str(e)}" 