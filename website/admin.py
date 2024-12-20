from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Ticket, User
from . import db

admin = Blueprint('admin', __name__)

# created to restrict access to admin users only, decorator to ensure only admins can access certain routes 
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admins only, Access denied!", category="error")
            return redirect(url_for('views.home'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin.route('/create-ticket', methods=['GET', 'POST'])
@login_required
@admin_required
def create_ticket():
    # Allow admin to create ticket
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')

        if not title or not description or not priority:
            flash("All fields are required to create a ticket", category="error")
        else:
            ticket = Ticket(
                title=title,
                description=description,
                priority=priority,
                created_by=current_user.id
            )
            db.session.add(ticket)
            db.session.commit()
            flash("A new Ticket has been created successfully!", category="success")
            return redirect(url_for('admin.view_tickets'))

    return render_template("create_ticket.html")

@admin.route('/edit-ticket/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_ticket(id):
    # admins can edit existing tickets 
    ticket = Ticket.query.get_or_404(id)
    if request.method == 'POST':
        ticket.title = request.form.get('title')
        ticket.description = request.form.get('description')
        ticket.priority = request.form.get('priority')
        ticket.status = request.form.get('status')
        db.session.commit()
        flash("Ticket has been updated successfully!", category="success")
        return redirect(url_for('admin.view_tickets'))

    return render_template("edit_ticket.html", ticket=ticket)

@admin.route('/admin-view-tickets/<int:id>', endpoint='admin_view_ticket')
@login_required
@admin_required
def view_tickets():
    # Display all tickets in the system to admins
    tickets = Ticket.query.all()
    return render_template("view_tickets.html", tickets=tickets)

@admin.route('/admin-delete-ticket/<int:id>', methods=['GET'])
@login_required
@admin_required
def confirm_delete_ticket(id):
    # Fetch the ticket and display confirmation page
    ticket = Ticket.query.get_or_404(id)
    return render_template("delete_ticket.html", ticket=ticket)

@admin.route('/admin-delete-ticket/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_ticket(id):
    # Allow admin user to delete tickets 
    ticket = Ticket.query.get_or_404(id)

    # Delete the ticket
    db.session.delete(ticket)
    db.session.commit()

    # Flash Message and redirect
    flash("Ticket has been deleted successfully!", category="success")
    return redirect(url_for('admin.view_tickets'))
