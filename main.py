import time
from src.emitter import Emitter

emitter = Emitter(100, 100, emit_rate=5)
for frame in range(50):
    emitter.update(0.1)  # 0.1 sekundy (symulacja ~10 FPS)
    print(f"Cząstek aktywnych: {len(emitter.particles)}")
    time.sleep(0.1)
