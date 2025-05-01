from flask import Flask,jsonify,render_template,request,redirect,url_for,session,flash,Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/cosmoweb'
app.secret_key = 'your_secret_key'


db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Customer(db.Model):
       customerid=db.Column(db.Integer,primary_key=True)
       customername=db.Column(db.String(80),unique=False,nullable=False)
       emailid=db.Column(db.String(120),unique=False,nullable=False)
       password=db.Column(db.String(120),unique=True,nullable=False)
       
#code for product catalog
class Product(db.Model):
    productid = db.Column(db.Integer, primary_key=True,nullable=False)
    productname = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    productbrand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)  # Stores image filename

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'), nullable=False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable=False)
    productname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    __table_args__=(db.UniqueConstraint('customerid','productid',name='unique_customer_product'),)

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='POST'):
         name=request.form.get('name')
         mail=request.form.get('mail')
         password=request.form.get('password')
         entry=Customer(customername=name,emailid=mail,password=password)
         db.session.add(entry)
         db.session.commit()
         
    return render_template('index.html',logged_in='user_id' in session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next') or request.referrer or url_for('productcat')  # Get previous page URL
    if request.method == 'POST':  # Only process login when form is submitted
        email = request.form.get('email')
        password = request.form.get('password')
        user = Customer.query.filter_by(emailid=email, password=password).first()

        if user:
            session['user_id'] = user.customerid  # Store user ID in session
            return redirect(next_page)
        else:
             return f"""
            <script>
                alert("Invalid Login Credentials!");
                window.location.href = "{next_page}";
            </script>
            """
    return Response(status=204) # Show login page on GET request


    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/productcatalog.html')
def productcat():
    products=Product.query.all() 
    return render_template('productcatalog.html',products=products,logged_in='user_id' in session)


@app.route('/productcatalog')
def product_catalog():
    category = request.args.get('category')  # Get category from URL
    brand = request.args.get('brand')  # Get brand from URL
    min_price = request.args.get('min_price', type=float)  # Get min price
    max_price = request.args.get('max_price', type=float)  # Get max price
    print(f"Brand: {brand}, Min Price: {min_price}, Max Price: {max_price}")

    query = Product.query  # Start with the base query

    if category:
        query = query.filter_by(category=category)  # Filter by category
    if brand and brand!='all':
        query = query.filter_by(productbrand=brand)  # Filter by brand
    if min_price is not None and max_price is not None:
        query = query.filter(Product.price.between(min_price, max_price))  # Filter by price range

    products = query.all()  # Get filtered products
    print(f"Filtered Products: {len(products)} found")  # Debugging

    return render_template('productcatalog.html', products=products)


@app.route('/add_to_cart/<int:productid>', methods=['POST'])
def add_to_cart(productid):
     if 'user_id' not in session:
        return redirect(url_for('login'))
     print("prod rece:",productid)
     customerid = session['user_id']
     product = Product.query.get(productid)
    
     if product:
        # Check if the product is already in the cart
        existing_cart_item = Cart.query.filter_by(customerid=customerid,productid=productid).first()

        if existing_cart_item:
            existing_cart_item.quantity += 1  # Increase quantity
        else:
            new_cart_item = Cart(
                customerid=customerid, 
                productid=productid,
                productname=product.productname,
                price=product.price,
                image=product.image,
                quantity=1
            )
            db.session.add(new_cart_item)
        
        db.session.commit()
        return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:productid>', methods=['POST'])
def remove_from_cart(productid):
     if 'user_id' not in session:
        return redirect(url_for('login'))
     customerid=session['user_id']
     item = Cart.query.filter_by(customerid=customerid, productid=productid).first()
     if item:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('cart'))

@app.route('/cart')
def cart():
     if 'user_id' not in session:
        return redirect(url_for('login'))
     
     customerid = session['user_id']
     cart_items = Cart.query.filter_by(customerid=customerid).all()
     cart_total = sum(item.price * item.quantity for item in cart_items)
     return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/ppy.html')
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    customerid = session['user_id']
    cart_items = Cart.query.filter_by(customerid=customerid).all()
    cart_total = sum(item.price * item.quantity for item in cart_items)

    if not cart_items:  # Prevent access if cart is empty
        return redirect(url_for('cart'))

    return render_template('ppy.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/submit-payment',methods=['POST'])
def success():
    if request.method== 'POST':
        next_page = url_for('productcat')
        return f"""
            <script>
                alert("Payment Successfull!");
                window.location.href = "{next_page}";
            </script>
            """

if __name__ == "__main__":
    app.run(debug=True)