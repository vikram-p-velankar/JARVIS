from freewili import FreeWili
from freewili.framing import ResponseFrame
from freewili.types import EventDataType, EventType, IRData


def event_callback(event_type: EventType, response_frame: ResponseFrame, event_data: EventDataType) -> None:
    """Callback function to handle events from FreeWili."""
    if isinstance(event_data, IRData):
        print(f"HEYY HOW ARE YOU")
        user_input = "350 1 20"
        frequency_hz, duration_sec, amplitude = map(float, user_input.split())
        frequency_hz = int(frequency_hz)  # Convert to int for frequency
        # v54 firmware: Response frame always returns failure
        fw.play_audio_tone(frequency_hz, duration_sec, amplitude)  # .expect("Failed to play audio tone")


with FreeWili.find_first().expect("Failed to find FreeWili") as fw:
    fw.set_event_callback(event_callback)
    print("Enabling IR events")
    fw.enable_ir_events(True).expect("Failed to enable IR events")
    print("Waiting for IR events... Press Ctrl+C to exit.")
    while True:
        try:
            fw.process_events()
        except KeyboardInterrupt:
            print("Exiting IR event loop")
            break
    fw.enable_ir_events(False).expect("Failed to disable IR events")
print("Done.")