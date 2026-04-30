import grpc
from concurrent import futures
import hand_pos_pb2
import hand_pos_pb2_grpc
import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class HandTrackerServicer(hand_pos_pb2_grpc.HandTrackerServicer):
    def __init__(self):
        self.prev_x = 0.5
        self.prev_y = 0.5

    def SendPosition(self, request, context):
        # 1. Heartbeat check - See if data is arriving at all
        print(f"Received coords: x={request.x:.2f}, y={request.y:.2f}")

        dx = request.x - self.prev_x
        dy = request.y - self.prev_y
        
        # 2. Lower the threshold for testing (from 0.03 to 0.01)
        threshold = 0.01
        direction = None

        if abs(dx) > abs(dy):
            if abs(dx) > threshold:
                direction = "RIGHT" if dx > 0 else "LEFT"
        else:
            if abs(dy) > threshold:
                direction = "DOWN" if dy > 0 else "UP"

        if direction:
            print(f"MATCH: {direction}")
            r.publish("aim_direction", direction)
        
        self.prev_x, self.prev_y = request.x, request.y
        return hand_pos_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hand_pos_pb2_grpc.add_HandTrackerServicer_to_server(HandTrackerServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Tracking Service started on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()