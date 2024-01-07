from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prebuiltsystem import run_function
from ultralytics import YOLO
from io import BytesIO
from PIL import Image
import io
import base64
import numpy as np 
import cv2
from pine import getanswer
from component import ramfunc, cpufunc,gpufunc,psufunc,mobofunc,storfunc
import requests

class_mapping = {
    0: 'CPU',
    1: 'GPU',
    2: 'HDD',
    3: 'MOTHERBOARD',
    4: 'PSU',
    5: 'RAM',
    6: 'SSD'
}

def alternative():
    try:
        
        # Get the image file from the user's request
        image = request.files['fileUpload']
        if len(image.read()) > 2 * 1024 * 1024:  # 2 MB in bytes
            return render_template('index.html', error='File size exceeds 2MB')
        #postProcessed = clahe(image)
        #print(postProcessed)
        if not image:
            raise ValueError("No Image Provided")
  
        # Prepare the data to send to the Ultralytics API
        url = "https://api.ultralytics.com/v1/predict/ynSBfJYksFVQUmJiKkmu"
        headers = {"x-api-key": "1f752d22c016d6b879ff47610a64828ef2d080d29e"}
        data = {"size": 640, "confidence": 0.25, "iou": 0.45}

        # Make a request to the Ultralytics API
        response = requests.post(url, headers=headers, data=data, files={"image": image})

        # Check for a successful response
        response.raise_for_status()
        results = response.json()
        if len(results) > 0:
            return render_template('new.html', classify=[results['data'][0]['name'],results['data'][0]['confidence']])
        else:
            return render_template('index.html',error="Please provide a computer component image")
        #session['inference'] = response.json()
        # Render the 'new.html' template with the API response
        

    except Exception as e:
        return jsonify({'error': str(e)})

def adaptive_wiener_filter(image, kernel_size=(5, 5), noise_var=0.01):
    # Convert the image to grayscale if it's not already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute local mean and local variance using a square neighborhood
    local_mean = cv2.blur(image, kernel_size)
    local_variance = cv2.boxFilter(image ** 2, -1, kernel_size) - local_mean ** 2

    # Compute global variance of the image
    global_variance = np.var(image)

    # Compute the adaptive filter weights
    filter_weights = local_variance / (local_variance + noise_var)
    filter_weights = np.minimum(1.0, np.maximum(0.0, filter_weights))

    # Apply the adaptive filter to the image
    filtered_image = local_mean + filter_weights * (image - local_mean)

    # Convert NumPy array to PIL image
    pil_image = Image.fromarray(filtered_image)

    return pil_image

def apply_clahe(image):
    # Convert PIL Image to OpenCV format (BGR)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert BGR to LAB color space
    lab_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)

    # Extract the L channel
    l_channel = lab_image[:, :, 0]

    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    clahe_l_channel = clahe.apply(l_channel)

    # Replace the original L channel with the CLAHE-processed channel
    lab_image[:, :, 0] = clahe_l_channel

    # Convert LAB back to BGR
    clahe_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

    # Convert BGR back to RGB (PIL format)
    pil_image = Image.fromarray(cv2.cvtColor(clahe_image, cv2.COLOR_BGR2RGB))

    return pil_image

def convert_filestorage_to_pil(filestorage):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'jfif'}
    
    if '.' not in filestorage.filename or filestorage.filename.split('.')[-1].lower() not in allowed_extensions:
        raise ValueError('Invalid file type')
    
    # Read the file into a BytesIO buffer
    byteImgIO = io.BytesIO()
    byteImg = Image.open(filestorage)
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()

    dataBytesIO = io.BytesIO(byteImg)
    trynew = Image.open(dataBytesIO)
    awf = adaptive_wiener_filter(np.array(trynew))
    # Apply CLAHE to the image
    clahe_applied = apply_clahe(trynew)
    
    return [clahe_applied,trynew]
    #return trynew

app = Flask(__name__)
app.secret_key = 'Matt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file
db = SQLAlchemy(app)
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

def save(image_str): 
    image_data = ImageData(data=image_str)
    db.session.add(image_data)
    db.session.commit()
    session['picID'] = image_data.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/component')
def findComponents():
    return render_template('component.html')    

@app.route('/pre_built')
def findPre_built():
    return render_template('recommend.html') 
   
@app.route('/querying')
def querying():
    return render_template('questionanswering.html')    
     

 
@app.route('/your_route')
def your_route():
    try:
        # Simulate data retrieval or processing
        #result = {"prediction": "Your prediction", "image_url": "your_image_url.jpg"}
        #session['resultImg'] = result
        # Render the 'new.html' template with the simulated data    
        return render_template('new.html')

    except Exception as e:
        return jsonify({'error': str(e)})
    


@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        # Get user selections from the form
        category = request.form['category']
        subcategory = request.form['subcategory']
        budget = int(request.form['budget'])
        results =run_function(category, subcategory, budget)
        unicodess = u"\u279C"
        # Process the selections (you can replace this with your actual processing logic)
        result = session.get('resultImg', {})
        
        inference = session.get('inference',{})
        category = f'{category} {unicodess} {subcategory}'
        #template results[selected,best][per computer][attributes]
        # Pass the result to the template
        return render_template('recommend.html', recommend1=results[0], recommend2 =results[1] , category=category.upper())
     


