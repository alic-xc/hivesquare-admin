
function showNotification(action){
        // create a new notification
    const imgSrc = $('#primaryImage').attr('src')
    var msg;
    if(action === 'show'){
        msg = "A delivery has been placed on queue"
    }else{
        msg = "An action have been performed on a queue delivery"
    }

    const notification = new Notification('Queue Notification', {
        body: msg,
        icon: imgSrc,
        vibrate: [200, 100, 200]

    });

    // close the notification after 10 seconds
    setTimeout(() => {
        notification.close();
    }, 100 * 1000);

    // navigate to a URL when clicked
    notification.addEventListener('click', () => {
    });
}

function idleLogout(url) {
        var t;
        var allow_passage = false
        window.onload = resetTimer;
        window.onmousemove = resetTimer;
        window.onmousedown = resetTimer;  // catches touchscreen presses as well
        window.ontouchstart = resetTimer; // catches touchscreen swipes as well
        window.onclick = resetTimer;      // catches touchpad clicks as well
        window.onkeypress = resetTimer;
        window.addEventListener('scroll', resetTimer, true); // improved; see comments

        function inactivity() {
            let timerInterval
            Swal.fire({
              title: 'Inactivity',
              icon: 'warning',
              html: '<br/><b></b> seconds before logging you out.',
              timer: 120000,
              timerProgressBar: true,
              onBeforeOpen: () => {
                Swal.showLoading()
                timerInterval = setInterval(() => {
                  const content = Swal.getContent()
                  if (content) {
                    const b = content.querySelector('b')
                    if (b) {
                      b.textContent = Math.floor(parseInt(Swal.getTimerLeft())/ 1000)

                    }
                  }
                }, 1000)
              },
              onClose: () => {
                clearInterval(timerInterval)
                if(Swal.stopTimer() < 1){
                    window.location = url
                }
              }
            }).then((result) => {
              /* Read more about handling dismissals below */
              if (result.dismiss === Swal.DismissReason.timer) {
                console.log('I was closed by the timer')
              }
            })
        }

        function resetTimer() {
            if(allow_passage == false) {
                clearTimeout(t);
                Swal.close()
                t = setTimeout(inactivity, 6000000);  // time is in milliseconds
            }
        }
        $(document).on('click', '#confirm-delete', function (e) {
    e.preventDefault()
    allow_passage = true
    const data = $(this).data()
    const msgText = msg(data['type'], data['driver'], data['vehicle'] )
    swal({
        title: 'Are you sure?',
        text: msgText,
        icon: 'warning',
        buttons: true,
        dangerMode: true,
    }).then( willDelete => {
        if (willDelete) {
            window.location = data.href
        }else{
            allow_passage = false
        }
    });
});

        $(document).on('click', '#confirm-approve', function (e) {
            e.preventDefault()
            allow_passage = true
            const data = $(this).data()
            const msgText = approveText(data['type'])
            swal({
                title: 'Are you sure?',
                text: msgText,
                icon: 'warning',
                buttons: true,
                dangerMode: true,
            }).then( willDelete => {
                if (willDelete) {
                    window.location = data.href
                }else{
                    allow_passage = false
                }
            });
        });

        $(document).on('click', '.actionConfirmation', function (e) {
            e.preventDefault()
            allow_passage = true
            const data = $(this).data()
            console.log(data)
            const msgText = text(data['actionType'], data['action'])
            swal({
                title: 'Are you sure?',
                text: msgText,
                icon: 'warning',
                buttons: true,
                dangerMode: true,
            }).then( confirm => {
                if(confirm){
                    window.location = data.href
                } else {
                    allow_passage = false
                }
            } );
        });


    }

$('#viewDocument').on('show.bs.modal', function (event) {
    const elem = $(event.relatedTarget)
    const imageURL = elem.data('href')
    var imageContainer = $('#imageContainer')
    if(imageURL){
        if(imageURL.endsWith('png') || imageURL.endsWith('jpg') || imageURL.endsWith('gif') || imageURL.endsWith('jpeg')){
            imageContainer.html('')
            imageContainer.html("<img src='" + imageURL + "' class='img-fluid' style='width:auto;height: 480px' />")
        }else{
            imageContainer.html('')
            imageContainer.html(" <h5 class='text-center my-5'>This document is not an image. Click <a href='" + imageURL+ "' target='_blank' download><i class='fa fa-download'></i></a> </h5> ")
        }
    }else{

        imageContainer.html("<span class='text-danger text-center'>No document found</span>")
    }

})

