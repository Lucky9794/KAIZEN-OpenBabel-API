from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/sdf_to_pdb', methods=['POST'])
def sdf_to_pdb():

    file = request.files['file']
    file.save("input.sdf")

    subprocess.run([
        "obabel",
        "input.sdf",
        "-O",
        "output.pdb"
    ])

    return send_file(
        "output.pdb",
        as_attachment=True,
        download_name="compound.pdb"
    )
