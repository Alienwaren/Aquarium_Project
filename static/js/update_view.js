var update_view = function(api_key, temperature_graph, insolation_graph)
{
    //api/latest/<api_key>/<data_topic>
    $.get(`http://127.0.0.1:8000/api/latest/${api_key}/temperature`, function(data_temperature){
        if(data_temperature['response']['status']['code'] === 0 && data_temperature['response']['contents']['data_topic'] === "temperature")
        {
            let temperature_value = data_temperature['response']['contents']['value'];
            document.getElementById("temperature").textContent = "Temperature: " + temperature_value;
            temperature_graph.data.datasets[0].data.push(temperature_value);
            temperature_graph.update();
        }
    });
    $.get(`http://127.0.0.1:8000/api/latest/${api_key}/insolation`, function(data_insolation) {
        if(data_insolation['response']['status']['code'] === 0 && data_insolation['response']['contents']['data_topic'] === "insolation")
        {
            let insolation_value = data_insolation['response']['contents']['value'];
            document.getElementById("insolation").textContent = "Insolation: " + insolation_value;
            insolation_graph.data.datasets[0].data.push(insolation_value);
            insolation_graph.update();
        }
    });
};


document.addEventListener("DOMContentLoaded", function () {
    let hidden_api_key_value = document.getElementById("api_key").value;
    let temperature_ctx = document.getElementById("temperature_graph").getContext('2d');
    let temperature_graph = new Chart(temperature_ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            datasets: [{
                label: 'Temperature',
                borderColor: 'rgb(15,0,255)',
                data: []
            }]
        },

        // Configuration options go here
        options: {}
    });

    let insolation_ctx = document.getElementById("insolation_graph").getContext('2d');
    let insolation_graph = new Chart(insolation_ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            datasets: [{
                label: 'Insolation',
                borderColor: 'rgb(255,147,0)',
                data: []
            }]
        },

        // Configuration options go here
        options: {}
    });
    setInterval(function () {
        update_view(hidden_api_key_value, temperature_graph, insolation_graph);
    }, 10000);
}, false);