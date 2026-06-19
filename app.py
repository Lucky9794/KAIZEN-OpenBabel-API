from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)   # Enable CORS for GitHub Pages

@app.route("/")
def home():
    return "KAIZEN OpenBabel API is running!"

@app.route("/sdf_to_pdb", methods=["POST"])
def sdf_to_pdb():

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    input_file = "input.sdf"
    output_file = "output.pdb"

    file.save(input_file)

    try:
        result = subprocess.run(
            [
                "obabel",
                input_file,
                "-O",
                output_file
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"Open Babel Error:\n{result.stderr}", 500

        if not os.path.exists(output_file):
            return "PDB file was not generated", 500

        return send_file(
            output_file,
            as_attachment=True,
            download_name="compound.pdb"
        )

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
