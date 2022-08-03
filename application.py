import os
from flask import Flask, request, render_template, url_for, send_file, flash, redirect
from CaptionsSplitterSrt import CaptionsSplitter
from CaptionsGeneratorSrt import CaptionsGenerator
from aws import upload_file
from transcribe import s3toTranscribe
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'mp3'}

application = Flask(__name__)
application.secret_key = os.urandom(24)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route("/")
def caption():
	return render_template("index.html", status = "Vamos começar!"), 200

@application.route('/', methods=['GET', 'POST'])
def generateCaption():
	x = render_template("index.html", status = "Estamos trabalhando! ")

	if request.method == 'POST':

		# check if the post request has the file part
		if "File" not in request.files:
			flash('No file part')
			return redirect(request.url)

		file = request.files['File']

		# if user does not select file, browser also submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):

			filename = secure_filename(file.filename)
			file.save(os.path.join(THIS_FOLDER, filename))
			fileAdd = upload_file(filename, 'zoeaws')

			fileJSON = s3toTranscribe(filename, fileAdd)

			if fileJSON.empty:
				return render_template("index.html", status = "A transcrição falhou :("), 200

			else:
				captionName = "Legenda-" + filename.rsplit('.', 1)[0] + ".srt"
				caption = CaptionsSplitter(fileJSON)
				CaptionsGenerator(caption, captionName)

				captionAWS = upload_file(captionName, 'zoeaws')

				return render_template("index.html", status = "Funcionou!", captionFile = captionAWS), 200

		return render_template("index.html", status = "Algo estanho aconteceu :/"), 200

	return render_template("index.html", status = "Deu errado :'("), 200

# run the app.
if __name__ == "__main__":
	application.debug = True
	application.run()





