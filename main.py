import time
from src.emitter import Emitter

emitter = Emitter(100, 100, emit_rate=15) 
for frame in range(100):  
    emitter.update(0.033)
    
    active_particles = len(emitter.particles)
    print(f"Frame {frame:3d}: {active_particles:3d} active particles")
    
    # Show some particle details every 10 frames
    if frame % 10 == 0 and emitter.particles:
        sample_particle = emitter.particles[0]
        print(f"  Sample particle: pos=({sample_particle.x:.1f}, {sample_particle.y:.1f}), "
              f"life={sample_particle.life:.2f}, alpha={sample_particle.color[3]:.2f}")
        
        

    