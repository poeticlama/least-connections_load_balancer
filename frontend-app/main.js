const url = "http://127.0.0.1:8000/images/2"

document.getElementById("main-button").addEventListener("click", async () => {
    // Actions after clicking a button

    // Randomly choosing a number of picture
    const image_num = Math.ceil(Math.random() * 4)

    // Changing text in image space
    let container = document.querySelector('.picture')
    container.children[0].innerHTML = 'Waiting for server response...'

    // Sending a request to balancer
    const response = await fetch(url)
    if (response.status === 200) {
        // Getting an image
        const imageBlob = await response.blob()
        const imageObjectURL = URL.createObjectURL(imageBlob);

        const image = document.createElement('img')
        image.src = imageObjectURL

        // Appending an image to container
        container.removeChild(container.children[0])
        container.appendChild(image)
    } else {
        console.log("HTTP-Error: " + response.status)
        container.children[0].innerHTML = 'Error occurred, try again'
    }
})