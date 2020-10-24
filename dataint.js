var localData = document.getElementById("localdata")
var increase = document.getElementById("increase")
var decrease = document.getElementById("decrease")
increase.addEventListener("click", () => {
    localData.innerText = parseInt(localData.innerText) + 1
    let incReq = new XMLHttpRequest()
    inqReq.addEventListener("load", () => {
        console.log("Successfully(?) increased data.")
    })
    incReq.open("GET", "http://raspberrypi.local:8080/api/v1/data/increase")
    incReq.send()
})
decrease.addEventListener("click", () => {
    localData.innerText = parseInt(localData.innerText) - 1
    let decReq = new XMLHttpRequest()
    decReq.addEventListener("load", () => {
        console.log("Successfully(?) decreased data.")
    })
    decReq.open("GET", "http://raspberrypi.local:8080/api/v1/data/decrease")
    decReq.send()
})