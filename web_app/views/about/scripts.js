async function getInfo(rx_json_file) {
    let file_object = await fetch(rx_json_file)
    console.log(file_object)
    let text_info = await file_object.text()
    console.log(text_info)
    let text_json = JSON.parse(text_info)
    console.log(text_json)
    document.getElementById("rx_name").innerHTML = text_json["name"]
    document.getElementById("rx_email").innerHTML = text_json["email"]
}

getInfo('/about/data.json')