function text(actionType, action){
    const msgObj = {
        'activation':{
            'activate': "Are you sure you want to activate driver",
            'deactivate': "Are you sure you want to deactivate driver"
        },
        'requestVisibility':{
            'go_online': "Are you sure you want driver to have access to marketplace",
            'go_offline': "Are you sure you want restrict driver from marketplace",
        },
        'modifyItem':{
            'delete': "Remember this action is irreversible."
        },
        'associate':{
            'rider_detach': "Are you sure you want to detach this rider from your company",
            'vehicle_detach': "Are you sure you want to detach this vehicle from your company",
        }

    }
    return msgObj[actionType][action]
}

function approveText(type){
    if(type == "True"){
        msg = "You are about to approve this expense"
    }else{
        msg = "You are about to reject this expense"
        }
    return msg
}

function msg(type, driver='', vehicle=''){
    var test;
    if(type == true){
        text = `You are about to remove ${driver} from ${vehicle}`
    }else{
        text = 'Once deleted, you will not be able to recover this data!'
    }
    return text
}

function fileUpload(params){
    const {url, csrfToken, type, obj} = params
    obj.attr('disabled', '')
    const fieldName = obj.data()['name']
    const progressBar = $(`#${fieldName}`)
    progressBar.parent('div').removeClass('d-none')

    // initialize a form
    let form = new FormData();
    form.append('doc', obj[0].files[0])
    form.append('doc_type', fieldName)
    form.append('csrfmiddlewaretoken', csrfToken )
    form.append('url_type', type)

    $.ajax({
        xhr: function() {
            var xhr = new window.XMLHttpRequest();

            xhr.upload.addEventListener("progress", function(evt) {
              if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                percentComplete = parseInt(percentComplete * 100);

                progressBar.width(percentComplete+'%');
              }

            }, false);

            return xhr;
            },
        url: url,
        data: form,
        contentType: false,
        processData: false,
        method: 'POST',
        success: function(response){
            // Change progress bar status
            progressBar.removeClass('bg-primary')
            progressBar.addClass('bg-success')

            // Output success msg
            iziToast.success({
                    "title": "Success",
                    "message": "Document uploaded successfully.",
                    "position": "topRight"
                })
            setTimeout(() => window.location.reload(), 5000 )
            // Remove restriction, hide progress bar and change icon
            setTimeout(() => progressBar.parent('div').addClass('d-none'), 5000)
            obj.val('')
            $(`span[data-label='${fieldName}']`).html("<i class='fa fa-check-circle text-success'></i>")
            obj.removeAttr('disabled', '')
        },
        error: function(err){
            progressBar.removeClass('bg-primary')
            progressBar.addClass('bg-danger')
            setTimeout(() => progressBar.parent('div').addClass('d-none'), 5000)
            obj.removeAttr('disabled', '')
            let baseElem = '.document-upload'
            errorManager(err, baseElem)
        }
    })
}

function errorManager(err, baseElem){
            // mapping error to required field
            const response = JSON.parse(err.responseText)

            // Check response is an object
            const baseError = response['error']
            try{
                for(let key in baseError){
                    const errorSpan = document.querySelector(`${baseElem} #${key}`)
                    errorSpan.innerHTML = baseError[key]
                }
            }
            catch (e) {
                iziToast.error({
                    'title': 'Error',
                    'message': baseError['detail'] || baseError['details'] || baseError,
                    'position': 'topRight'
                })
            }

        }

function populateBank(url, selectInput){
    // Populate bank select
    $.ajax({
        url: url,
        method: 'GET',
        success: function(response){
            const results = response.results
            selectInput.html('')
            selectInput.append('<option value="">Please select</option>')
            selectInput.append(results.map( result => `<option value="${result.id}" > ${result.bank_name}</option>` ))

        },

    })
}

function dateFormatter(date) {
    const formatDate = new Date(date)
    return formatDate.toDateString()
}

function currencyFormater(amount){
    return new Intl.NumberFormat().format(amount)
}

function getPartialService(url, elem){
    $.ajax({
        url: url,
        data: $('#sorting-form').serialize(),
        method: 'GET',
        success:function(response){
            elem.find('tbody').remove()
            elem.find('tfoot').remove()
            elem.append(response)
        }
    })

    sortTable(url, elem)
    handlePagination(elem)
}

