import main  # type: ignore
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class classes(Resource):
    def get(self):
        if("username" in request.headers and "password" in request.headers):
            return jsonify(main.getClasses(request.headers["username"], request.headers["password"]))
        else:
            return "need username and password"


class studentInfo(Resource):
    def get(self):
        if("username" in request.headers and "password" in request.headers):
            return jsonify(main.getStudentInfo(request.headers["username"], request.headers["password"]))
        else:
            return "need username and password"


class schedule(Resource):
    def get(self, mp):
        if("username" in request.headers and "password" in request.headers):
            return jsonify(main.getSched(request.headers["username"], request.headers["password"], mp))
        else:
            return "need username and password"


api.add_resource(classes, "/classes")
api.add_resource(studentInfo, "/studentInfo")
api.add_resource(schedule, "/schedule/<mp>")

if __name__ == "__main__":
    app.run()
