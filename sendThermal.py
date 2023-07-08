import time
import websocket
import numpy as np
import board
import busio
import adafruit_mlx90640

# Function to send IR data through WebSocket
def send_ir_data(ws, ir_data):
    data_str = ' '.join(map(str, ir_data))
    ws.send(data_str)

# Setup MLX90640
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
mlx_shape = (24, 32)
frame = np.zeros((24 * 32,))

# Create a function to establish a WebSocket connection
def connect_websocket():
    return websocket.create_connection("ws://10.0.0.55:8083/MyWebSocketServer")

# Main loop
while True:
    try:
        # Connect to WebSocket server
        ws = connect_websocket()

        while True:
            # Grab frame from MLX90640
            mlx.getFrame(frame)
            data_array = np.reshape(frame, mlx_shape)

            # Send IR data
            try:
                send_ir_data(ws, data_array.flatten())
            except websocket._exceptions.WebSocketConnectionClosedException:
                # Handle connection closed exception here, reconnect by breaking the inner loop
                print("WebSocket connection closed. Reconnecting...")
                break
            except Exception as e:
                # Generic error handler for unexpected errors
                print(f"Unexpected error: {e}")
                break

            time.sleep(0.1)  # Adjust sleep time as needed

    except Exception as e:
        print(f"Error establishing WebSocket connection: {e}")
        time.sleep(5)  # Sleep before retrying connection

    finally:
        # Close WebSocket connection
        try:
            ws.close()
        except Exception as e:
            print(f"Error closing WebSocket connection: {e}")
