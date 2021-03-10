import main  # type: ignore
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class login(Resource):
    def get(self):
        if(main.login(request.headers["username"], request.headers["password"]) == False):
            return "500"
        return "400"


class classes(Resource):
    def get(self):
        if("username" in request.headers and "password" in request.headers):
            if(main.login(request.headers["username"], request.headers["password"]) == False):
                return "400"  # incorrect login
            return jsonify(main.getClasses(request.headers["username"], request.headers["password"]))
        else:
            return "500"  # no/missing header data


class studentInfo(Resource):
    def get(self):
        if("username" in request.headers and "password" in request.headers):
            if(main.login(request.headers["username"], request.headers["password"]) == False):
                return "E2"  # incorrect login
            return jsonify(main.getStudentInfo(request.headers["username"], request.headers["password"]))
        else:
            return "E1"  # no/missing header data


class schedule(Resource):
    def get(self, mp):
        if("username" in request.headers and "password" in request.headers):
            if(main.login(request.headers["username"], request.headers["password"]) == False):
                return "E2"  # incorrect login
            return jsonify(main.getSched(request.headers["username"], request.headers["password"], mp))
        else:
            return "E1"  # no/missing header data

class day(Resource):
    def get(self):
        if("username" in request.headers and "password" in request.headers):
            if(main.login(request.headers["username"], request.headers["password"]) == False):
                return "E2"  # incorrect login
            return main.getCurrentDay(request.headers["username"], request.headers["password"])
        else:
            return "E1"  # no/missing header data


api.add_resource(classes, "/classes")
api.add_resource(studentInfo, "/studentInfo")
api.add_resource(schedule, "/schedule/<mp>")
api.add_resource(day, "/day")

if __name__ == "__main__":
    app.run()