function sortTable(url, elem){
    $('#sorting-form').submit(function(e){
        e.preventDefault()
        let submitButton = $(this).find('button')
        submitButton.addClass('btn-progress')
        submitButton.addClass('disabled')
        $.ajax({
            url: url,
            data: $(this).serialize(),
            method: 'GET',
            success:function(response){
                elem.find('tbody').remove()
                elem.find('tfoot').remove()
                elem.append(response)
                submitButton.removeClass('btn-progress')
                submitButton.removeClass('disabled')
            },
            error: function(err){
                console.log(err)
                submitButton.removeClass('btn-progress')
                submitButton.removeClass('disabled')
                let baseElem = '.services'
                errorManager(err, baseElem)
            }
        })
    })
}

function loadMapLibrary(){
    // Create the script tag, set the appropriate attributes
    var script = document.createElement('script');
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAaOp7Ae5nC5_SRVIYOjZP5uC7sDfYUmWc&callback=initMap';
    script.async = true;

    // Append the 'script' element to 'head'
    document.head.appendChild(script);
}

function getDriversStatusRealtime(){
    firebaseConfig()
    const getDriversIDArr = document.querySelectorAll('.riders')
    getDriversIDArr.forEach( function(driver){
        let driverID = driver.dataset.rider
        const loc_ref= firebase.database().ref(`driversAvailable/${driverID}/l/`);
        const gotData = (data) => {
            var locations = data.val();
            try{
                const curr_lat = locations[0];
                const curr_lng = locations[1];
                console.log(curr_lat)
                driver.querySelector('.statusBox').innerHTML = "<div class=\"text-success text-small font-600-bold\"><i class=\"fa fa-circle text-success\"></i> Online</div>"
            }
            catch (e) {
                console.log("EE")
                driver.querySelector('.statusBox').innerHTML="<div class=\"text-danger text-small font-600-bold\"><i class=\"fa fa-circle text-danger\"></i> Offline</div>"
            }
        }

        function errData(err){
            console.log('error: '+ err);
        }
        loc_ref.on('value', gotData, errData);


    })
}

function realtimeMapUpdate(map, driverID, imageURL){
    /*
    Get current driver update and update the map
    */

    // Firebase configuration
    const config = {
            apiKey: "AIzaSyAaOp7Ae5nC5_SRVIYOjZP5uC7sDfYUmWc",
            authDomain: "patch-fc9dd.firebaseapp.com",
            databaseURL: "https://patch-fc9dd-default-rtdb.firebaseio.com",
            projectId: "coursera",
            storageBucket: "patch-fc9dd.appspot.com",
            messagingSenderId: "686773017591",
            appId: "1:686773017591:web:cc9ec3bf55969b73e9ecf2"
        };

    firebase.initializeApp(config);

    var markers;
    function ShowLocation(lat,lng) {
        // Update current location
        if(markers!=null){
            markers.setMap(null);
        }

        const cordinate = { lat: lat, lng: lng };

        const icon = {
            url: imageURL, // url
            scaledSize: new google.maps.Size(25, 60), // scaled size
            origin: new google.maps.Point(0,0), // origin
            anchor: new google.maps.Point(0, 0), // anchor
        };

        // Icon for representation on map.
        const marker = new google.maps.Marker({
            position: cordinate,
            map: map,
            icon: icon,
        });

        marker.icon.rotation = 135;
        map.setZoom(17);
        map.panTo(marker.position);
        markers = marker; // add marker

    }

    // get firebase database reference.
    const loc_ref= firebase.database().ref(`driversAvailable/${driverID}/l/`);
    loc_ref.on('value', gotData, errData);
    var curr_lat;
    var curr_lng;
    function gotData(data){
        var locations = data.val();
        try{
            curr_lat=locations[0];
            curr_lng=locations[1];
            $('#online-status').html("<i class=\"fa fa-circle text-success\"></i> Online")
            ShowLocation(parseFloat(curr_lat),parseFloat(curr_lng));
        }
        catch (e) {
            $('#online-status').html("<i class=\"fa fa-circle text-danger\"></i> Offline")
        }
    }

    function errData(err){
        console.log('error: '+err);
    }

}

function initMapObject(center){
    return new google.maps.Map(document.getElementById("map"), {
            center: center,
            zoom: 15,
                disableDefaultUI: false,
                zoomControl: false,
        });
}

function driverRealtimeUpdate(driverID, imageURL){
    return () => {
        map = initMapObject({ lat: 6.465422, lng: 3.406448})
        realtimeMapUpdate(map, driverID, imageURL)
    }

}

