from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
import asyncio
import argparse
from aiortc import RTCPeerConnection, RTCIceCandidate, RTCSessionDescription


async def run_webrtc_agent(pc, signaling):
    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s", pc.connectionState)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state:", pc.iceConnectionState)

    await signaling.connect()
    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            if obj.type == "offer":
                print("Received offer.")
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raspberry Pi camera streamer")
    add_signaling_arguments(parser)
    args = parser.parse_args()

    pc = RTCPeerConnection()
    signaling = create_signaling(args)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run_webrtc_agent(pc, signaling))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
        loop.close()