from app import app,db,bcrypt
from flask import  render_template, request, redirect, url_for,flash,jsonify
from app.models import User,RegistrationForm,Todo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

###---------------------------Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        if not username or not password or not email:
            flash("Username, Password, and Email are required")
            return redirect(url_for('register_page'))

        exists_user = User.query.filter_by(username=username).first()
        if exists_user:
            flash('Username Already Exists')
            return redirect(url_for('register_page'))

        exists_email = User.query.filter_by(email=email).first()
        if exists_email:
            flash('Email Already Exists')
            return redirect(url_for('register_page'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Signup Successful', 'success')
        return redirect(url_for('login_page'))

    return render_template('register.html', form=form)

########---------------------------Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username & Password are Required')
            return redirect(url_for('login_page'))

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid Username or Password')
            return redirect(url_for('login_page'))

        if not bcrypt.check_password_hash(user.password, password):
            flash('Invalid Username or Password')
            return redirect(url_for('login_page'))

        access_token = create_access_token(identity=user.id)  # Create JSON web token
        return jsonify({'access_token': access_token}), 200

    return render_template('login.html')


####------------------------------------Todo List Page
# Create Todo Item
@app.route('/api/todo', methods=['POST'])
@jwt_required()
def create_todo():
    description = request.json.get('description')
    if not description:
        return jsonify({'message': 'Missing description'}), 400

    user_id = get_jwt_identity()
    todo_item = Todo(user_id=user_id, description=description)
    db.session.add(todo_item)
    db.session.commit()
    return jsonify({'message': 'Todo item created successfully'}), 201

# Update Todo Item
@app.route('/api/todo/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    description = request.json.get('description')
    if not description:
        return jsonify({'message': 'Missing description'}), 400

    todo_item = Todo.query.get(todo_id)
    if not todo_item:
        return jsonify({'message': 'Todo item not found'}), 404

    todo_item.description = description
    db.session.commit()
    return jsonify({'message': 'Todo item updated successfully'}), 200

# Delete Todo Item
@app.route('/api/todo/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo_item = Todo.query.get(todo_id)
    if not todo_item:
        return jsonify({'message': 'Todo item not found'}), 404

    db.session.delete(todo_item)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted successfully'}), 200