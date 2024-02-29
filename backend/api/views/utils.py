import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app, abort, Request
from werkzeug.datastructures import FileStorage

class Utility:


    @staticmethod
    def parse_form_data(request: Request):
        form_data = request.form.to_dict()
        for key, value in form_data.items():
            if isinstance(value, str):
                form_data[key] = value = value.strip()
            # Convert boolean strings into actual booleans
        
            if value.lower() == 'true':
                form_data[key] = True
            elif value.lower() == 'false':
                form_data[key] = False
            else:
                # Convert numeric strings into actual numbers
                try:
                    # First, try to convert to int
                    form_data[key] = int(value)
                except ValueError:
                    try:
                        # If that fails, try to convert to float
                        form_data[key] = float(value)
                    except ValueError:
                        # If it's not a number or boolean, leave it as a string
                        pass
        return form_data

    @staticmethod
    def handle_file_upload(file: FileStorage, folder: str):
        if file.filename == '':
            abort(404, 'No selected file')
        if file and Utility.allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Check if the directory exists, if not, create it
            if not os.path.exists(folder):
                os.makedirs(folder)

            file_path = os.path.join(folder, filename)
            file.save(file_path)

            # Read the file into a byte array
            with open(file_path, 'rb') as f:
                blob = f.read()

            return file_path, blob

    @staticmethod
    def allowed_file(filename: str):
        allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def delete_file(filename: str ,folder: str):
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            abort(404, "The file does not exist")

    @staticmethod
    def secure_filename_with_time(file: FileStorage):
        return secure_filename(str(datetime.now().strftime("%Y%m%d-%H%M%S")) + file.filename)
    

    @staticmethod
    def validate_json(json_data: dict, fields: dict):
        for field, field_type in fields.items():
            if field not in json_data or json_data.get(field) is None or not isinstance(json_data.get(field), field_type):
                abort(400, description=f"Missing, empty or wrong type for {field}\
                    with {json_data.get(field)}. Expected {field_type}\
                        got {type(json_data.get(field))}")