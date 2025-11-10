from flask import Blueprint, redirect, render_template, flash, url_for

"""Basic routes controller for public pages.

This module handles routing for public-facing pages including
landing, about, and contact pages.
"""


# Create blueprint for public routes
main = Blueprint('main', __name__)

@main.route('/')
def index() -> str:
    """Render the landing page.
    
    Returns:
        str: Rendered HTML template for landing page
    """
    return render_template('public/landing/index.html')


@main.route('/about')
def about() -> str:
    """Render the about page.
    
    Returns:
        str: Rendered HTML template for about page
    """
    return render_template('public/about/index.html')


@main.route('/contact')
def contact() -> str:
    """Render the contact page.
    
    Returns:
        str: Rendered HTML template for contact page
    """
    return render_template('public/contact/index.html')


@main.route('/seed')
def seed_data() -> str:
    """Route to seed initial data into the database.
    
    Returns:
        str: Confirmation message
    """
    # Placeholder for seeding logic
    # seed_database()
    from seed.seed_users import clear_all, seed_roles, seed_users
    seed_roles()
    seed_users()

    flash("Seeding database...", "info")
    return redirect(url_for('main.index'))