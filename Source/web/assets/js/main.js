let model = 'LR'
let model_type = 'outliers'

let data = {
  amenities : '',
  bathrooms : '1',
  bedrooms: '1',
  square_feet : '50',
  cityname: '',
  state: '',
  latitude: 40.676751931350395, 
  longitude: -99.75224599607984
}
let model_list = [
  'CB',
  'DT',
  'KNN',
  'Lasso',
  'LR',
  'MLP',
  'NN_L',
  'NN_M',
  'NN_S',
  'NN_XL',
  'NN_XL_nor',
  'RF',
  'Ridge',
  'XGB',
]

function send_forcast_request(data){
  // console.log(data, model, model_type)
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
      // Các header khác nếu cần thiết
    },
    body: JSON.stringify({'model': model, 'model_type':model_type, 'data':data})
  };

  fetch('http://localhost:5000/forcast_price', requestOptions)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    // Xử lý dữ liệu trả về từ server nếu cần
    console.log(data);
    const span = document.querySelector('#price-in-map');
    
    if (data['status'] == 'success'){ 
      result = data['result']
      if (result !== '' ){
        span.innerHTML = 'Price: <strong>' + result + '$</strong>'
      }
      const price_display_box = document.querySelector('.forcasted-price');
      price_display_box.innerHTML = '' + result + '$'
    }
  })
  .catch(error => {
    console.error('Error during fetch operation:', error);
  });
}

const select = document.querySelector('#select-model');
select.innerHTML = ''
model_list.forEach(item => {
  select.innerHTML += '<option value="'+item+'">'+item+'</option>'
});
// Get Data From Form
// Get Bedroom
let selectBedroom = document.getElementById('select-bedroom')
selectBedroom.onchange = (e) => {
  data.bedrooms = e.target.value

  // console.log(data)
  send_forcast_request(data)
}

// Get Bathroom
let selectBathroom = document.getElementById('select-bathroom')
selectBathroom.onchange = (e) => {
  data.bathrooms = e.target.value

  console.log(data)
  send_forcast_request(data)

}
// Get square_feet
// const rangeSlider = document.querySelector('.input__range');
// const rangeValue = document.getElementById('input-range');
// rangeSlider.addEventListener('input', function() {
//   rangeValue.textContent = rangeSlider.value;
//   data.square_feet = rangeValue.innerText

//   // console.log(data)
//   send_forcast_request(data)
// });

// const inputRange = document.querySelector('.input__range');
// inputRange.onchange = (e) => {
//   if(e.target.value < 5 || e.target.value > 50000){
//     alert("Please enter square feet again.")
//     inputRange.value = 50
//   }
//   else{
//     data.square_feet = e.target.value
//     // console.log("Square feet", data.square_feet)
//     send_forcast_request(data)
//   }
// }


// Get Fee
// let inputFee = document.getElementById("input__fee");
// inputFee.onchange = (e) => {
//   if(inputFee.checked){
//     data.fee = true
//   }
//   else{
//     data.fee = false
//   }

//   // console.log(data)
//   send_forcast_request(data)
// }

// Get Category
// let selectCategory = document.getElementById('select-category')
// selectCategory.onchange = (e) => {
//   data.category = e.target.value

//   // console.log(data)
//   send_forcast_request(data)
// }
// Get Model Type
let selectModelType = document.getElementById('select-model-type')
selectModelType.onchange = (e) => {
  model_type = e.target.value

  // console.log(model_type)
  send_forcast_request(data)
}

// Get Model
let selectModel = document.getElementById('select-model')
selectModel.onchange = (e) => {
  model = e.target.value

  // console.log(model)
  send_forcast_request(data)
}

// Get Amenities
let formAmenities = document.getElementById("form__amenities")
formAmenities.addEventListener('submit', function(e) {
    e.preventDefault()
    const formDataAmenities = new FormData(this);
    let arrayAmenities = formDataAmenities.getAll("amenities");
    stringAmenities = arrayAmenities.join(', ');
    data.amenities = stringAmenities

    // console.log(data)
    send_forcast_request(data)

    const ul = document.querySelector('.amenities-list');
    ul.innerHTML = ''
    arrayAmenities.forEach(item => {
      const li = document.createElement('li');
      li.classList.add('amenities-item');
      li.textContent = item;
      ul.appendChild(li);
    });
 }
)

// Get Pet
// let formPet = document.getElementById("form__pet")
// formPet.addEventListener('submit', function(e) {
//     e.preventDefault()
//     const formDataPet = new FormData(this);
//     let arrayPet = formDataPet.getAll("pet");
//     stringPet = arrayPet.join(',');
//     data.pets_allowed = stringPet

//     // console.log(data)
//     send_forcast_request(data)

//     const ul = document.querySelector('.pet-list');
//     ul.innerHTML = ''
//     arrayPet.forEach(item => {
//       const li = document.createElement('li');
//       li.classList.add('amenities-item');
//       li.textContent = item;
//       ul.appendChild(li);
//     });
//  }
// )
// nhập trên bản đồ
function initMap() {
  const myLatlng = { lat: 40.676751931350395, lng: -99.75224599607984  };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: myLatlng,
  });
  // Create the initial InfoWindow.
  let infoWindow = new google.maps.InfoWindow({
    content: "Click the map to get Lat/Lng!",
    position: myLatlng,
  });

  infoWindow.open(map);
  // Configure the click listener.
  map.addListener("click", (mapsMouseEvent) => {
    // Close the current InfoWindow.
    infoWindow.close();
    // Create a new InfoWindow.
    infoWindow = new google.maps.InfoWindow({
      position: mapsMouseEvent.latLng,
    });
    // get city and state
    let lat = mapsMouseEvent.latLng.toJSON()['lat']
    let lng = mapsMouseEvent.latLng.toJSON()['lng']
    data.latitude = lat
    data.longitude = lng
    let content = '<div>Lat: '+lat+'</div>' + 
                  '<div>Lon: '+lng+'</div>'
    let url = 'http://localhost:5000/nearest_city?latitude='+lat+'&longitude='+lng
    fetch(url)
        .then(response => response.json())
        .then(res_data => {

            data.cityname = res_data['city']
            data.state = res_data['state']  
            content += "<span id='price-in-map'></span>"+'<div>City: '+res_data['city']+'</div>' +
                      '<div>State: '+res_data['state']+'</div>'
            
            console.log(data);
            send_forcast_request(data)
            infoWindow.setContent(content);
        })
        .catch(error => console.error('Error:', error));
    
    infoWindow.setContent(content);
    infoWindow.open(map);
  });
}

window.initMap = initMap;