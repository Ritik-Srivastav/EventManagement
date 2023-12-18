from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import or_
from flask_bcrypt import Bcrypt
from datetime import datetime 
from sqlalchemy import and_
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_POOL_SIZE'] = 20 

db = SQLAlchemy(app)

# Your models and database setup

with app.app_context():
    # Create tables
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, default=0)
    membership_taken = db.Column(db.Boolean, default=False)

# Assuming you already have the User model defined

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationship with Product
    products = db.relationship('Product', backref='section', lazy=True)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    manufacture_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    count = db.Column(db.Integer)
    price = db.Column(db.Float)

    # Foreign Key for Section
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

class Purchased(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # User Information
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    
    # Product Information
    product_name = db.Column(db.String(50), nullable=False)
    product_count = db.Column(db.Integer)
    product_price = db.Column(db.Float)


with app.app_context():
    # Create tables
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], address=data['address'], password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Include additional user information in the response
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'role': user.role
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/searchProducts',methods=['GET'])
def search_products():
    search_query = request.args.get('query', '')

    # Use SQLAlchemy's or_ to search for the query in multiple columns
    results = Product.query.filter(
        or_(
            Product.name.ilike(f'%{search_query}%'),
            Product.manufacture_date.ilike(f'%{search_query}%'),
            Product.expiry_date.ilike(f'%{search_query}%'),
            db.cast(Product.count, db.String).ilike(f'%{search_query}%'),
            db.cast(Product.price, db.String).ilike(f'%{search_query}%')
        )
    ).all()

    # Convert the results to a list of dictionaries
    products = [{'id': result.id,
                  'name': result.name,
                  'manufacture_date': result.manufacture_date,
                  'expiry_date': result.expiry_date,
                  'count': result.count,
                  'price': result.price}
                 for result in results]

    return jsonify({'products': products})


@app.route('/addSection', methods=['POST'])
def add_section():
    try:
        data = request.get_json()

        if 'name' not in data:
            return jsonify({'error': 'Section name is required'}), 400

        new_section = Section(name=data['name'])
        db.session.add(new_section)
        db.session.commit()

        return jsonify({'message': 'Section added successfully'}), 201

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/getSections', methods=['GET'])
def get_sections():
    try:
        sections = Section.query.all()
        sections_list = [{"id": section.id, "name": section.name} for section in sections]
        return jsonify({"sections": sections_list}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Edit section
@app.route('/editSection/<int:section_id>', methods=['PUT'])
def edit_section(section_id):
    try:
        data = request.get_json()
        new_name = data.get('name')

        section = Section.query.get(section_id)
        if not section:
            return jsonify({'error': 'Section not found'}), 404

        section.name = new_name
        db.session.commit()

        return jsonify({'message': 'Section edited successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Delete section
@app.route('/deleteSection/<int:section_id>', methods=['DELETE'])
def delete_section(section_id):
    try:
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'error': 'Section not found'}), 404

        db.session.delete(section)
        db.session.commit()

        return jsonify({'message': 'Section deleted successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/addProduct', methods=['POST'])
def add_product():
    try:
        data = request.get_json()

        new_product = Product(
            name=data['name'],
            manufacture_date=datetime.strptime(data['manufacture_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(),
            count=data['count'],
            price=data['price'],
            section_id=data['section_id']
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/getProducts', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        print("Products:", products)  # Add this line to log the products to the console
        products_list = [{
            "id": product.id,
            "name": product.name,
            "manufacture_date": str(product.manufacture_date),
            "expiry_date": str(product.expiry_date),
            "count": product.count,
            "price": product.price,
            "section_id": product.section_id
        } for product in products]
        return jsonify({"products": products_list}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Edit product
@app.route('/editProduct/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    try:
        data = request.get_json()

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product.name = data['name']
        product.manufacture_date = datetime.strptime(data['manufacture_date'], '%Y-%m-%d').date()
        product.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        product.count = data['count']
        product.price = data['price']

        db.session.commit()

        return jsonify({'message': 'Product edited successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Delete product
@app.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/buyProducts', methods=['POST'])
def buy_products():
    try:
        data = request.get_json()
        user_id = data['user_id']
        purchased_items = data['purchasedItems']

        for item in purchased_items:
            product_name = item['product_name']
            product_count = item['product_count']

            # Update the remaining product count in the Product table
            product = Product.query.filter_by(name=product_name).first()
            if product:
                product.count -= product_count

            # Add the purchased item to the Purchased table
            purchased_item = Purchased(
                user_id=user_id,
                user_name=data['user_name'],
                user_email=data['user_email'],
                product_name=product_name,
                product_count=product_count,
                product_price=item['product_price']
            )
            db.session.add(purchased_item)

        db.session.commit()
        return jsonify({'message': 'Purchase successful'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to complete the purchase'}), 500

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product_count(product_id):
    data = request.get_json()

    product = Product.query.get(product_id)

    if product:
        new_count = data.get('count', product.count)
        product.count = new_count
        db.session.commit()

        return jsonify({'message': 'Product count updated successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404
    


# Add a new endpoint to fetch users based on roles
@app.route('/getUsersByRole', methods=['GET'])
def get_users_by_role():
    try:
        # Fetch users with role 1 (vendor)
        vendors = User.query.filter_by(role=1).all()

        # Fetch users with role 0 (regular user)
        regular_users = User.query.filter_by(role=0).all()

        # Convert the results to a list of dictionaries
        vendors_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role} for user in vendors]
        regular_users_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role} for user in regular_users]

        return jsonify({'vendors': vendors_list, 'regularUsers': regular_users_list})

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/update-membership', methods=['POST'])
def update_membership():
    try:
        data = request.get_json()

        # Find the user's membership record
        user = User.query.get(data['user_id'])

        if user:
            # Update membership information
            user.membership_taken = True
            db.session.commit()

            return jsonify({'message': 'Membership updated successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/remove-membership', methods=['POST'])
def remove_membership():
    try:
        data = request.get_json()

        # Find the user's membership record
        user = User.query.get(data['user_id'])

        if user:
            # Update membership information
            user.membership_taken = False
            db.session.commit()

            return jsonify({'message': 'Membership removed successfully'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

# Add a new endpoint to fetch all Purchased data
@app.route('/getPurchasedData', methods=['GET'])
def get_purchased_data():
    try:
        purchased_data = Purchased.query.all()
        data_list = [{
            "id": purchase.id,
            "user_name": purchase.user_name,
            "user_email": purchase.user_email,
            "product_name": purchase.product_name,
            "product_count": purchase.product_count,
            "product_price": purchase.product_price,
        } for purchase in purchased_data]
        return jsonify({"purchased_data": data_list}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    app.run(debug=True)