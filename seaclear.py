import math
import os
import sys
import time


def get_terminal_text():
    """Captures standard dimensions to simulate sweeping over current layout."""
    try:
        columns, lines = os.get_terminal_size()
    except OSError:
        columns, lines = 80, 24
    return columns, lines


def sea_clear():
    columns, lines = get_terminal_text()

    # Wave character palette from deep water to crashing foam
    # " " (water/background) -> "." -> "~" -> "≈" -> "*" -> "░" (foam crest)
    wave_chars = " .~~≈*░"
    palette_len = len(wave_chars)

    # Hide cursor
    sys.stdout.write("\033[?25l")

    # The tide rises from the bottom (lines) and washes past the top (-15 for padding)
    for wave_front in range(lines + 5, -15, -1):
        output = []

        for y in range(lines):
            row = []
            for x in range(columns):
                # 1. Base distance from the rising tide front
                distance_to_wave = y - wave_front

                if distance_to_wave < 0:
                    # Below the wave front: The water has already washed over this area!
                    # We randomize characters to look like swirling sea foam dissolving text
                    if distance_to_wave > -4:
                        row.append(" ")  # Receding water
                    else:
                        row.append(" ")  # Wiped clean

                elif distance_to_wave > 8:
                    # Far above the wave: The text/commands haven't been touched yet.
                    # We don't overwrite this block so existing text visually remains.
                    # (Represented by keeping it blank or letting it be overwritten later)
                    row.append("\033[1C")  # Move cursor forward without drawing over old text

                else:
                    # 2. Inside the moving Wave: Compute Sine Wave Fluid Ripples
                    # Adding mathematical variation based on X creates a cresting pattern
                    ripple = math.sin(x * 0.25 + wave_front * 0.4) * 2.0
                    intensity = int(
                        ((8 - distance_to_wave) + ripple)
                        / 10.0
                        * (palette_len - 1)
                    )
                    intensity = max(0, min(palette_len - 1, intensity))

                    char = wave_chars[intensity]

                    # 3. Inject Ocean Colors (ANSI Blue/Cyan)
                    if char in ["░", "*"]:
                        # Wave Crest / Crashing Foam (Bright White/Cyan)
                        row.append(f"\033[1;36m{char}\033[0m")
                    elif char in ["≈", "~"]:
                        # Deep Wave Body (Blue)
                        row.append(f"\033[34m{char}\033[0m")
                    else:
                        # Shallow water line
                        row.append(f"\033[30;1m{char}\033[0m")

            output.append("".join(row))

        # Move cursor to top left, print the frame, and flush buffer
        sys.stdout.write("\033[H" + "\n".join(output))
        sys.stdout.flush()
        time.sleep(0.04)  # Wave speed (~25 FPS)

    # Final Step: Fully reset the terminal window buffer (True clear)
    sys.stdout.write("\033[?25h\033[2J\033[H")
    sys.stdout.flush()


if __name__ == "__main__":
    sea_clear()
  