@app.route('/detect', methods=['POST'])
def detect_objects():
    file = request.files['fileUpload']
    try:
        # Get the image file from the user's request
        
        if len(file.read()) > 5 * 1024 * 1024:  # 2 MB in bytes
            return render_template('index.html', error='File size exceeds 2MB')
        #postProcessed = clahe(image)
        #print(postProcessed)
        if not file:
            raise ValueError("No Image Provided")

        # Prepare the data to send to the Ultralytics API
        model = YOLO('tech.pt')
        #print("test")
        pil_image = convert_filestorage_to_pil(file)
        #print("bro")
        results = model.predict(pil_image[0], imgsz=640, conf=0.35, iou=0.25)
        results1 = model.predict(pil_image[1], imgsz=640, conf=0.35, iou=0.25)
        if len(results) > 0:
            print(results)
            confidence_tensor = results[0].boxes.conf.clone().detach()
            class_id_tensor = results[0].boxes.cls.clone().detach()
            confidence = confidence_tensor[0].item()
            class_id = int(class_id_tensor[0].item())
            Oldconfidence_tensor = results1[0].boxes.conf.clone().detach()
            Oldconfidence = Oldconfidence_tensor[0].item()
            Oldclass_id_tensor = results1[0].boxes.cls.clone().detach()
            Oldclass_id = int(Oldclass_id_tensor[0].item())
            improvedAcc = confidence - Oldconfidence
            class_name = class_mapping.get(class_id, 'Unknown')
            Oldclass_name = class_mapping.get(Oldclass_id, 'Unknown')

            if confidence > Oldconfidence:

                #print(f'Class: {class_name}, Confidence: {confidence:.4f}')
                for r in results:
                    im_array = r.plot()  
                    im = Image.fromarray(im_array[..., ::-1])  
                    #im.show() 
                    pil_image[0] = Image.fromarray(im_array[..., ::-1])  
                    buffered = io.BytesIO()
                    pil_image[0].save(buffered, format="PNG")
                    image_str = buffered.getvalue()

                classified = [class_name,confidence,str(improvedAcc)+'%']
                session['classification'] = classified
                save(image_str)
                image_data_id = session.get('picID', None)
                
                
                image_data = ImageData.query.get(image_data_id)
                pic = base64.b64encode(image_data.data).decode('utf-8')
                
                
                return render_template('new.html', result1=pic, classify = classified, improved=classified)
            else:
                for r in results:
                    im_array = r.plot()  
                    im = Image.fromarray(im_array[..., ::-1])  
                    #im.show() 
                    pil_image[1] = Image.fromarray(im_array[..., ::-1])  
                    buffered = io.BytesIO()
                    pil_image[1].save(buffered, format="PNG")
                    image_str = buffered.getvalue()

                classified = [Oldclass_name,Oldconfidence,"negative improvements so the image will reverted back to old values"]
                session['classification'] = classified
                save(image_str)
                image_data_id = session.get('picID', None)
                
                
                image_data = ImageData.query.get(image_data_id)
                pic = base64.b64encode(image_data.data).decode('utf-8')
                
                return render_template('new.html', result1=pic, classify = classified, improved=classified)
        else:
            return render_template('index.html', error='The model could not handle the prediction, try one item at a time')
        
    except Exception as e:
        return render_template('index.html', error='Unfortunately, The model can only classify the general components of a computer. Try inputting a motherboard.')





@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data from the request
        full_name = request.form.get('full-name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Save form data to the database
        new_message = ContactMessage(full_name=full_name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({'error': str(e)})

 
@app.route('/answer', methods=['POST'])
def answer():
    if request.method == 'POST':
       
        question = request.form['question']
        prediction = getanswer(question)
        # Call your Q&A model to get the answer based on the user's question
        # Replace the following line with your actual Q&A model inference code
        result = session.get('resultImg', {})
        
        inference = session.get('inference',{})

        return render_template('questionanswering.html', question=question, answer=prediction)
    
@app.route('/goto')
def getComponentHTML():
    result = session.get('resultImg', {})
    inference = session.get('inference',{})
    return render_template('component.html',result=result, result1=inference)

@app.route('/getcomponent', methods=['GET', 'POST'])
def componentFunction():
    result = session.get('resultImg', {})
    inference = session.get('inference',{})
    if request.method == 'POST':
        selectedoption = request.form['component']
        budget = float(request.form['budget'])
        category = request.form['category']
        if category == 'ram':
            data = ramfunc(budget, selectedoption)
        elif category == 'cpu':
            data = cpufunc(budget, selectedoption)
        elif category == 'gpu':
            data = gpufunc(budget, selectedoption)
        elif category == 'psu':
            data = psufunc(budget, selectedoption)
        elif category == 'mobo':
            data = mobofunc(budget, selectedoption)
        elif category == 'storage':
            data = storfunc(budget, selectedoption)
        attributes = set()
        for item in data:
            attributes.update(item.keys())

    # Convert set to list and sort for consistent order
    attributes = sorted(list(attributes))
    return render_template('component.html',result=result, result1=inference,attributes=attributes,data=data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
