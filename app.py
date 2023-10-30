from flask import Flask, request, render_template, session, redirect, send_from_directory
from werkzeug.utils import secure_filename
from threading import Thread
from PIL import Image
from lib.validation import *

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
APP_ENV = os.environ.get('APP_ENV', 'development')

# create the app and configure it
app = Flask(__name__)
create_db_tables()

# check if an uploaded image is an actual image file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# compress and save images uploaded
def process_image(image):
    secure_name = secure_filename(image.filename)

    if APP_ENV == 'production':
        with open(f'../shared/images/{secure_name}', 'wb') as file:
            file.write(image.read())
        pil_image = Image.open(f"../shared/images/{secure_name}")
        pil_image.thumbnail((500, 500))
        pil_image.save(f"../shared/images/{secure_name}")
    else:
        with open(f'images/{secure_name}', 'wb') as file:
            file.write(image.read())
        pil_image = Image.open(f"images/{secure_name}")
        pil_image.thumbnail((500, 500))
        pil_image.save(f"images/{secure_name}")

# overwrite the default static image file serving
@app.route('/images/<path:filename>')
def serve_image(filename):
    if APP_ENV == 'production':
        return send_from_directory('../shared/images', filename)
    else:
        return send_from_directory('images', filename)


# index redirect to sign up page
@app.route('/', methods=['GET'])
def index():
    return redirect('/signup')

# sign up page
@app.route('/signup', methods=['GET'])
def signup():
    if 'user_id' in session:
        return redirect('/animals')
    else:
        return render_template('signup.html')
    
@app.route('/signup', methods=['POST'])
def create_account():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_rep = request.form['password-confirm']

    errors = generate_signup_errors(username, email, password, password_rep)

    if errors == None:
        hashed_password = User.hash_password(password)
        User.create(username=username, email=email, password=hashed_password)
        return redirect('/login')
    else:
        return render_template('signup.html', errors=errors)

# login page
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect('/animals')
    else:
        return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = User.check_login(username, password)

    if user == None:
        return render_template('login.html', error=True)
    else:
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/animals')

# logout page
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# animals page
@app.route('/animals', methods=['GET'])
def animals():
    if 'user_id' in session:
        animals = Animal.get_animals_by_user_id(session['user_id'])
        return render_template('animal_list.html', animals=animals)
    else:
        return redirect('/login')

# add animal page
@app.route('/animals/add', methods=['GET'])
def add_animal():
    if 'user_id' in session:
        return render_template('new_animal.html')
    else:
        return redirect('/login')

@app.route('/animals/add', methods=['POST'])
def create_animal():
    name = request.form['name']
    species = request.form['species']
    date_of_birth = request.form.get('date-of-birth', None)
    image = request.files.get('image', None)

    if image != None and allowed_file(image.filename):
        Thread(target=process_image, args=(image,)).start()
        secure_name = secure_filename(image.filename)
    else:
        secure_name = ''

    errors = generate_animal_errors(name, species)

    if errors == None:
        Animal.create(name=name, 
                    species=species, 
                    owner=session['user_id'], 
                    date_of_birth=date_of_birth, 
                    img_url=f'/images/{secure_name}' if image != None else None
                    )
        return redirect('/animals')
    else:
        return render_template('new_animal.html', errors=errors)

@app.route('/animals/<int:animal_id>', methods=['GET'])
def view_animal(animal_id):
    if 'user_id' in session:
        try:
            animal = Animal.select().where(Animal.id == animal_id).get()
            notes = Notes.get_by_animal_id(animal_id)

            if animal.owner.id != session['user_id']:
                return redirect('/animals')
        except:
            return redirect('/animals')
        return render_template('animal_page.html', animal=animal, notes=notes)
    else:
        return redirect('/login')
    
@app.route('/animals/<int:animal_id>/notes/add', methods=['POST'])
def add_note(animal_id):
    if 'user_id' in session:
        animal = Animal.select().where(Animal.id == animal_id).get()

        if animal.owner.id != session['user_id']:
            return redirect('/animals')
        else:

            content = request.form['content']
            content = content.replace('\n', '<br>')

            Notes.create(content=content, animal=animal_id)

            return redirect(f'/animals/{animal_id}')
    else:
        return redirect('/login')



# run the app if file is executed
if __name__ == "__main__":
    if APP_ENV == 'test':
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=int(os.environ.get('PORT', 7474)))
    elif APP_ENV == 'production':
        app.secret_key = os.urandom(16)
        app.run(debug=False, host='0.0.0.0', port=7474)
    else:
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=7474)