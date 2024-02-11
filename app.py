import os

from api.summarizer import *
from api.report import *
from api.llm import *

from flask import (Flask,request,send_from_directory,jsonify)
from flask_cors import CORS

from base64 import b64decode

from io import BytesIO

app = Flask(__name__)
# Enable CORS
CORS(app)
summ1 = Summarizer()
llm = LLM()
report = Report()

@app.route('/')
def index():
   return "EQWECARE"

@app.route("/send_report",methods=['POST','GET'])
def generate_report():
   if(request.method == 'POST'):
      content = request.get_json()
      summaries =[]
      content_data = json.loads(content['data'])
      pdfs = content_data['pdfs']
      user = content_data['users']

      inx =0 
      for pdf in pdfs:
         # Decode the Base64 string, making sure that it contains only valid characters
         bytes = b64decode(pdf.split(',')[1], validate=True)
         f = open('./cache/output_'+str(inx)+".pdf", 'wb')
         f.write(bytes)
         f.close()
         summaries.append(summ1.generate_pdf_to_text("output_"+str(inx)+".pdf"))

      user_summary,brief = llm.generate_summary_response(user)
      summaries.append(user_summary)
      brief += " " + summ1.generate_summary(summaries)
      report.generate_pdf_report([brief],['Summary Medical Report'])
   return send_from_directory(os.path.join(app.root_path, 'cache'),'report.pdf',mimetype='application/pdf')

@app.route("/get_bot_response",methods=['POST','GET'])
def get_bot_response():
   if(request.method == 'POST'):
      content = request.json['user_inp']
      response = llm.bot_trav_response(content)
      return jsonify({"response":response})

if __name__ == '__main__':
   app.run(debug=True)
