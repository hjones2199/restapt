#! /usr/bin/env python3
"""Presents apt via a restful API"""
from flask import Flask, jsonify, make_response
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
    """404 response for bad requests"""
    return make_response(jsonify({'ERROR': 'No such function'}), 404)


class PkgStatus(Resource):
    """Retrieves package status for a single package from manager"""
    pkg_manager = packageman.Dpkg()

    def get(self, pkg_name):
        """Returns package status as a JSON object"""
        stat = self.pkg_manager.pkg_status(pkg_name)
        result = {
            'status':
            'not found' if stat == '' else stat
        }
        return jsonify(result)


class PkgList(Resource):
    """JSONifies a list of all packages on the system"""
    pkg_manager = packageman.Dpkg()

    def get(self):
        """Returns list of packages as a JSON object"""
        pkgs = self.pkg_manager.list_pkgs().split('\n')
        parsed_pkgs = []
        for pkg in pkgs:
            if pkg == '':
                continue
            tmp_pkg = pkg.split('\t')
            pkg_sing_dict = {tmp_pkg[0]: tmp_pkg[1]}
            parsed_pkgs.append(pkg_sing_dict)
        return jsonify(parsed_pkgs)


API.add_resource(PkgStatus, '/pkgstatus/<pkg_name>')
API.add_resource(PkgList, '/pkglist')

if __name__ == '__main__':
    APP.run(debug=True)
