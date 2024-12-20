from flask import Blueprint, render_template, request, flash, jsonify , redirect, url_for
from flask_login import login_required, current_user
from .models import Ticket, User
from . import db
import json

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
     # Shows tickets based on user role
    if current_user.role == "admin":
        # Admin sees all tickets
        tickets = Ticket.query.all()
    else:
        # Regular Users see only tickets assigned to them
        tickets = Ticket.query.filter_by(assigned_to=current_user.full_name).all()

    return render_template("home.html", user=current_user, tickets=tickets)

@views.route('/create-ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if current_user.role != "admin":
        flash("Access denied: Only admins can create tickets.", category="error")
        return redirect(url_for('views.home'))

    users = User.query.all()  # Fetch all users for assigning tickets
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        assigned_to = request.form.get('assigned_to')

        if not title or not description or not priority or not assigned_to:
            flash("All fields are required.", category="error")
        else:
            ticket = Ticket(
                title=title,
                description=description,
                priority=priority,
                assigned_to=assigned_to,
                created_by=current_user.id
            )
            db.session.add(ticket)
            db.session.commit()
            flash("Ticket created successfully!", category="success")
            return redirect(url_for('views.home'))
    return render_template("create_ticket.html", user=current_user, users=users)

@views.route('/edit-ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    # Admins can edit any ticket, users can only edit their own tickets
    if current_user.role != "admin" and ticket.created_by != current_user.id:
        flash("Access denied: You cannot edit this ticket.", category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        ticket.title = request.form.get('title')
        ticket.description = request.form.get('description')
        ticket.priority = request.form.get('priority')
        ticket.status = request.form.get('status')

        db.session.commit()
        flash("Ticket updated successfully!", category="success")
        return redirect(url_for('views.home'))
    return render_template("edit_ticket.html", user=current_user, ticket=ticket)

@views.route('/update-status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    ticket = Ticket.query.get_or_404(id)

    # Only assigned users can update ticket status
    if ticket.assigned_to != current_user.full_name:
        flash("Access denied: You cannot update the status of this ticket.", category="error")
        return redirect(url_for('views.home'))

    new_status = request.form.get('status')
    if new_status in ["Open", "In Progress", "Closed"]:
        ticket.status = new_status
        db.session.commit()
        flash("Ticket status updated successfully!", category="success")
    else:
        flash("Invalid status update.", category="error")
    return redirect(url_for('views.home'))

@views.route('/view-ticket/<int:id>')
@login_required
def view_ticket(id):
    # Fetch the ticket
    ticket = Ticket.query.get_or_404(id)

    # Admins can view all tickets
    if current_user.is_admin:
        return render_template("view_ticket.html", user=current_user, ticket=ticket)

    # Regular users can view only tickets assigned to them or created by them
    if ticket.assigned_to == current_user.full_name or ticket.created_by == current_user.id:
        return render_template("view_ticket.html", user=current_user, ticket=ticket)

    # If the user does not have permission, restrict access
    flash("Access denied: You cannot view this ticket.", category="error")
    return redirect(url_for('views.home'))

# @views.route('/update-status/<int:id>', methods=['POST'])
# @login_required
# def update_status(id):
#     # Allow users to update the status of their assigned tickets
#     ticket = Ticket.query.get_or_404(id)

#     if ticket.assigned_to != current_user.full_name:
#         flash("Access denied: You cannot update this ticket.", category="error")
#         return redirect(url_for('views.home'))
    
#     new_status = request.form.get('status')
#     if new_status in ["In Progress", "Closed"]:
#         ticket.status = new_status
#         db.session.commit()
#         flash("Ticket status updated successfully!", category="success")
#     else:
#         flash("Invalid status update.", category="error")
    
#     return redirect(url_for('views.home'))

# @views.route('/create-ticket', methods=['GET', 'POST'])
# @login_required
# def create_ticket():
#     # Allow users to create a new ticket
#     users = User.query.all()

#     if request.method == 'POST':
#         title = request.form.get('title')
#         description = request.form.get('description')
#         priority = request.form.get('priority')
#         assigned_to = request.form.get('assigned_to')  

#         # Validation
#         if not title or not description or not priority:
#             flash("Please fill in all required fields.", category="error")
#         else:
#             new_ticket = Ticket(
#                 title=title,
#                 description=description,
#                 priority=priority,
#                 assigned_to=assigned_to,
#                 created_by=current_user.id
#             )
#             db.session.add(new_ticket)
#             db.session.commit()
#             flash("Ticket created successfully!", category="success")
#             return redirect(url_for('views.home'))
        
#     return render_template("create_ticket.html", user=current_user, users=users)

# @views.route('/edit-ticket/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_ticket(id):
#     # Edit an existing ticket
#     ticket = Ticket.query.get_or_404(id)

#     if not (ticket.assigned_to == current_user.full_name or ticket.created_by == current_user.id):
#         flash("Access denied: You cannot edit this ticket.", category="error")
#         return redirect(url_for('views.home'))

#     if request.method == 'POST':
#         ticket.title = request.form.get('title')
#         ticket.description = request.form.get('description')
#         ticket.priority = request.form.get('priority')
#         if ticket.assigned_to == current_user.full_name:
#             ticket.status = request.form.get('status')

#         db.session.commit()
#         flash("Ticket updated successfully!", category="success")
#         return redirect(url_for('views.home'))

#     return render_template("edit_ticket.html", user=current_user, ticket=ticket)

