import numpy as np
from PIL import Image

class LCG:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (1103515245 * self.state + 12345) % (2**31)
        return self.state

def get_shifts_for_iteration(lcg, h, w):
    shifts_r = [lcg.next() % w for _ in range(h)]
    shifts_g = [lcg.next() % w for _ in range(h)]
    shifts_b = [lcg.next() % w for _ in range(h)]
    return shifts_r, shifts_g, shifts_b

def decrypt_image(input_path, output_path, key, iterations=10):
    # Load ciphered image
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img)
    R, G, B = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    lcg = LCG(key)
    all_shifts = []
    
    # Pre-compute all matrix dimensions and shift values 
    # to perfectly reverse the iteration loop
    current_shape = R.shape
    for i in range(iterations):
        # Simulate transposition dimension changes
        current_shape = (current_shape[1], current_shape[0])
        h, w = current_shape
        shifts = get_shifts_for_iteration(lcg, h, w)
        all_shifts.append(shifts)
        
    # Execute inverse operations in reverse order
    for i in range(iterations - 1, -1, -1):
        shifts_r, shifts_g, shifts_b = all_shifts[i]
        h, w = R.shape
        
        # Apply inverse displacement (negative shift)
        for row in range(h):
            R[row] = np.roll(R[row], -shifts_r[row])
            G[row] = np.roll(G[row], -shifts_g[row])
            B[row] = np.roll(B[row], -shifts_b[row])
            
        # Inverse transpose
        R, G, B = R.T, G.T, B.T
        
    # Concatenate the decrypted RGB components
    dec_arr = np.dstack((R, G, B))
    dec_img = Image.fromarray(dec_arr.astype(np.uint8))
    dec_img.save(output_path)
    print(f"Decryption complete. Saved to {output_path}")

if __name__ == "__main__":
    # Example usage
    decrypt_image("./output/flag.png", "decrypted_flag.png", key=4397328654844826923795068102505872571721883526553349659561256924505973939597593482272505698004801207988043088656411102133523080581, iterations=67)