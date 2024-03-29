from importlib.resources import path
from flask import Flask, render_template, send_file, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import csv


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('design.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return render_template('design.html')
      #return 'file uploaded successfully'  

@app.route("/downloader")
def downloader():
     
    return render_template('yml_display.html')

@app.route("/will_download")
def fetch():
    return send_file("kafka.yml",as_attachment=True)

@app.route('/auth')
def auth():

    authorization_url = workos.client.sso.get_authorization_url(
        domain = CUSTOMER_EMAIL_DOMAIN,
        redirect_uri = url_for('auth_callback', _external=True),
        state = {},
        connection = CUSTOMER_CONNECTION_ID 
    )

    return redirect(authorization_url)
    

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    print(code)
    profile = workos.client.sso.get_profile_and_token(code)
    p_profile = profile.to_dict()
    first_name = p_profile['profile']['first_name']

    if "picture" in p_profile['profile']['raw_attributes']:
        image = p_profile['profile']['raw_attributes']['picture']
    else: 
        image = "../static/images/rbc_logo.png"

    raw_profile = p_profile['profile']


    return render_template('login_successful.html', first_name=first_name, image=image, raw_profile=raw_profile)

@app.route("/create_yaml/")
def move_forward():
    csvfile = open('template.csv', 'r')
# Save a CSV Reader object.
    datareader = csv.reader(csvfile, delimiter=',', quotechar='"')

# Empty array for data headings, which we will fill with the first row from our CSV.
    data_headings = []

    filename = "kafka" + '.yml'
    new_yaml = open(filename, 'w')


# Loop through each row...
    for row_index, row in enumerate(datareader):

# If this is the first row, populate our data_headings variable.
      if row_index == 0:
       data_headings = row

# Othrwise, create a YAML file from the data in this row...
      else:
		# Open a new file with filename based on index number of our current row.
		#filename = str(row_index) + '.yml'
		#new_yaml = open(filename, 'w')

		# Empty string that we will fill with YAML formatted text based on data extracted from our CSV.
       yaml_text = ""

		# Loop through each cell in this row...
       for cell_index, cell in enumerate(row):

			# Compile a line of YAML text from our headings list and the text of the current cell, followed by a linebreak.
			# Heading text is converted to lowercase. Spaces are converted to underscores and hyphens are removed.
			# In the cell text, line endings are replaced with commas.
        cell_heading = data_headings[cell_index].lower().replace(" ", " ").replace("-", "").replace("&","-").replace("!"," ")
        cell_text = cell_heading + ": " + cell.replace("\n", ", ") + "\n"

			# Add this line of text to the current YAML string.
        yaml_text += cell_text
            
		# Write our YAML string to the new text file and close it.
       new_yaml.write(yaml_text)
           
		#new_yaml.close()

# We're done! Close the CSV file.
    new_yaml.close()
    csvfile.close()
        
    #forward_message = "oving Forward..."
    #return send_file("kafka.yml",as_attachment=True)
    return render_template('design.html')
   



if __name__=='__main__':
    app.run(debug="true")
