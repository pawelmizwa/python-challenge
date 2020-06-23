from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequestKeyError
from flask_basicauth import BasicAuth
from helpers.files_handler import FileHandler
from config import prod
import logging

logger = logging.getLogger("example")
app = Flask(__name__)
api = Api(app)
app.config["BASIC_AUTH_USERNAME"] = prod.local_user
app.config["BASIC_AUTH_PASSWORD"] = prod.local_password
basic_auth = BasicAuth(app)
app.config["BASIC_AUTH_FORCE"] = True


class Nesting_level_error(Exception):
    pass


class Data(Resource):
    def __init__(self):
        self.fh = FileHandler(
            input_path=prod.input_path,
            output_path=prod.output_path,
            nesting_keys=prod.nesting_keys,
        )

    def post(self):
        try:
            raw_data = self.fh.get_data_from_file()
            nesting_level = request.args["nesting_level"]
            level = self.get_nesting_level(nesting_level)
            nested_result = self.fh.convert_list_of_dicts_to_nested_dict(
                nesting_level=level, raw_data=raw_data
            )
            # self.fh.write_data_to_file() ### not needed
            response = make_response(jsonify(nested_result), 200)
        except BadRequestKeyError as e:
            response = make_response(
                {"message": "Please specify nesting_level in params"}, 400
            )
            logger.warning(msg=e)
        except ValueError as e:
            response = make_response(
                {"message": "Please provide nesting level in correct format"}, 400
            )
            logger.warning(msg=e)
        except FileNotFoundError as e:
            logger.error(msg=e)
            response = make_response({"message": "Data import system issue"}, 500)
        except Exception as e:
            logger.critical(msg=e)
            response = make_response({"message": "System issue"}, 500)
        return response

    def get_nesting_level(self, nesting_level):
        level = int(nesting_level.split("_")[-1])
        return level


api.add_resource(Data, "/data")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=4002)
