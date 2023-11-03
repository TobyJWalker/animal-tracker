from flask import Flask, request, render_template, session, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from threading import Thread
from PIL import Image
from lib.validation import *
from jinja_markdown import MarkdownExtension
from time import sleep
from random import randint

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
APP_ENV = os.environ.get('APP_ENV', 'development')

if APP_ENV == 'test':
    UPLOAD_FOLDER = 'shared/images'
elif APP_ENV == 'production':
    UPLOAD_FOLDER = '/var/images'


# create the app and configure it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
create_db_tables()

# create ssl context
context = ('cert.pem', 'priv_key.pem')

# add markdown extension
app.jinja_env.add_extension(MarkdownExtension)

# check if an uploaded image is an actual image file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# compress and save images uploaded
def process_image(image, folder):
    secure_name = f'{folder}/{secure_filename(image.filename)}'

    with open(f'{UPLOAD_FOLDER}/{secure_name}', 'wb') as file:
        file.write(image.read())

    pil_image = Image.open(f"{UPLOAD_FOLDER}/{secure_name}")
    pil_image.thumbnail((500, 500))
    pil_image.save(f"{UPLOAD_FOLDER}/{secure_name}")


# route to generate/retrieve api key
@app.route('/api-key', methods=['GET'])
def get_api_key():
    if 'user_id' not in session:
        return redirect('/login')
    else:
        key = ApiKey.get_by_user_id(session['user_id'])

        if key == None:
            key = ApiKey.generate_key(session['user_id'])

        return f'Your api-key: {key}'

# route to get all animals through api-key
@app.route('/api/<string:api_key>/animals', methods=['GET'])
def get_animals(api_key):
    user = User.get_by_api_key(api_key)

    if user == None:
        return None
    else:
        animals = Animal.get_animals_by_user_id(user.id)
        json_data = [{
            'name': animal.name,
            'species': animal.species,
            'age': animal.age,
            'date_of_birth': datetime.strftime(animal.date_of_birth, '%Y-%m-%d'),
            'colour': animal.colour,
            'personality': animal.personality,
            'tag': animal.tag,
            'owner': animal.owner.username,
            'height': animal.height,
            'height_type': animal.height_type,
            'weight': animal.weight,
            'weight_type': animal.weight_type,
            'length': animal.length,
            'length_type': animal.length_type,
        } for animal in animals]
        return jsonify(json_data)

# route to get an animal through api-key
@app.route('/api/<string:api_key>/animals/<string:animal_name>', methods=['GET'])
def get_animal(api_key, animal_name):
    user = User.get_by_api_key(api_key)

    if user == None:
        return None
    else:
        animals = Animal.get_animals_by_user_id(user.id)

        for animal in animals:
            if animal.name.lower() == animal_name.lower():
                json_data = {
                    'name': animal.name,
                    'species': animal.species,
                    'age': animal.age,
                    'date_of_birth': datetime.strftime(animal.date_of_birth, '%Y-%m-%d'),
                    'colour': animal.colour,
                    'personality': animal.personality,
                    'tag': animal.tag,
                    'owner': animal.owner.username,
                    'height': animal.height,
                    'height_type': animal.height_type,
                    'weight': animal.weight,
                    'weight_type': animal.weight_type,
                    'length': animal.length,
                    'length_type': animal.length_type,
                }
                return jsonify(json_data)
        return None

# enforce https with aws
@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# route for image serving
@app.route('/shared/images/<folder>/<name>')
def download_file(folder, name):
    return send_from_directory(f'{app.config["UPLOAD_FOLDER"]}/{folder}', name)

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
    
# route to sort animal
@app.route('/animals/sort/<string:sort_by>-<string:order>/', methods=['GET'])
def sort_animals(sort_by, order):
    if 'user_id' not in session:
        return redirect('/login')
    
    animals = Animal.get_animals_by_user_id(session['user_id'])

    animals_sorted = Animal.sort_animals(animals, sort_by, order)

    return render_template('animal_list.html', animals=animals_sorted, sort_by=sort_by)
    

# add animal page
@app.route('/animals/add', methods=['GET'])
def add_animal():
    if 'user_id' in session:
        return render_template('new_animal.html')
    else:
        return redirect('/login')

# route to create a new animal
@app.route('/animals/add', methods=['POST'])
def create_animal():
    name = request.form['name']
    species = request.form['species']
    date_of_birth = request.form.get('date-of-birth')
    image = request.files.get('image', None)

    if image != None and allowed_file(image.filename):
        folder_name = f'{randint(0, 100000)}-{name}'
        os.mkdir(f'{UPLOAD_FOLDER}/{folder_name}')
            
        Thread(target=process_image, args=(image,folder_name,)).start()
        secure_name = f'/shared/images/{folder_name}/{secure_filename(image.filename)}'
    else:
        secure_name = None

    errors = generate_animal_errors(name, species)

    if errors == None:
        today = datetime.today()
        dob = date_of_birth.split('-')
        dob = [int(i) for i in dob]
        age = today.year - dob[0] - ((today.month, today.day) < (dob[1], dob[2]))

        Animal.create(name=name, 
                    species=species, 
                    owner=session['user_id'], 
                    date_of_birth=date_of_birth,
                    age=age,
                    img_url=secure_name,
                    height=0,
                    weight=0,
                    length=0,
                    )
        return redirect('/animals')
    else:
        return render_template('new_animal.html', errors=errors)

