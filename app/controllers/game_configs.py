from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.host import Host
from app.models.game_server import GameServer
from app.models.game_config import GameConfig
import json

game_configs_bp = Blueprint('game_configs', __name__)

@game_configs_bp.route('/servers/<int:server_id>/configs/new', methods=['GET', 'POST'])
@login_required
def new(server_id):
    """Create a new configuration file for a game server."""
    game_server = GameServer.query.get_or_404(server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add configurations to this server.', 'danger')
        return redirect(url_for('hosts.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        file_path = request.form.get('file_path')
        file_type = request.form.get('file_type', 'json')
        content = request.form.get('content')
        is_active = request.form.get('is_active') == '1'
        description = request.form.get('description')
        
        if not name or not file_path:
            flash('Name and file path are required!', 'danger')
            return render_template('game_configs/new.html', 
                                  title='New Configuration', 
                                  game_server=game_server,
                                  host=host)
            
        game_config = GameConfig(
            name=name,
            file_path=file_path,
            file_type=file_type,
            content=content,
            is_active=is_active,
            game_server_id=game_server.id
        )
        
        db.session.add(game_config)
        db.session.commit()
        
        flash(f'Configuration "{name}" created successfully!', 'success')
        return redirect(url_for('game_servers.show', id=game_server.id))
        
    return render_template('game_configs/new.html', 
                          title='New Configuration', 
                          game_server=game_server,
                          host=host)

@game_configs_bp.route('/servers/<int:server_id>/configs', methods=['POST'])
@login_required
def create(server_id):
    """Process the configuration creation form submission."""
    game_server = GameServer.query.get_or_404(server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to add configurations to this server.', 'danger')
        return redirect(url_for('hosts.index'))
    
    name = request.form.get('name')
    file_path = request.form.get('file_path')
    file_type = request.form.get('file_type', 'json')
    content = request.form.get('content')
    is_active = request.form.get('is_active') == '1'
    description = request.form.get('description')
    
    if not name or not file_path:
        flash('Name and file path are required!', 'danger')
        return redirect(url_for('game_configs.new', server_id=server_id))
        
    game_config = GameConfig(
        name=name,
        file_path=file_path,
        file_type=file_type,
        content=content,
        is_active=is_active,
        game_server_id=game_server.id
    )
    
    db.session.add(game_config)
    db.session.commit()
    
    flash(f'Configuration "{name}" created successfully!', 'success')
    return redirect(url_for('game_servers.show', id=game_server.id))

@game_configs_bp.route('/configs/<int:id>')
@login_required
def show(id):
    """Show configuration details."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to view this configuration.', 'danger')
        return redirect(url_for('hosts.index'))
        
    return render_template('game_configs/show.html', 
                          title=config.name, 
                          config=config, 
                          game_server=game_server,
                          host=host,
                          versions=[])  # Empty versions list until version history is implemented

@game_configs_bp.route('/configs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a configuration."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to edit this configuration.', 'danger')
        return redirect(url_for('hosts.index'))
    
    if request.method == 'POST':
        config.name = request.form.get('name')
        config.file_path = request.form.get('file_path')
        config.file_type = request.form.get('file_type', 'json')
        config.content = request.form.get('content')
        config.is_active = request.form.get('is_active') == '1'
        description = request.form.get('description')
        
        if not config.name or not config.file_path:
            flash('Name and file path are required!', 'danger')
            return render_template('game_configs/edit.html', 
                                 title=f'Edit {config.name}', 
                                 config=config,
                                 game_server=game_server,
                                 host=host)
        
        deploy_after_save = request.form.get('deploy_after_save') == '1'
        
        db.session.commit()
        
        flash(f'Configuration "{config.name}" updated successfully!', 'success')
        
        if deploy_after_save:
            # Simulate deployment
            flash(f'Configuration "{config.name}" has been deployed to the server.', 'success')
        
        return redirect(url_for('game_configs.show', id=config.id))
        
    return render_template('game_configs/edit.html', 
                         title=f'Edit {config.name}', 
                         config=config,
                         game_server=game_server,
                         host=host)

@game_configs_bp.route('/configs/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    """Process the configuration update form submission."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to edit this configuration.', 'danger')
        return redirect(url_for('hosts.index'))
    
    config.name = request.form.get('name')
    config.file_path = request.form.get('file_path')
    config.file_type = request.form.get('file_type', 'json')
    config.content = request.form.get('content')
    config.is_active = request.form.get('is_active') == '1'
    description = request.form.get('description')
    
    if not config.name or not config.file_path:
        flash('Name and file path are required!', 'danger')
        return redirect(url_for('game_configs.edit', id=config.id))
    
    deploy_after_save = request.form.get('deploy_after_save') == '1'
    
    db.session.commit()
    
    flash(f'Configuration "{config.name}" updated successfully!', 'success')
    
    if deploy_after_save:
        # Simulate deployment
        flash(f'Configuration "{config.name}" has been deployed to the server.', 'success')
    
    return redirect(url_for('game_configs.show', id=config.id))

@game_configs_bp.route('/configs/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a configuration."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to delete this configuration.', 'danger')
        return redirect(url_for('hosts.index'))
    
    name = config.name
    server_id = game_server.id
    db.session.delete(config)
    db.session.commit()
    
    flash(f'Configuration "{name}" deleted successfully!', 'success')
    return redirect(url_for('game_servers.show', id=server_id))

@game_configs_bp.route('/configs/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_active(id):
    """Toggle a configuration's active state."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        is_active = config.toggle_active()
        db.session.commit()
        return jsonify({
            'success': True, 
            'is_active': is_active,
            'message': f'Configuration {"activated" if is_active else "deactivated"}'
        })
    except Exception as e:
        current_app.logger.error(f"Error toggling configuration: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@game_configs_bp.route('/configs/<int:id>/deploy', methods=['POST'])
@login_required
def deploy(id):
    """Deploy a configuration to the game server."""
    config = GameConfig.query.get_or_404(id)
    game_server = GameServer.query.get_or_404(config.game_server_id)
    host = Host.query.get_or_404(game_server.host_id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    # For now, just simulate deploying
    # In a real implementation, you would connect to the host and write the file
    try:
        # Verify the config is active
        if not config.is_active:
            return jsonify({
                'success': False, 
                'message': 'Cannot deploy inactive configuration'
            }), 400
            
        # Simulated deployment
        # Update the last updated time to reflect the deployment
        config.updated_at = db.func.current_timestamp()
        db.session.commit()
        
        flash(f'Configuration "{config.name}" deployed successfully!', 'success')
        return redirect(url_for('game_configs.show', id=config.id))
    except Exception as e:
        current_app.logger.error(f"Error deploying configuration: {str(e)}")
        flash('Error during deployment: ' + str(e), 'danger')
        return redirect(url_for('game_configs.show', id=config.id)) 