import numpy as np
from PIL import Image

class LCG:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        # POSIX standard parameters for LCG
        self.state = (1103515245 * self.state + 12345) % (2**31)
        return self.state

def get_shifts_for_iteration(lcg, h, w):
    shifts_r = [lcg.next() % w for _ in range(h)]
    shifts_g = [lcg.next() % w for _ in range(h)]
    shifts_b = [lcg.next() % w for _ in range(h)]
    return shifts_r, shifts_g, shifts_b

def encrypt_image(input_path, output_path, key, iterations=10):
    # Load plain image and extract RGB components
    img = Image.open(input_path).convert('RGB')
    arr = np.array(img)
    R, G, B = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    lcg = LCG(key)
    
    for i in range(iterations):
        # Transpose matrices (rows become columns)
        R, G, B = R.T, G.T, B.T
        h, w = R.shape
        
        # Generate displacement factor arrays for R, G, B
        shifts_r, shifts_g, shifts_b = get_shifts_for_iteration(lcg, h, w)
        
        # Apply cyclic shift displacement 
        for row in range(h):
            R[row] = np.roll(R[row], shifts_r[row])
            G[row] = np.roll(G[row], shifts_g[row])
            B[row] = np.roll(B[row], shifts_b[row])
            
    # Concatenate the encrypted RGB components
    enc_arr = np.dstack((R, G, B))
    enc_img = Image.fromarray(enc_arr.astype(np.uint8))
    enc_img.save(output_path)
    print(f"Encryption complete. Saved to {output_path}")

if __name__ == "__main__":
    # key is RSA-260 factor
    encrypt_image("flag.png", "./output/flag.png", key=4397328654844826923795068102505872571721883526553349659561256924505973939597593482272505698004801207988043088656411102133523080581, iterations=67)