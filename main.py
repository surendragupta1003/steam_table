from flask import Flask, jsonify, request
from pyXSteam.XSteam import XSteam

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Enthalpy Calculation API!"

@app.route('/enthalpy', methods=['GET', 'POST'])
def calculate_enthalpy():
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            # Extract data from JSON request body
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Request body must be JSON"}), 400
            
            pressure = float(data['pressure'])
            temperature = float(data['temperature'])
        
        elif request.method == 'POST':
            # Extract data from JSON request body
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Request body must be JSON"}), 400

            pressure = float(data['pressure'])
            temperature = float(data['temperature'])

        # Calculate enthalpy
        steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
        enthalpy_in_KJKg = steamTable.h_pt(pressure, temperature)
        enthalpy_in_KcalKg = enthalpy_in_KJKg / 4.184

        # Format enthalpy values to 2 decimal places
        enthalpy_in_KJKg = round(enthalpy_in_KJKg, 2)
        enthalpy_in_KcalKg = round(enthalpy_in_KcalKg, 2)

        # Prepare result JSON
        result = {
            "enthalpy_KJ_Kg": enthalpy_in_KJKg,
            "enthalpy_kcal_Kg": enthalpy_in_KcalKg
        }

        # Return JSON response
        return jsonify(result), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key in JSON data: {str(e)}"}), 400

    except ValueError as e:
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
