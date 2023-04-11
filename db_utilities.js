var ydb_url = 'https://functions.yandexcloud.net/d4e1kh1fs1avg1jd64mb'

function update_car_list(data)
{
    $("#database td").parent().remove();
    let received_cars = JSON.parse(preconvert_json(data));
    for(let i = 0; i < received_cars.length; ++i) {
        let car = new Automobile(received_cars[i]);
        $('#database tr:last').after(car.to_table_entry());
    }
    $("#database").show();
}

function update_model_list(data)
{
    $('#models')
        .find('option')
        .remove()
        .end()
        .append('<option value="whatever">Select model</option>')
        .val('blank')
    ;

    let received_models = JSON.parse(preconvert_json(data));
    for(let i = 0; i < received_models.length; ++i) {
        console.log(received_models[i]);
        let model = received_models[i].model;
        $('#models').append($('<option>', {
            value: model,
            text: model
        }));
    }
}