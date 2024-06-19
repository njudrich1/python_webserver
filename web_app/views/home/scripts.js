async function getInfo(rx_json_file) {
    let file_object = await fetch(rx_json_file)
    console.log(file_object)
    let text_info = await file_object.text()
    console.log(text_info)
    document.getElementById("test").innerHTML = text_info
}

getInfo('/home/data.json')