function firebaseConfig(){
    const config = {
            apiKey: "AIzaSyAaOp7Ae5nC5_SRVIYOjZP5uC7sDfYUmWc",
            authDomain: "patch-fc9dd.firebaseapp.com",
            databaseURL: "https://patch-fc9dd-default-rtdb.firebaseio.com",
            projectId: "patch-fc9dd",
            storageBucket: "patch-fc9dd.appspot.com",
            messagingSenderId: "686773017591",
            appId: "1:686773017591:web:cc9ec3bf55969b73e9ecf2"
        };

    return firebase.initializeApp(config);
}

function serviceMap(pickupLocation, destinationLocation, driverID, imageURL) {

    return () => {
        const directionsService = new google.maps.DirectionsService();
        const directionsRenderer = new google.maps.DirectionsRenderer({suppressMarkers: true});
        map = initMapObject(pickupLocation)
        const label = {text: 'P', color: 'white'}
        const label2 = {text: 'D', color: 'white'}
        directionsRenderer.setMap(map);
        var markers;
        var markersArr = []
        calculateAndDisplayRoute(directionsService, directionsRenderer, pickupLocation, destinationLocation);
        const pickUp = addMarker(label, pickupLocation, map)
        const destination = addMarker(label2, destinationLocation, map)
        markersArr.push(pickUp)
        markersArr.push(destination)
        const firebase = firebaseConfig()
        function ShowLocation(lat,lng) {
            // Update current location
            if(markers != null){
                markers.setMap(null);
            }

            const cordinate = { lat: lat, lng: lng };

            const icon = {
                url: imageURL, // url
                scaledSize: new google.maps.Size(25, 60), // scaled size
                origin: new google.maps.Point(0,0), // origin
                anchor: new google.maps.Point(0, 0), // anchor
            };

            // Icon for representation on map.
            const marker = new google.maps.Marker({
                position: cordinate,
                map: map,
                icon: icon,
            });

            marker.icon.rotation = 135;
            // map.setZoom(17);
            // map.panTo(marker.position);
            markers = marker; // add marker
            markersArr.push(marker)
        }

        // Detect rider focus click
        $('#driverFocus').click(function(){
            const dataset = $(this).attr('data-focus')
            console.log(dataset)
            if(dataset === 'false'){
                map.panTo(markersArr[markersArr.length - 1].position)
                map.setZoom(17)
                $(this).removeAttr('data-focus')
                $(this).attr('data-focus', 'true')

            }else{
                map.panTo(pickupLocation)
                map.setZoom(11)
                $(this).removeAttr('data-focus')
                $(this).attr('data-focus', 'false')
            }

        })

        // get firebase database reference.
        const locationRef= firebase.database().ref(`driversAvailable/${driverID}/l/`);
        locationRef.on('value', processData, errData);

        function processData(data){
            try{
                const coordinate = data.val()
                const currentLatitude = coordinate[0];
                const currentLongitude = coordinate[1];
                $('#online-status').html("<i class=\"fa fa-circle text-success\"></i> Online")
                ShowLocation(parseFloat(currentLatitude), parseFloat(currentLongitude));
            }
            catch (e) {
                console.log(e)
                $('#online-status').html("<i class=\"fa fa-circle text-danger\"></i> Offline")
            }
        }

        function errData(err){
            console.log('error: '+err);
        }



    }
}

function addMarker(label, position, map){
    return new google.maps.Marker({
                position: position,
                label: label,
                map,
              });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, pickup, destination) {

      directionsService.route(
        {
          origin: pickup,
          destination: destination,
          waypoints: [],
          optimizeWaypoints: true,
          travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status === "OK" && response) {
                directionsRenderer.setDirections(response);
                directionsRenderer.setMarker({})
            }
        }
      );
}

