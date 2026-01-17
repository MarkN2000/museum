import json
import base64
import struct

def create_plane_gltf(filepath):
    # Geometry Data
    # 4 vertices: BL, BR, TL, TR
    # Position (Vec3 float)
    positions = [
        -0.5, -0.5, 0.0,  # 0: Bottom-Left
         0.5, -0.5, 0.0,  # 1: Bottom-Right
        -0.5,  0.5, 0.0,  # 2: Top-Left
         0.5,  0.5, 0.0   # 3: Top-Right
    ]
    
    # Normals (Vec3 float) - all pointing +Z
    normals = [
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0
    ]
    
    # UVs (Vec2 float)
    # Standard UV mapping:
    # (0,0) usually Top-Left in some contexts, but in glTF (0,0) is Top-Left of the texture? 
    # Actually in glTF: (0,0) is Upper-Left. Wait, glTF spec says (0,0) is Top-Left.
    # Let's map standard:
    # 0: BL -> (0, 1)
    # 1: BR -> (1, 1)
    # 2: TL -> (0, 0)
    # 3: TR -> (1, 0)
    uvs = [
        0.0, 1.0, # 0: BL corresponds to Bottom of image (V=1)
        1.0, 1.0, # 1: BR corresponds to Bottom of image (V=1)
        0.0, 0.0, # 2: TL corresponds to Top of image (V=0)
        1.0, 0.0  # 3: TR corresponds to Top of image (V=0)
    ]
    # NOTE: If texture is upside down, we swap 0 and 1.
    
    # Indices (Scalar unsigned short)
    # Triangle 1: 0 (BL), 1 (BR), 2 (TL) -> CCW
    # Triangle 2: 2 (TL), 1 (BR), 3 (TR) -> CCW
    indices = [0, 1, 2, 2, 1, 3]

    # Pack data
    buffer_data = bytearray()
    
    # Offsets (Keep track for accessors)
    pos_offset = 0
    for val in positions:
        buffer_data.extend(struct.pack('<f', val))
        
    normal_offset = len(buffer_data)
    for val in normals:
        buffer_data.extend(struct.pack('<f', val))
        
    uv_offset = len(buffer_data)
    for val in uvs:
        buffer_data.extend(struct.pack('<f', val))
        
    indices_offset = len(buffer_data)
    for val in indices:
        buffer_data.extend(struct.pack('<H', val))
        
    total_length = len(buffer_data)
    
    # Encode to Base64
    b64_data = base64.b64encode(buffer_data).decode('utf-8')
    uri = f"data:application/octet-stream;base64,{b64_data}"

    # GLTF JSON Structure
    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "Plane"}],
        "meshes": [
            {
                "name": "PlaneMesh",
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 0,
                            "NORMAL": 1,
                            "TEXCOORD_0": 2
                        },
                        "indices": 3,
                        "mode": 4, # TRIANGLES
                        "material": 0
                    }
                ]
            }
        ],
        "materials": [
            {
                "name": "DefaultMaterial",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "metallicFactor": 0,
                    "roughnessFactor": 1
                },
                "doubleSided": True 
            }
        ],
        "buffers": [
            {
                "uri": uri,
                "byteLength": total_length
            }
        ],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": pos_offset,
                "byteLength": 4 * 3 * 4, # 4 verts * 3 float * 4 bytes
                "target": 34962 # ARRAY_BUFFER
            },
            {
                "buffer": 0,
                "byteOffset": normal_offset,
                "byteLength": 4 * 3 * 4,
                "target": 34962
            },
            {
                "buffer": 0,
                "byteOffset": uv_offset,
                "byteLength": 4 * 2 * 4,
                "target": 34962
            },
            {
                "buffer": 0,
                "byteOffset": indices_offset,
                "byteLength": 6 * 2, # 6 indices * 2 bytes (ushort)
                "target": 34963 # ELEMENT_ARRAY_BUFFER
            }
        ],
        "accessors": [
            { # POSTION
                "bufferView": 0,
                "componentType": 5126, # FLOAT
                "count": 4,
                "type": "VEC3",
                "max": [0.5, 0.5, 0.0],
                "min": [-0.5, -0.5, 0.0]
            },
            { # NORMAL
                "bufferView": 1,
                "componentType": 5126, # FLOAT
                "count": 4,
                "type": "VEC3"
            },
            { # TEXCOORD_0
                "bufferView": 2,
                "componentType": 5126, # FLOAT
                "count": 4,
                "type": "VEC2"
            },
            { # INDICES
                "bufferView": 3,
                "componentType": 5123, # UNSIGNED_SHORT
                "count": 6,
                "type": "SCALAR"
            }
        ]
    }

    with open(filepath, 'w') as f:
        json.dump(gltf, f, indent=2)
    
    print(f"Generated {filepath}")

if __name__ == "__main__":
    create_plane_gltf("assets/plane.gltf")
