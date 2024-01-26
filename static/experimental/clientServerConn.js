console.log(Math.random());
createButton = document.createElement("button");
createButton.textContent = "Start";
video = document.getElementById("video");
let url = "ws://" + window.location.host + "/ws/server-to-peer/";
const io = new WebSocket(url);
pc = new RTCPeerConnection();
// navigator.mediaDevices
//   .getUserMedia({ video: true, audio: true })
//   .then((stream) =>
//     stream.getTracks().forEach((track) => pc.addTrack(track, stream))
//   );
pc.onnegotiationneeded = async () => {
  console.log("negotiation");
  await pc.setLocalDescription(await pc.createOffer());
};

pc.ontrack = (e) => {
  video.srcObject = e.streams[0];
};
pc.onicecandidate = (e) => {
  console.log("candidate");
  if (!e.candidate) {
    console.log("final candidate");
    data = { finalDes: pc.localDescription };
    console.log(data);
    io.send(JSON.stringify(data));
  }
};

io.onmessage = async (e) => {
  data = JSON.parse(e.data);
  console.log(data);
  if (data.description) {
    await pc.setRemoteDescription(data.description);
    console.log("local", pc.localDescription);
    console.log("remote", pc.remoteDescription);
  }
};

createButton.addEventListener("click", () => {
  dc = pc.createDataChannel("channel");
  dc.onopen = (evt) => console.log("dc started");
  dc.onclose = (evt) => console.log("dc closed");
  dc.onmessage = (evt) => console.log(evt.data);
});

document.body.appendChild(createButton);
