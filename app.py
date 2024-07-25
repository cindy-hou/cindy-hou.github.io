from flask import Flask, request, send_file, redirect, url_for, render_template
import os
import subprocess
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        uploaded_file = request.files.get('file')

        if not task or not uploaded_file:
            return redirect(url_for('index'))

        # Save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            uploaded_file.save(temp_file.name)

            # Determine the script to run based on the task
            if task == 'generate_plans':
                script = 'main_logic.py'
            # elif task == 'international_model':
            #     script = 'setup.py'
            else:
                return redirect(url_for('index'))

            # Run the script with the uploaded file
            output_file = f'/tmp/output_{task}.xlsx'
            result = subprocess.run(['python', script, temp_file.name, output_file], capture_output=True)

            if result.returncode != 0:
                return f"Error occurred: {result.stderr.decode()}"

            # Serve the output file for download
            return send_file(output_file, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
