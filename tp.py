import time
from freewili import FreeWili
from gtts import gTTS
import pygame
import os
from red import *

# --- This is the gTTS + pygame part ---
def say_hello_on_computer():
    """Creates an MP3 of 'Hello' and plays it using pygame."""
    text = "Hello"
    audio_file = "hello.mp3"
    
    try:
        # Create the MP3 file using Google's API
        print("Creating audio file...")
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        
        # Play the MP3 file using pygame's mixer
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error during audio playback: {e}")
    finally:
        # Clean up the created file
        if os.path.exists(audio_file):
            # A small delay before removing can prevent "file in use" errors
            pygame.mixer.music.unload() 
            os.remove(audio_file)

to_phone_number = "REGISTERED_TWILIO_NUMBER"
count_red = 0
# --- This is the FreeWili part with your requested logic ---
try:
    # Initialize the pygame mixer
    pygame.init()
    pygame.mixer.init()
    
    with FreeWili.find_first().expect("Failed to find a FreeWili device") as fw:
        print(f"✅ Successfully connected to {fw}")

        red_button_was_pressed = False

        while True:
            try:
                # This function checks for new events and triggers the callback if any are found.
                # It's non-blocking, so we add a small sleep to prevent high CPU usage.
                fw.enable_radio_events(True).expect("Failed to enable radio events")
                fw.process_events()
                time.sleep(0.05) # Poll for events 20 times per second.
            
            except KeyboardInterrupt:
                # This code runs when you press Ctrl+C.
                print("\n🛑 Keyboard interrupt received. Shutting down gracefully...")
                break
        
            
            # Read the state of all buttons from the device.
            buttons = fw.read_all_buttons().expect("Failed to read buttons")
            
            # Loop through the dictionary of buttons returned by the device.
            for button_color, button_state in buttons.items():
                # Check if the current button in the loop is the red one.
                if button_color.name.lower() == "red":
                    # Determine if the button is currently pressed.
                    is_red_pressed_now = (button_state == 1)
                    
                    # Trigger only if it's pressed NOW and was NOT pressed before.
                    if is_red_pressed_now and not red_button_was_pressed:
                        count_red += 1
                        if count_red % 3 == 0:
                            make_call(to_phone_number)

                    # Update the state for the next loop cycle.
                    red_button_was_pressed = is_red_pressed_now

                elif button_color.name.lower() == "blue":
                    # Determine if the button is currently pressed.
                    is_red_pressed_now = (button_state == 1)
                    
                    # Trigger only if it's pressed NOW and was NOT pressed before.
                    if is_red_pressed_now and not red_button_was_pressed:
                        print("Button Pressed! Saying 'Hello' on the computer...")
                        
                        # ✅ ACTION: Call the function to use gTTS and pygame
                        say_hello_on_computer()

                    # Update the state for the next loop cycle.
                    red_button_was_pressed = is_red_pressed_now
                
                elif button_color.name.lower() == "green":
                    # Determine if the button is currently pressed.
                    is_red_pressed_now = (button_state == 1)
                    
                    # Trigger only if it's pressed NOW and was NOT pressed before.
                    if is_red_pressed_now and not red_button_was_pressed:
                        print("Button Pressed! Saying 'Hello' on the computer...")
                        
                        # ✅ ACTION: Call the function to use gTTS and pygame
                        say_hello_on_computer()

                    # Update the state for the next loop cycle.
                    red_button_was_pressed = is_red_pressed_now

                elif button_color.name.lower() == "yellow":
                    # Determine if the button is currently pressed.
                    is_red_pressed_now = (button_state == 1)
                    
                    # Trigger only if it's pressed NOW and was NOT pressed before.
                    if is_red_pressed_now and not red_button_was_pressed:
                        print("Button Pressed! Saying 'Hello' on the computer...")
                        
                        # ✅ ACTION: Call the function to use gTTS and pygame
                        say_hello_on_computer()

                    # Update the state for the next loop cycle.
                    red_button_was_pressed = is_red_pressed_now

                elif button_color.name.lower() == "white":
                    # Determine if the button is currently pressed.
                    is_red_pressed_now = (button_state == 1)
                    
                    # Trigger only if it's pressed NOW and was NOT pressed before.
                    if is_red_pressed_now and not red_button_was_pressed:
                        roku_keyhome = bytes([0xBE, 0xEF, 00, 0xFF])
                        print("Sending Roku Key Home IR command:", roku_keyhome)
                        fw.send_ir(roku_keyhome).expect("Failed to send IR command")
                        print("Done.")

                    # Update the state for the next loop cycle.
                    red_button_was_pressed = is_red_pressed_now

                else:
                    continue
            
            # A small delay to keep the script efficient.
            time.sleep(0.05)
            # 4. Disable IR events before closing the connection.
        print("🔌 Disabling IR event listener...")
        fw.enable_ir_events(False).expect("❌ ERROR: Failed to disable IR events.")

except (KeyboardInterrupt, SystemExit):
    print("\nExiting program.")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")
finally:
    # Cleanly exit pygame when the program ends

    pygame.quit()
