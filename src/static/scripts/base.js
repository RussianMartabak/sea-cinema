const homeButton = document.querySelector("#home")

homeButton.addEventListener('click', goHome)

function goHome() {
    window.open("/", "_self")
}