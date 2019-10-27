let update_view = function(api_key)
{
    //api/latest/<api_key>/<data_topic>
    $.get(`http://127.0.0.1:8000/api/latest/${api_key}/temperature`, function(data_temperature){
        if(data_temperature['response']['status']['code'] === 0 && data_temperature['response']['contents']['data_topic'] === "temperature")
        {
            document.getElementById("temperature").textContent = "Temperature: " + data_temperature['response']['contents']['value']
        }
    });
    $.get(`http://127.0.0.1:8000/api/latest/${api_key}/insolation`, function(data_insolation) {
        if(data_insolation['response']['status']['code'] === 0 && data_insolation['response']['contents']['data_topic'] === "insolation")
        {
            document.getElementById("insolation").textContent = "Insolation: " + data_insolation['response']['contents']['value']
        }
    });
};
document.addEventListener("DOMContentLoaded", function () {
    let hidden_api_key_value = document.getElementById("api_key").value;
    setInterval(function () {
        update_view(hidden_api_key_value);
    }, 10000);
}, false);