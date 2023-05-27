import asyncio

import edge_tts

TEXT = "Hello World!"
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "output/tmp.wav"


async def tts_main(TEXT):
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save("E:/SadTalker/output/tmp.mp3")
    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(tts_main())
    finally:
        loop.close()