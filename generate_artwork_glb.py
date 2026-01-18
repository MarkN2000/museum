"""
Generate GLB files with embedded textures for AR display.

Usage:
    python generate_artwork_glb.py <image_path> <width_cm> <height_cm> [output_path]

Example:
    python generate_artwork_glb.py assets/images/03621.jpg 37.7 25.5

Dependencies:
    pip install Pillow
"""

import sys
import os
import json
import struct
from pathlib import Path

try:
    from PIL import Image
    import io
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


def create_artwork_glb(image_path: str, width_cm: float, height_cm: float, output_path: str = None) -> str:
    """
    Create a GLB file with a plane mesh and embedded image texture.
    """
    # Convert cm to meters
    width_m = width_cm / 100
    height_m = height_cm / 100
    
    # Load and encode image
    with Image.open(image_path) as img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGB')
        
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=90)
        image_bytes = img_buffer.getvalue()
    
    # Create plane vertices (centered at origin)
    hw = width_m / 2
    hh = height_m / 2
    
    # Separate arrays for non-interleaved data
    positions = [
        -hw, -hh, 0,  # 0: Bottom-left
         hw, -hh, 0,  # 1: Bottom-right
         hw,  hh, 0,  # 2: Top-right
        -hw,  hh, 0,  # 3: Top-left
    ]
    
    normals = [
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
        0, 0, 1,
    ]
    
    texcoords = [
        0, 1,  # Bottom-left
        1, 1,  # Bottom-right
        1, 0,  # Top-right
        0, 0,  # Top-left
    ]
    
    # Indices (two triangles, counter-clockwise)
    indices = [0, 1, 2, 0, 2, 3]
    
    # Pack binary data
    position_bytes = struct.pack(f'{len(positions)}f', *positions)
    normal_bytes = struct.pack(f'{len(normals)}f', *normals)
    texcoord_bytes = struct.pack(f'{len(texcoords)}f', *texcoords)
    index_bytes = struct.pack(f'{len(indices)}H', *indices)
    
    # Pad index_bytes to 4-byte alignment
    index_padding = (4 - len(index_bytes) % 4) % 4
    index_bytes += b'\x00' * index_padding
    
    # Calculate offsets
    position_offset = 0
    position_length = len(position_bytes)
    
    normal_offset = position_offset + position_length
    normal_length = len(normal_bytes)
    
    texcoord_offset = normal_offset + normal_length
    texcoord_length = len(texcoord_bytes)
    
    index_offset = texcoord_offset + texcoord_length
    index_length = len(index_bytes) - index_padding  # Original length without padding
    
    image_offset = index_offset + len(index_bytes)  # Include padding
    image_length = len(image_bytes)
    
    # Pad image_bytes to 4-byte alignment
    image_padding = (4 - len(image_bytes) % 4) % 4
    image_bytes_padded = image_bytes + b'\x00' * image_padding
    
    total_buffer_length = image_offset + len(image_bytes_padded)
    
    # Create GLTF JSON
    gltf = {
        "asset": {"version": "2.0", "generator": "museum-ar-generator"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "Artwork"}],
        "meshes": [{
            "primitives": [{
                "attributes": {
                    "POSITION": 0,
                    "NORMAL": 1,
                    "TEXCOORD_0": 2
                },
                "indices": 3,
                "material": 0
            }]
        }],
        "accessors": [
            # 0: POSITION
            {
                "bufferView": 0,
                "componentType": 5126,  # FLOAT
                "count": 4,
                "type": "VEC3",
                "max": [hw, hh, 0],
                "min": [-hw, -hh, 0]
            },
            # 1: NORMAL
            {
                "bufferView": 1,
                "componentType": 5126,  # FLOAT
                "count": 4,
                "type": "VEC3"
            },
            # 2: TEXCOORD_0
            {
                "bufferView": 2,
                "componentType": 5126,  # FLOAT
                "count": 4,
                "type": "VEC2"
            },
            # 3: INDICES
            {
                "bufferView": 3,
                "componentType": 5123,  # UNSIGNED_SHORT
                "count": 6,
                "type": "SCALAR"
            }
        ],
        "bufferViews": [
            # 0: Position
            {"buffer": 0, "byteOffset": position_offset, "byteLength": position_length, "target": 34962},
            # 1: Normal
            {"buffer": 0, "byteOffset": normal_offset, "byteLength": normal_length, "target": 34962},
            # 2: TexCoord
            {"buffer": 0, "byteOffset": texcoord_offset, "byteLength": texcoord_length, "target": 34962},
            # 3: Indices
            {"buffer": 0, "byteOffset": index_offset, "byteLength": index_length, "target": 34963},
            # 4: Image
            {"buffer": 0, "byteOffset": image_offset, "byteLength": image_length}
        ],
        "buffers": [{"byteLength": total_buffer_length}],
        "materials": [{
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0},
                "metallicFactor": 0,
                "roughnessFactor": 1
            },
            "doubleSided": True,
            "name": "ArtworkMaterial"
        }],
        "textures": [{"source": 0, "sampler": 0}],
        "images": [{"bufferView": 4, "mimeType": "image/jpeg"}],
        "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]
    }
    
    # Encode JSON
    gltf_json = json.dumps(gltf, separators=(',', ':'))
    gltf_json_bytes = gltf_json.encode('utf-8')
    
    # Pad JSON to 4-byte alignment
    json_padding = (4 - len(gltf_json_bytes) % 4) % 4
    gltf_json_bytes += b' ' * json_padding
    
    # Binary buffer
    binary_buffer = position_bytes + normal_bytes + texcoord_bytes + index_bytes + image_bytes_padded
    
    # GLB Header
    glb_length = 12 + 8 + len(gltf_json_bytes) + 8 + len(binary_buffer)
    glb_header = struct.pack('<4sII', b'glTF', 2, glb_length)
    
    # JSON chunk
    json_chunk_header = struct.pack('<II', len(gltf_json_bytes), 0x4E4F534A)  # JSON
    
    # Binary chunk
    bin_chunk_header = struct.pack('<II', len(binary_buffer), 0x004E4942)  # BIN
    
    # Combine all
    glb_data = glb_header + json_chunk_header + gltf_json_bytes + bin_chunk_header + binary_buffer
    
    # Determine output path
    if output_path is None:
        base_name = Path(image_path).stem
        output_path = f"assets/{base_name}.glb"
    
    # Write file
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(glb_data)
    
    print(f"Generated: {output_path}")
    print(f"  Size: {width_cm} x {height_cm} cm ({width_m:.3f} x {height_m:.3f} m)")
    print(f"  File size: {len(glb_data):,} bytes")
    
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    
    image_path = sys.argv[1]
    width_cm = float(sys.argv[2])
    height_cm = float(sys.argv[3])
    output_path = sys.argv[4] if len(sys.argv) > 4 else None
    
    create_artwork_glb(image_path, width_cm, height_cm, output_path)
