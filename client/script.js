SERVER_URL = "http://127.0.0.1:5000"
alert('loaded')
function handleLogin(response){
    localStorage.setItem("token", response.credential);
    console.log(response);
}

function onLinkAdsAccount(){
    token = localStorage.getItem("token");
    window.location.href = `${SERVER_URL}/authorize?token=${token}`;
}