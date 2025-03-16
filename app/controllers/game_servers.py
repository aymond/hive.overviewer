from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.host import Host
from app.models.game_server import GameServer
from app.models.game_config import GameConfig
import json

game_servers_bp = Blueprint('game_servers', __name__)

@game_servers_bp.route('/hosts/<int:host_id>/servers/new', methods=['GET', 'POST'])
@login_required
def new(host_id):
    """Create a new game server for a host."""
    host = Host.query.get_or_404(host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add game servers to this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        game_type = request.form.get('game_type')
        server_port = request.form.get('server_port', type=int)
        query_port = request.form.get('query_port', type=int)
        max_players = request.form.get('max_players', 10, type=int)
        auto_start = request.form.get('auto_start') == '1'
        install_path = request.form.get('install_path')
        description = request.form.get('description')
        
        if not name or not game_type or not server_port:
            flash('Name, game type, and server port are required!', 'danger')
            return render_template('game_servers/new.html', title='New Game Server', host=host)
            
        game_server = GameServer(
            name=name,
            game_type=game_type,
            server_port=server_port,
            query_port=query_port,
            max_players=max_players,
            auto_start=auto_start,
            install_path=install_path,
            host_id=host.id
        )
        
        db.session.add(game_server)
        db.session.commit()
        
        flash(f'Game server "{name}" created successfully!', 'success')
        return redirect(url_for('hosts.show', id=host.id))
        
    return render_template('game_servers/new.html', title='New Game Server', host=host)

@game_servers_bp.route('/hosts/<int:host_id>/servers', methods=['POST'])
@login_required
def create(host_id):
    """Process the game server creation form submission."""
    host = Host.query.get_or_404(host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add game servers to this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    name = request.form.get('name')
    game_type = request.form.get('game_type')
    server_port = request.form.get('server_port', type=int)
    query_port = request.form.get('query_port', type=int)
    max_players = request.form.get('max_players', 10, type=int)
    auto_start = request.form.get('auto_start') == '1'
    install_path = request.form.get('install_path')
    description = request.form.get('description')
    
    if not name or not game_type or not server_port:
        flash('Name, game type, and server port are required!', 'danger')
        return redirect(url_for('game_servers.new', host_id=host.id))
        
    game_server = GameServer(
        name=name,
        game_type=game_type,
        server_port=server_port,
        query_port=query_port,
        max_players=max_players,
        auto_start=auto_start,
        install_path=install_path,
        host_id=host.id
    )
    
    db.session.add(game_server)
    db.session.commit()
    
    flash(f'Game server "{name}" created successfully!', 'success')
    return redirect(url_for('hosts.show', id=host.id))

@game_servers_bp.route('/servers/<int:id>')
@login_required
def show(id):
    """Show game server details."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to view this game server.', 'danger')
        return redirect(url_for('hosts.index'))
        
    # Get all configurations for this game server
    configs = GameConfig.query.filter_by(game_server_id=game_server.id).all()
    
    return render_template('game_servers/show.html', 
                          title=game_server.name, 
                          game_server=game_server, 
                          host=host,
                          configs=configs)

@game_servers_bp.route('/servers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a game server."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to edit this game server.', 'danger')
        return redirect(url_for('hosts.index'))
    
    if request.method == 'POST':
        game_server.name = request.form.get('name')
        game_server.game_type = request.form.get('game_type')
        game_server.server_port = request.form.get('server_port', type=int)
        game_server.query_port = request.form.get('query_port', type=int)
        game_server.max_players = request.form.get('max_players', 10, type=int)
        game_server.auto_start = request.form.get('auto_start') == '1'
        game_server.install_path = request.form.get('install_path')
        game_server.description = request.form.get('description')
        
        if not game_server.name or not game_server.game_type or not game_server.server_port:
            flash('Name, game type, and server port are required!', 'danger')
            return render_template('game_servers/edit.html', 
                                 title=f'Edit {game_server.name}', 
                                 game_server=game_server,
                                 host=host)
        
        db.session.commit()
        
        flash(f'Game server "{game_server.name}" updated successfully!', 'success')
        return redirect(url_for('game_servers.show', id=game_server.id))
        
    return render_template('game_servers/edit.html', 
                         title=f'Edit {game_server.name}', 
                         game_server=game_server,
                         host=host)

@game_servers_bp.route('/servers/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    """Process the game server update form submission."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to edit this game server.', 'danger')
        return redirect(url_for('hosts.index'))
    
    game_server.name = request.form.get('name')
    game_server.game_type = request.form.get('game_type')
    game_server.server_port = request.form.get('server_port', type=int)
    game_server.query_port = request.form.get('query_port', type=int)
    game_server.max_players = request.form.get('max_players', 10, type=int)
    game_server.auto_start = request.form.get('auto_start') == '1'
    game_server.install_path = request.form.get('install_path')
    game_server.description = request.form.get('description')
    
    if not game_server.name or not game_server.game_type or not game_server.server_port:
        flash('Name, game type, and server port are required!', 'danger')
        return redirect(url_for('game_servers.edit', id=game_server.id))
    
    db.session.commit()
    
    flash(f'Game server "{game_server.name}" updated successfully!', 'success')
    return redirect(url_for('game_servers.show', id=game_server.id))

@game_servers_bp.route('/servers/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a game server."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to delete this game server.', 'danger')
        return redirect(url_for('hosts.index'))
    
    name = game_server.name
    host_id = host.id
    db.session.delete(game_server)
    db.session.commit()
    
    flash(f'Game server "{name}" deleted successfully!', 'success')
    return redirect(url_for('hosts.show', id=host_id))

@game_servers_bp.route('/servers/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    """Update game server status."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        status = request.json.get('status')
        game_server.update_status(status)
        db.session.commit()
        return jsonify({'success': True, 'status': game_server.status})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating game server status: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@game_servers_bp.route('/servers/<int:id>/control', methods=['POST'])
@login_required
def control(id):
    """Control game server operations (start, stop, restart)."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    action = request.json.get('action')
    if action not in ['start', 'stop', 'restart']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    
    try:
        # Here you would implement actual server control logic
        # For now, we'll just update the status
        if action == 'start':
            game_server.update_status('running')
        elif action == 'stop':
            game_server.update_status('stopped')
        elif action == 'restart':
            game_server.update_status('restarting')
            # Simulating a restart delay
            # In a real implementation, you would use a task queue
            
        db.session.commit()
        return jsonify({
            'success': True, 
            'status': game_server.status,
            'message': f'Server {action} operation initiated'
        })
    except Exception as e:
        current_app.logger.error(f"Error controlling game server: {str(e)}")
        return jsonify({'success': False, 'message': f'Error during {action} operation'}), 500

@game_servers_bp.route('/servers/<int:id>/check', methods=['POST'])
@login_required
def check_status(id):
    """Check the actual status of a game server."""
    game_server = GameServer.query.get_or_404(id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        # Check game server status
        is_running, message, status_data = game_server.check_status()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'status': game_server.status,
            'message': message,
            'status_data': status_data,
            'is_running': is_running
        })
    except Exception as e:
        current_app.logger.error(f"Error checking game server status: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while checking server status'}), 500

@game_servers_bp.route('/hosts/<int:host_id>/servers/docker', methods=['POST'])
@login_required
def create_from_docker(host_id):
    """Create a new game server from a Docker Compose file."""
    host = Host.query.get_or_404(host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add game servers to this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    try:
        name = request.form.get('name')
        server_port = request.form.get('server_port', type=int)
        max_players = request.form.get('max_players', type=int)
        auto_start = bool(request.form.get('auto_start'))
        config_method = request.form.get('config_method')
        
        if not name or not server_port or not max_players:
            flash('Name, server port, and max players are required!', 'danger')
            return redirect(url_for('hosts.show', id=host.id))
        
        # Get Docker Compose content based on method
        if config_method == 'upload':
            # Handle Docker Compose file upload
            if 'docker_compose' not in request.files:
                flash('Docker Compose file is required when using upload method!', 'danger')
                return redirect(url_for('hosts.show', id=host.id))
                
            docker_compose_file = request.files['docker_compose']
            if docker_compose_file.filename == '':
                flash('No selected file!', 'danger')
                return redirect(url_for('hosts.show', id=host.id))
                
            # Read and validate docker-compose file
            docker_compose_content = docker_compose_file.read().decode('utf-8')
        else:
            # Handle generated configuration
            docker_compose_content = request.form.get('generated_docker_compose')
            if not docker_compose_content:
                flash('Docker Compose configuration is required!', 'danger')
                return redirect(url_for('hosts.show', id=host.id))
        
        # Create installation directory
        install_path = f'/opt/gameservers/{name.lower().replace(" ", "_")}'
        
        # Create the game server
        game_server = GameServer(
            name=name,
            game_type='docker',  # Special type for Docker-based servers
            server_port=server_port,
            max_players=max_players,
            auto_start=auto_start,
            install_path=install_path,
            host_id=host.id,
            status='installing'  # Set initial status
        )
        
        db.session.add(game_server)
        db.session.commit()
        
        # Create Docker Compose configuration
        config = GameConfig(
            name='docker-compose.yml',
            file_path=f'{install_path}/docker-compose.yml',
            file_type='yaml',
            content=docker_compose_content,
            is_active=True,
            game_server_id=game_server.id
        )
        
        db.session.add(config)
        db.session.commit()
        
        # TODO: Trigger async task to set up Docker environment
        
        flash(f'Docker-based game server "{name}" created successfully!', 'success')
        return redirect(url_for('hosts.show', id=host.id))
        
    except Exception as e:
        current_app.logger.error(f"Error creating Docker game server: {str(e)}")
        flash('Error creating game server: ' + str(e), 'danger')
        return redirect(url_for('hosts.show', id=host.id))

@game_servers_bp.route('/hosts/<int:host_id>/servers/java', methods=['POST'])
@login_required
def create_from_java(host_id):
    """Create a new game server from Java configuration."""
    host = Host.query.get_or_404(host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add game servers to this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    try:
        name = request.form.get('name')
        server_port = request.form.get('server_port', type=int)
        max_players = request.form.get('max_players', type=int)
        auto_start = bool(request.form.get('auto_start'))
        java_version = request.form.get('java_version')
        memory = request.form.get('memory', type=int)
        
        if not name or not server_port or not max_players or not java_version or not memory:
            flash('All fields are required!', 'danger')
            return redirect(url_for('hosts.show', id=host.id))
        
        # Handle server.properties file upload
        if 'server_properties' not in request.files:
            flash('Server properties file is required!', 'danger')
            return redirect(url_for('hosts.show', id=host.id))
            
        properties_file = request.files['server_properties']
        if properties_file.filename == '':
            flash('No selected file!', 'danger')
            return redirect(url_for('hosts.show', id=host.id))
            
        # Read and validate server.properties
        properties_content = properties_file.read().decode('utf-8')
        
        # Create installation directory
        install_path = f'/opt/gameservers/{name.lower().replace(" ", "_")}'
        
        # Create the game server
        game_server = GameServer(
            name=name,
            game_type='minecraft',  # Assuming Java-based servers are Minecraft
            server_port=server_port,
            max_players=max_players,
            auto_start=auto_start,
            install_path=install_path,
            host_id=host.id,
            status='installing'  # Set initial status
        )
        
        db.session.add(game_server)
        db.session.commit()
        
        # Create server.properties configuration
        config = GameConfig(
            name='server.properties',
            file_path=f'{install_path}/server.properties',
            file_type='properties',
            content=properties_content,
            is_active=True,
            game_server_id=game_server.id
        )
        
        db.session.add(config)
        
        # Create Java configuration
        java_config = {
            'version': java_version,
            'memory': memory,
            'args': [
                f'-Xmx{memory}G',
                f'-Xms{memory}G',
                '-XX:+UseG1GC',
                '-XX:+ParallelRefProcEnabled',
                '-XX:MaxGCPauseMillis=200',
                '-XX:+UnlockExperimentalVMOptions',
                '-XX:+DisableExplicitGC',
                '-XX:+AlwaysPreTouch',
                '-XX:G1NewSizePercent=30',
                '-XX:G1MaxNewSizePercent=40',
                '-XX:G1HeapRegionSize=8M',
                '-XX:G1ReservePercent=20',
                '-XX:G1HeapWastePercent=5',
                '-XX:G1MixedGCCountTarget=4',
                '-XX:InitiatingHeapOccupancyPercent=15',
                '-XX:G1MixedGCLiveThresholdPercent=90',
                '-XX:G1RSetUpdatingPauseTimePercent=5',
                '-XX:SurvivorRatio=32',
                '-XX:+PerfDisableSharedMem',
                '-XX:MaxTenuringThreshold=1'
            ]
        }
        
        java_settings = GameConfig(
            name='java_settings.json',
            file_path=f'{install_path}/java_settings.json',
            file_type='json',
            content=json.dumps(java_config, indent=2),
            is_active=True,
            game_server_id=game_server.id
        )
        
        db.session.add(java_settings)
        db.session.commit()
        
        # TODO: Trigger async task to download and set up Java environment
        
        flash(f'Java-based game server "{name}" created successfully!', 'success')
        return redirect(url_for('hosts.show', id=host.id))
        
    except Exception as e:
        current_app.logger.error(f"Error creating Java game server: {str(e)}")
        flash('Error creating game server: ' + str(e), 'danger')
        return redirect(url_for('hosts.show', id=host.id)) 