from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from flask_cors import CORS
from model import Model
from model import Preprocessor

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")
# Init model
model = Model()
preprocessor = Preprocessor()
# SUPORT FUNCTION
def get_city_state(lat, lng):
    coordinates = f"{lat} , {lng}"

    location = geolocator.reverse(coordinates)
    address = location.raw['address']

    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')

    return {
        'city': city,
        'state': state,  
        'country': country
    }

# MAIN APP
app = Flask(__name__)
CORS(app)
# http://localhost:5000/nearest_city?latitude=37.7749&longitude=-122.4194
@app.route('/nearest_city', methods=['GET'])
def nearest_city():
    try:
        # Lấy tham số kinh độ và vĩ độ từ request
        user_latitude = float(request.args.get('latitude'))
        user_longitude = float(request.args.get('longitude'))
    except ValueError:
        return jsonify({'error': 'Invalid parameters'}), 400

    res_data = get_city_state(user_latitude, user_longitude)
    
    return jsonify(res_data)

@app.route('/forcast_price', methods=['POST'])
def forcast_price():
    try:
        if request.is_json:
            # Lấy dữ liệu JSON từ request
            req = request.get_json()
            # Xử lý dữ liệu ở đây
            preprocessor.select_processor(req['model_type'])  # chọn cách xử lý
            model.select_model(req['model_type'], req['model']) # chọn model
            # xử lý
            data = preprocessor.process(req['data']) # xử lý data đầu vào, và cả city sẽ cho kết quả khác với trong data
            if str(data) == '':
                return jsonify({"status": "success", 'result': ''})
            # chức năng của model ở đây
            result = model.predict(data)
            print(req['model_type'], req['model'])
            # Trả về phản hồi JSON (nếu cần)
            return jsonify({"status": "success", 'result': round(float(result),2)})
        else:
            return jsonify({"status": "error 1", "message": "Invalid JSON format"})
    except Exception as e:
        return jsonify({"status": "error 2", "message": str(e)})


if __name__ == '__main__':  
    app.run(debug=True)
