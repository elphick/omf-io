def validate_surface_data(surface_data):
    """Validate the triangulated surface data.

    Args:
        surface_data (dict): A dictionary with 'vertices' and 'faces'.

    Raises:
        ValueError: If the surface data is invalid.
    """
    vertices = surface_data.get('vertices', [])
    faces = surface_data.get('faces', [])

    # Check vertices
    if not vertices:
        raise ValueError("The vertices list is empty.")
    for vertex in vertices:
        if not (isinstance(vertex, (list, tuple)) and len(vertex) == 3):
            raise ValueError(f"Invalid vertex: {vertex}. Each vertex must be a tuple of three numbers.")

    # Check faces
    if not faces:
        raise ValueError("The faces list is empty.")
    for face in faces:
        if not (isinstance(face, (list, tuple)) and len(face) == 3):
            raise ValueError(f"Invalid face: {face}. Each face must have exactly three vertex indices.")
        if any(idx < 0 or idx >= len(vertices) for idx in face):
            raise ValueError(f"Face {face} references invalid vertex indices.")

    # Check for duplicate faces
    if len(faces) != len(set(tuple(sorted(face)) for face in faces)):
        raise ValueError("Duplicate faces detected.")

    # Check for degenerate faces
    for face in faces:
        if len(set(face)) < 3:
            raise ValueError(f"Degenerate face detected: {face}.")
