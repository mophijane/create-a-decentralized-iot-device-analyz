import json
import requests
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# IoT Device Information
devices = {
    "device1": {
        "device_id": "1234567890",
        "device_type": "temperature_sensor",
        "data": []
    },
    "device2": {
        "device_id": "2345678901",
        "device_type": "humidity_sensor",
        "data": []
    }
}

class DeviceAnalyzer(Resource):
    def get(self, device_id):
        if device_id in devices:
            return jsonify(devices[device_id])
        else:
            return jsonify({"error": "Device not found"})

    def post(self, device_id):
        data = request.get_json()
        if device_id in devices:
            devices[device_id]["data"].append(data)
            return jsonify({"message": "Data received successfully"})
        else:
            return jsonify({"error": "Device not found"})

class Analytics(Resource):
    def get(self):
        analytics_data = {}
        for device in devices.values():
            if device["data"]:
                analytics_data[device["device_id"]] = {
                    "avg": sum(device["data"]) / len(device["data"]),
                    "max": max(device["data"]),
                    "min": min(device["data"])
                }
        return jsonify(analytics_data)

api.add_resource(DeviceAnalyzer, '/device/<string:device_id>')
api.add_resource(Analytics, '/analytics')

if __name__ == '__main__':
    app.run(debug=True)