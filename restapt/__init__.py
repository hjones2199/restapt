#! /usr/bin/env python3
"""Presents apt via a restful API"""
from flask import Flask, jsonify, abort, make_response
from flask_restful import Resource, Api
import packageman

APP = Flask(__name__)
API = Api(APP)

@APP.route('/')
def index():
    """Returns the URI"""
    return "restapt API root"


@APP.errorhandler(404)
def no_function(error):
    return make_response(jsonify({'ERROR': 'No such function'}), 404)


class PkgStatus(Resource):
    pkg_manager = packageman.Dpkg()
    def get(self, pkg_name):
        """Forwards request to package manager"""
        result = {
            'status':
            self.pkg_manager.pkg_status(pkg_name).decode('utf-8')
        }
        return jsonify(result)


API.add_resource(PkgStatus, '/pkgstatus/<pkg_name>')


if __name__ == '__main__':
    APP.run(debug=True)