# route to delete an animal
@app.route('/animals/<int:animal_id>/delete', methods=['POST'])
def delete_animal(animal_id):
    if 'user_id' in session:
        animal = Animal.select().where(Animal.id == animal_id).get()

        if animal.owner.id != session['user_id']:
            return redirect('/animals')
        else:
            if animal.img_url != None:
                img_url_list = animal.img_url.split('/')
                img_url = f'{img_url_list[-2]}/{img_url_list[-1]}'
                try:
                    os.remove(f'{UPLOAD_FOLDER}/{img_url}')
                except:
                    pass
            Notes.delete().where(Notes.animal == animal).execute()
            Animal.delete().where(Animal.id == animal_id).execute()
            return redirect('/animals')
    else:
        return redirect('/login')

# route to view an animal
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

# route to add a note to an animal
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

# route to delete a note from an animal
@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    note = Notes.select().where(Notes.id == note_id).get()

    if note.animal.owner.id != session['user_id']:
        return redirect('/animals')
    else:
        Notes.delete().where(Notes.id == note_id).execute()
        return redirect(f'/animals/{note.animal.id}')
    
# route to get edit note form 
@app.route('/note/<int:note_id>/edit', methods=['GET'])
def edit_note_form(note_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    note = Notes.select().where(Notes.id == note_id).get()

    if note.animal.owner.id != session['user_id']:
        return redirect('/animals')
    else:
        return render_template('edit_note.html', note=note)

# route to edit a note
@app.route('/note/<int:note_id>/edit', methods=['POST'])
def edit_note_action(note_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    note = Notes.select().where(Notes.id == note_id).get()

    if note.animal.owner.id != session['user_id']:
        return redirect('/animals')
    else:
        content = request.form['content']
        content = content.replace('\n', '<br>')
        Notes.update(content=content).where(Notes.id == note_id).execute()
        return redirect(f'/animals/{note.animal.id}')

# route to show edit an animal form
@app.route('/animal/<int:animal_id>/edit', methods=['GET'])
def edit_animal_form(animal_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    animal = Animal.select().where(Animal.id == animal_id).get()

    if animal.owner.id != session['user_id']:
        return redirect('/animals')
    else:
        return render_template('edit_animal.html', animal=animal)
    
# route to edit an animal
@app.route('/animal/<int:animal_id>/edit', methods=['POST'])
def edit_animal(animal_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    animal = Animal.select().where(Animal.id == animal_id).get()

    if animal.owner.id != session['user_id']:
        return redirect('/animals')
    else:
        name = request.form.get('name', animal.name)
        species = request.form.get('species', animal.species)
        date_of_birth = request.form.get('date-of-birth', animal.date_of_birth)
        colour = request.form.get('colour', animal.colour)
        personality = request.form.get('personality', animal.personality)
        identification = request.form.get('identification', animal.tag)
        height = request.form.get('height', animal.height)
        height_type = request.form.get('height-type', animal.height_type)
        weight = request.form.get('weight', animal.weight)
        weight_type = request.form.get('weight-type', animal.weight_type)
        length = request.form.get('length', animal.length)
        length_type = request.form.get('length-type', animal.length_type)
        image = request.files.get('image', None)

        if image != None and allowed_file(image.filename):
            if animal.img_url != None:
                split_url = animal.img_url.split('/')
                if len(split_url) == 4:
                    folder_name = f'{randint(0, 100000)}-{animal.name}'
                    os.mkdir(f'{UPLOAD_FOLDER}/{folder_name}')
                else:
                    folder_name = split_url[-2]
                try:
                    os.remove(f'{UPLOAD_FOLDER}/{folder_name}/{animal.img_url.split("/")[-1]}')
                except:
                    pass
            else:
                folder_name = f'{randint(0, 100000)}-{animal.name}'
                os.mkdir(f'{UPLOAD_FOLDER}/{folder_name}')

            Thread(target=process_image, args=(image,folder_name,)).start()
            secure_name = f'/shared/images/{folder_name}/{secure_filename(image.filename)}'

        else:
            if animal.img_url != None:
                secure_name = animal.img_url
            else:
                secure_name = None

        errors = generate_animal_errors(name, species)

        if errors == None:
            today = datetime.today()
            dob = date_of_birth.split('-')
            dob = [int(i) for i in dob]
            age = today.year - dob[0] - ((today.month, today.day) < (dob[1], dob[2]))

            Animal.update(name=name, 
                        species=species, 
                        age=age,
                        colour=colour,
                        personality=personality,
                        tag=identification,
                        height=height,
                        height_type=height_type,
                        weight=weight,
                        weight_type=weight_type,
                        length=length,
                        length_type=length_type,
                        date_of_birth=date_of_birth, 
                        img_url=secure_name
                        ).where(Animal.id == animal_id).execute()
            
            sleep(0.5) # wait for image to be processed

            return redirect(f'/animals/{animal_id}')
        else:
            return render_template('edit_animal.html', errors=errors, animal=animal)


# run the app if file is executed
if __name__ == "__main__":
    if APP_ENV == 'test':
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=int(os.environ.get('PORT', 7474)))
    elif APP_ENV == 'production':
        app.secret_key = os.urandom(16)
        app.run(debug=False, host='0.0.0.0', port=7474, ssl_context=context)
    else:
        app.secret_key = os.urandom(16)
        app.run(debug=True, port=7474)
