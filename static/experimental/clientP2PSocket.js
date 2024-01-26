console.log(Math.random());
createButton = document.createElement("button");
createButton.textContent = "Start";
streamButton = document.createElement("button");
streamButton.textContent = "Stream";

video = document.getElementById("video");
let url = "ws://" + window.location.host + "/ws/socket-server/";
const io = new WebSocket(url);
// io.onmessage = function(e) {
//   console.log("Data:", e.data);
// };
pc = new RTCPeerConnection();

pc.onnegotiationneeded = async () => {
  console.log("need");
  await pc.setLocalDescription(await pc.createOffer());
  data = { description: pc.localDescription };
  io.send(JSON.stringify(data));
  console.log(data);
};
pc.onicecandidate = ({ candidate }) => {
  data = { candidate };
  io.send(JSON.stringify(data));
  console.log(data);
};
pc.ondatachannel = (e) => {
  dc = e.channel;
  dc.onopen = (evt) => console.log("dc started");
  dc.onclose = (evt) => console.log("dc closed");
  dc.onmessage = (evt) => console.log("message: " + evt.data);
};

io.onmessage = async (e) => {
  data = JSON.parse(e.data);
  console.log(data);
  if (data.description) {
    await pc.setRemoteDescription(data.description);
    if (data.description.type == "offer") {
      await pc.setLocalDescription(await pc.createAnswer());
      data = { description: pc.localDescription };
      io.send(JSON.stringify(data));
      console.log(data);
    }
  } else if (data.candidate) await pc.addIceCandidate(data.candidate);
};

createButton.addEventListener("click", () => {
  dc = pc.createDataChannel("channel");
  dc.onopen = (evt) => console.log("dc started");
  dc.onclose = (evt) => console.log("dc closed");
  dc.onmessage = (evt) => console.log("message: " + evt.data);
});
pc.ontrack = (e) => {
  video.srcObject = e.streams[0];
};
streamButton.addEventListener("click", async () => {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
  });
  for (const track of stream.getTracks()) {
    pc.addTrack(track, stream);
  }
});

document.body.appendChild(createButton);
document.body.appendChild(streamButton);
