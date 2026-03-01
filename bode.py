import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# 1. Define the Transfer Function: G(s) = 25 / (s^2 + 4s + 25)
# This represents a typical second-order system
num = [25]
den = [1, 4, 25]
sys = ctrl.TransferFunction(num, den)

# 2. Calculate Stability Margins
gm, pm, wg, wp = ctrl.margin(sys)

# 3. Create Visualization
fig = plt.figure(figsize=(12, 10))

# --- BODE PLOT (Frequency in Hz) ---
# Calculate data
mag, phase, omega = ctrl.bode(sys, Hz=True, plot=False)
freq_hz = omega / (2 * np.pi)

# Subplot: Magnitude
ax_mag = plt.subplot(2, 2, 1)
ax_mag.semilogx(freq_hz, 20 * np.log10(mag), color='blue', lw=1.5)
ax_mag.axhline(0, color='black', lw=1, linestyle='-') # 0dB line
if wg > 0:
    ax_mag.plot(wg/(2*np.pi), 0, 'ro') # Gain crossover frequency
ax_mag.set_title(f'Magnitude (Gain Margin: {20*np.log10(gm):.2f} dB)')
ax_mag.set_ylabel('Magnitude (dB)')
ax_mag.grid(True, which="both", ls="-", alpha=0.5)

# Subplot: Phase
ax_phase = plt.subplot(2, 2, 3)
ax_phase.semilogx(freq_hz, np.degrees(phase), color='blue', lw=1.5)
ax_phase.axhline(-180, color='red', lw=1, linestyle='--') # Stability limit
if wp > 0:
    ax_phase.plot(wp/(2*np.pi), -180 + pm, 'ro') # Phase margin point
ax_phase.set_title(f'Phase (Phase Margin: {pm:.2f}°)')
ax_phase.set_ylabel('Phase (deg)')
ax_phase.set_xlabel('Frequency (Hz)')
ax_phase.grid(True, which="both", ls="-", alpha=0.5)

# --- STEP RESPONSE ---
ax_step = plt.subplot(1, 2, 2)
t, y = ctrl.step_response(sys)
ax_step.plot(t, y, color='red', lw=2)
ax_step.set_title('Step Response')
ax_step.set_xlabel('Time (seconds)')
ax_step.set_ylabel('Amplitude')
ax_step.grid(True)

# Annotate stability status
status = "Stable" if (20*np.log10(gm) > 0 and pm > 0) else "Unstable"
fig.suptitle(f'System Analysis - Stability: {status}', fontsize=16)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Print metrics to console
print(f"Gain Margin: {20*np.log10(gm):.2f} dB at {wg/(2*np.pi):.2f} Hz")
print(f"Phase Margin: {pm:.2f}° at {wp/(2*np.pi):.2f} Hz")
