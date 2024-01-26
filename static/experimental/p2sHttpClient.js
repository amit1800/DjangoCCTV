var pc = null;
function createPeerConnection() {
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
    document.getElementById("video").srcObject = evt.streams[0];
  });

  return pc;
}

function negotiate() {
  console.log("negotiate");
  return pc
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
}

let frameRate = 1;
function start() {
  frameRate = document.getElementById("framerate").value;
  pc = createPeerConnection();
  transciever = pc.addTransceiver("video", { direction: "recvonly" });
  transciever.direction = "recvonly";
  dc = pc.createDataChannel("chat");
  dc.onclose = function() {
    console.log("dc closed");
  };

  dc.onopen = function() {};

  dc.onmessage = function(evt) {
    console.log(evt.data);
  };

  // navigator.mediaDevices
  //   .getUserMedia({
  //     video: { width: 320, height: 240, frameRate: { max: 30 } },
  //     audio: false,
  //   })
  //   .then(
  //     function(stream) {
  //       stream.getTracks().forEach(function(track) {
  //         pc.addTrack(track, stream);
  //       });
  //       return negotiate();
  //     },
  //     function(err) {
  //       alert("Could not acquire media: " + err);
  //     }
  //   );
  negotiate();
}
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
const csrftoken = getCookie("csrftoken");
