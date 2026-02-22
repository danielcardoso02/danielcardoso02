from PIL import Image, ImageDraw
from fetch_data import fetch_contribution_data

# --- Configuration ---
BLOCK_SIZE = 12
PADDING = 4
CORNER_RADIUS = 2
BG_COLOR = "#0d1117"
EMPTY_COLOR = "#161b22"
WIDTH = 53 * (BLOCK_SIZE + PADDING) + PADDING
HEIGHT = 7 * (BLOCK_SIZE + PADDING) + PADDING

def draw_frame(fixed_blocks, falling_blocks):
    """Draws a single frame of the animation."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 1. Draw the empty background grid
    for x in range(53):
        for y in range(7):
            x0 = PADDING + (x * (BLOCK_SIZE + PADDING))
            y0 = PADDING + (y * (BLOCK_SIZE + PADDING))
            draw.rounded_rectangle([x0, y0, x0+BLOCK_SIZE, y0+BLOCK_SIZE], radius=CORNER_RADIUS, fill=EMPTY_COLOR)

    # 2. Draw the blocks that have already landed
    for (x, y, color) in fixed_blocks:
        x0 = PADDING + (x * (BLOCK_SIZE + PADDING))
        y0 = PADDING + (y * (BLOCK_SIZE + PADDING))
        draw.rounded_rectangle([x0, y0, x0+BLOCK_SIZE, y0+BLOCK_SIZE], radius=CORNER_RADIUS, fill=color)
        
    # 3. Draw the blocks currently falling
    for (x, current_y, color) in falling_blocks:
        x0 = PADDING + (x * (BLOCK_SIZE + PADDING))
        y0 = PADDING + (current_y * (BLOCK_SIZE + PADDING))
        draw.rounded_rectangle([x0, y0, x0+BLOCK_SIZE, y0+BLOCK_SIZE], radius=CORNER_RADIUS, fill=color)
        
    return img

def generate_gif():
    print("Fetching data for animation...")
    data = fetch_contribution_data()
    weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    
    frames = []
    fixed_blocks = [] # Blocks that have finished falling
    
    print("Calculating drop paths and rendering frames (this might take a minute)...")
    
    # Process column by column (left to right)
    for x_index, week in enumerate(weeks):
        # Find all days in this week that have contributions, sort them so bottom ones fall first
        active_days = [day for day in week['contributionDays'] if day['contributionCount'] > 0]
        active_days.sort(key=lambda d: d['weekday'], reverse=True)
        
        for day in active_days:
            target_y = day['weekday']
            color = day['color']
            
            # Animate this block falling down its column
            current_y = 0
            while current_y < target_y:
                # Append a frame with this block currently falling
                frames.append(draw_frame(fixed_blocks, [(x_index, current_y, color)]))
                current_y += 1 # Drop speed (increase to make it fall faster)
                
            # The block has landed! Add it to the fixed blocks list
            fixed_blocks.append((x_index, target_y, color))
            
    # Add a few seconds of the final completed board at the end
    for _ in range(20):
        frames.append(draw_frame(fixed_blocks, []))

    print(f"Stitching {len(frames)} frames into a GIF...")
    # Save the frames as an animated GIF
    frames[0].save(
        "github-tetris.gif",
        save_all=True,
        append_images=frames[1:],
        duration=40, # Milliseconds per frame (lower is faster)
        loop=0 # 0 means loop infinitely
    )
    print("✅ Arcade animation complete! Check your folder for github-tetris.gif")

if __name__ == "__main__":
    generate_gif()
