
function start() {
  var pc = null;
  let frameRate = 1;
  try{
    frameRate = document.getElementById("framerate").value;
  }catch{}
  var config = {
    sdpSemantics: "unified-plan",
  };

  config.iceServers = [
    {
      urls: ["stun:stun1.1.google.com:19302", "stun:stun2.1.google.com:19302"],
    },
  ];

   pc = new RTCPeerConnection(config);
  pc.addEventListener("track", function(evt) {
    console.log("recieved stream");
    console.log(pc.connectionState);
    try{
      document.getElementById("video").srcObject = evt.streams[0];

    }catch(e){
      print(e)
    }
  });

  const transciever = pc.addTransceiver("video", { direction: "recvonly" });
  transciever.direction = "recvonly";
  const dc = pc.createDataChannel("chat");
  dc.onclose = function() {
    console.log("dc closed");
  };

  dc.onopen = function() {};

  dc.onmessage = function(evt) {
    console.log(evt.data);
  };
  
  console.log("negotiate");
  pc
    .createOffer()
    .then(function(offer) {
      return pc.setLocalDescription(offer);
    })
    .then(function() {
      // wait for ICE gathering to complete
      return new Promise(function(resolve) {
        if (pc.iceGatheringState === "complete") {
          resolve();
        } else {
          function checkState() {
            if (pc.iceGatheringState === "complete") {
              pc.removeEventListener("icegatheringstatechange", checkState);
              resolve();
            }
          }
          pc.addEventListener("icegatheringstatechange", checkState);
        }
      });
    })
    .then(function() {
      var offer = pc.localDescription;
      console.log(
        "offer generated: " + JSON.stringify(offer).substring(0, 15) + "..."
      );
      console.log("offer");
      console.log(frameRate);

      return fetch("/p2sOffer", {
        body: JSON.stringify({
          username: "amitpatange",
          password: "password",
          offer: {
            type: offer.type,
            sdp: offer.sdp,
            framerate: frameRate,
          },
        }),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        method: "POST",
      }).catch((e) => console.log(e));
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(answer) {
      console.log(
        "answer recieved: " + JSON.stringify(answer).substring(0, 15) + "..."
      );
      return pc.setRemoteDescription(answer);
    })
    .catch(function(e) {
      alert(e);
    });
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  }
