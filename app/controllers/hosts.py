from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.host import Host
from app.models.game_server import GameServer
from app.utils.network import check_host_status
import json

hosts_bp = Blueprint('hosts', __name__)

@hosts_bp.route('/hosts')
@login_required
def index():
    """List all hosts for the current user."""
    hosts = Host.query.filter_by(user_id=current_user.id).all()
    return render_template('hosts/index.html', title='My Hosts', hosts=hosts)

@hosts_bp.route('/hosts/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new host."""
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        port = request.form.get('port', 22, type=int)
        description = request.form.get('description')
        
        if not name or not address:
            flash('Name and address are required!', 'danger')
            return render_template('hosts/new.html', title='New Host')
            
        host = Host(
            name=name,
            address=address,
            port=port,
            description=description,
            user_id=current_user.id
        )
        
        db.session.add(host)
        db.session.commit()
        
        flash(f'Host "{name}" created successfully!', 'success')
        return redirect(url_for('hosts.index'))
        
    return render_template('hosts/new.html', title='New Host')

@hosts_bp.route('/hosts/<int:id>')
@login_required
def show(id):
    """Show host details."""
    host = Host.query.get_or_404(id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to view this host.', 'danger')
        return redirect(url_for('hosts.index'))
        
    # Get all game servers for this host
    game_servers = GameServer.query.filter_by(host_id=host.id).all()
    
    return render_template('hosts/show.html', title=host.name, host=host, game_servers=game_servers)

@hosts_bp.route('/hosts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a host."""
    host = Host.query.get_or_404(id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to edit this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    if request.method == 'POST':
        host.name = request.form.get('name')
        host.address = request.form.get('address')
        host.port = request.form.get('port', 22, type=int)
        host.description = request.form.get('description')
        
        if not host.name or not host.address:
            flash('Name and address are required!', 'danger')
            return render_template('hosts/edit.html', title=f'Edit {host.name}', host=host)
        
        db.session.commit()
        
        flash(f'Host "{host.name}" updated successfully!', 'success')
        return redirect(url_for('hosts.show', id=host.id))
        
    return render_template('hosts/edit.html', title=f'Edit {host.name}', host=host)

@hosts_bp.route('/hosts/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a host."""
    host = Host.query.get_or_404(id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        flash('You do not have permission to delete this host.', 'danger')
        return redirect(url_for('hosts.index'))
    
    name = host.name
    db.session.delete(host)
    db.session.commit()
    
    flash(f'Host "{name}" deleted successfully!', 'success')
    return redirect(url_for('hosts.index'))

@hosts_bp.route('/hosts/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    """Update host status."""
    host = Host.query.get_or_404(id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        status = request.json.get('status')
        host.update_status(status)
        db.session.commit()
        return jsonify({'success': True, 'status': host.status})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating host status: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@hosts_bp.route('/hosts/<int:id>/check', methods=['POST'])
@login_required
def check_host_status(id):
    """Check the actual status of a host."""
    host = Host.query.get_or_404(id)
    
    # Security check - only allow access to own hosts
    if host.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        is_online = host.check_status()
        db.session.commit()
        return jsonify({
            'success': True,
            'status': host.status,
            'message': host.status_message,
            'is_online': is_online
        })
    except Exception as e:
        current_app.logger.error(f"Error checking host status: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while checking host status'}), 500 