import socket
from typing import Tuple, Optional
import struct
import json
import re
from mcclient import SLPClient, QueryClient, BedrockSLPClient
import a2s

def check_minecraft_server(address: str, port: int) -> Tuple[bool, str, Optional[dict]]:
    """
    Check if a Minecraft server is running and get its status.
    Uses mcclient-lib to query both Java and Bedrock servers.
    
    Args:
        address: The server address
        port: The server port
        
    Returns:
        Tuple[bool, str, Optional[dict]]: (is_running, message, status_data)
    """
    try:
        # Try Java server first
        try:
            client = SLPClient(address, port)
            status = client.get_status()
            
            status_data = {
                'version': status.version.name,
                'players': {
                    'online': status.players.online,
                    'max': status.players.max,
                    'list': status.players.list if hasattr(status.players, 'list') else []
                },
                'description': status.motd,
                'protocol': status.version.protocol
            }
            
            return True, "Server is running (Java Edition)", status_data
            
        except Exception as java_error:
            # If Java fails, try Bedrock
            try:
                bedrock_client = BedrockSLPClient(address, port)
                status = bedrock_client.get_status()
                
                status_data = {
                    'version': status.version.name,
                    'players': {
                        'online': status.players.online,
                        'max': status.players.max,
                        'list': []  # Bedrock doesn't provide player list
                    },
                    'description': status.motd,
                    'protocol': status.version.protocol,
                    'server_id': status.server_id
                }
                
                return True, "Server is running (Bedrock Edition)", status_data
                
            except Exception as bedrock_error:
                # Try Query protocol as last resort (if enabled on server)
                try:
                    query_client = QueryClient(address, port)
                    status = query_client.get_status()
                    
                    status_data = {
                        'version': status.version.name,
                        'players': {
                            'online': status.players.online,
                            'max': status.players.max,
                            'list': status.players.list if hasattr(status.players, 'list') else []
                        },
                        'description': status.motd,
                        'map': status.map,
                        'plugins': status.plugins if hasattr(status, 'plugins') else []
                    }
                    
                    return True, "Server is running (Query Protocol)", status_data
                    
                except Exception as query_error:
                    # All methods failed
                    return False, "Server appears to be offline or unreachable", None
                    
    except Exception as e:
        return False, f"Error checking server: {str(e)}", None

def check_valheim_server(address: str, port: int) -> Tuple[bool, str, Optional[dict]]:
    """
    Check if a Valheim server is running and get its status.
    Uses python-a2s to query the server using Source Engine Query protocol.
    
    Args:
        address: The server address
        port: The server port
        
    Returns:
        Tuple[bool, str, Optional[dict]]: (is_running, message, status_data)
    """
    try:
        # Query server info
        info = a2s.info((address, port))
        
        # Get player list
        try:
            players = a2s.players((address, port))
            player_list = [{'name': p.name, 'score': p.score, 'duration': p.duration} for p in players]
        except Exception:
            player_list = []
        
        # Get server rules
        try:
            rules = a2s.rules((address, port))
        except Exception:
            rules = {}
        
        status_data = {
            'name': info.server_name,
            'map': info.map_name,
            'players': {
                'online': info.player_count,
                'max': info.max_players,
                'bots': info.bot_count,
                'list': player_list
            },
            'version': info.version,
            'password_protected': info.password_protected,
            'vac_enabled': info.vac_enabled,
            'rules': rules
        }
        
        return True, "Server is running", status_data
        
    except Exception as e:
        return False, f"Error checking server: {str(e)}", None

def check_game_server(address: str, game_type: str, port: int) -> Tuple[bool, str, Optional[dict]]:
    """
    Check if a game server is running based on its type.
    
    Args:
        address: The server address
        game_type: The type of game server (minecraft, valheim, etc.)
        port: The server port
        
    Returns:
        Tuple[bool, str, Optional[dict]]: (is_running, message, status_data)
    """
    game_type = game_type.lower()
    
    if game_type == 'minecraft':
        return check_minecraft_server(address, port)
    elif game_type == 'valheim':
        return check_valheim_server(address, port)
    else:
        # For unknown game types, just check if the port is open
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((address, port))
            sock.close()
            
            if result == 0:
                return True, "Server port is open", None
            else:
                return False, "Server port is closed", None
                
        except Exception as e:
            return False, f"Error checking server: {str(e)}", None 