function getServiceDetail(url, elem, imageURL) {
    $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
            // populate the vehicle elements
            const order = response.result
            elem.find('#category').html(order.service_category.name)
            elem.find('#description').html(order.description)
            elem.find('#date').html( dateFormatter(order.created_date))
            elem.find('#rating').html((order.rating.rating)?order.rating.rating:'N/A')
            elem.find('#amount').html("&#x20A6;"+currencyFormater(order.item_value))
            elem.find('#payment').html(order.pay_mode)
            elem.find('#startTime').html((order.start_time)?dateFormatter(order.start_time):'N/A')
            elem.find('#endTime').html((order.start_time)?dateFormatter(order.end_time):'N/A')
            elem.find('#estimatedCost').html("&#x20A6;" +currencyFormater(order.estimated_cost))
            elem.find('#pickup').html(order.pick_up_address)
            elem.find('#destination').html(order.destination_address)
            elem.find('#estDistance').html(order.estimated_distance)
            elem.find('#estTime').html(order.estimated_time)
            elem.find('#name').html(order.user.name)
            elem.find('#phone').html(order.user.phone)
            elem.find('#contactName').html(order.contact.recipient_name)
            elem.find('#contactPhone').html(order.contact.recipient_phone)
            elem.find('#riderName').html(order.rider.name)
            elem.find('#riderPhone').html(order.rider.phone)
            elem.find('#vehicleName').html(order.rider.vehicle.name)
            elem.find('#vehicleReg').html(order.rider.vehicle.reg)
            const pickupPoint = {lat: parseFloat(order.pick_up_latitude) , lng: parseFloat(order.pick_up_longitude) }
            const destinationPoint = {lat: parseFloat(order.destination_latitude), lng: parseFloat(order.destination_longitude) }

            // Check order status before showing rider's location
            let driverID = null
            if(order.status != 'pending' || order.status != 'completed'){
                driverID = order.rider.user_id
            }

             var span;
             if(order.status === 'pending'){
                 span = '<span class="badge badge-outline col-grey">'
             }else if(order.status === 'accepted'){
                 span = '<span class="badge badge-outline col-blue">'
             }else if(order.status === 'arrived'){
                 span = '<span class="badge badge-outline blue">'
             }else if(order.status === 'in-transit'){
                 span = '<span class="badge badge-outline col-blue-grey">'
             }else if(order.status === 'returning'){
                 const span = '<span class="badge badge-outline cyan">'
             }else if(order.status === 'completed'){
                 span = '<span class="badge badge-outline green">'
             }else{
                 span = '<span class="badge badge-outline col-red">'
             }

             const spanEndElem = '</span>'

            elem.find('#status').html(`${span}${order.status}${spanEndElem}`)

            //Verification & pickup code
            const pickupCodeElem = $('#pickupCode')
            const completionCodeElem = $('#completionCode')
            pickupCodeElem.html(order.verification_code)
            completionCodeElem.html(order.completion_code)

            window.initMap = serviceMap(pickupPoint, destinationPoint, driverID, imageURL)
            loadMapLibrary()
        }
    })
}

function dashboardWidgetsGraph(url){

    let submitButton = $('#dataSort').find('button')
        submitButton.addClass('btn-progress')
        submitButton.addClass('disabled')


    $.ajax({
        url: url,
        method: 'GET',
        success:function(response){
            submitButton.removeClass('btn-progress')
            submitButton.removeClass('disabled')
            const results = response.results
            const graph = response.graph_data
            const revenueAmount = (results.revenue.amount)?results.revenue.amount:0
            $('#revenue').html(currencyFormater(revenueAmount))
            $('#deliveryCount').html(results.delivery_count)
            $('#totalDeliveryCount').html(results.total_delivery_count)
            $('#riders').html(results.rider_count)
            $('#debt').html(currencyFormater(results.debt))
            $('#earnings').html(currencyFormater(results.pending_earnings))
            $('.completed').html(results.delivery_count.completed_deliveries)
            $('.total').html(results.delivery_count.total_deliveries)
            $('.cancelled').html(results.delivery_count.cancelled_deliveries)

            // document.querySelector("#revenue-chart").innerHTML = ''
            if(graph){
            var options = {
                colors: [
                    '#54ca68'
                ],
                  series: [{
                  name: 'revenue',
                  data: graph.revenue
                }],
                  chart: {
                  height: 350,
                  type: 'area'
                },
                dataLabels: {
                  enabled: false,
                },
                stroke: {
                  curve: 'smooth'
                },
                xaxis: {
                  type: 'datetime',
                  categories: graph.dates
                },
                tooltip: {
                  x: {
                    format: 'dd/MM/yy HH:mm'
                  },
                },
                };

                var chart = new ApexCharts(document.querySelector("#revenue-chart"), options);
                chart.render();
                }

        },
        error: function(err){
            submitButton.removeClass('btn-progress')
            submitButton.removeClass('disabled')
        }
    })
}

function getLastDay(year,month) {
    return  new Date(year, month, 0).getDate();
}

function datePickerInit(){
     const today = new Date()
     const year = today.getFullYear()
     const month = String(today.getMonth() + 1).padStart(2, '0');
     const endingMonthDay = `${year}-${month}-${getLastDay(year, month)}`
     const startingMonth = `${year}-${month}-01`
     const endingMonth = `${endingMonthDay}`

     $('#from_date').val(startingMonth)
     $('#to_date').val(endingMonth)
}
