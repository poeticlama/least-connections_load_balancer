const url = "127.0.0.1:8000"

document.getElementById("main-button").addEventListener("click", async () => {
    // Actions after clicking a button

    // Randomly choosing a number of picture
    const image_num = Math.ceil(Math.random() * 4)

    // Changing text in image space
    document.querySelector('.picture').children[0].innerHTML = 'Waiting for server response...'

    // Sending a request to balancer
    const response = await fetch(new Request(url, {
        method: "GET",
        headers: {
            "Image Number": image_num,
        }
    }))

})