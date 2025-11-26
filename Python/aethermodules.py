import os
import sys
import numpy as np
import pandas as pd
import random as rd
import re

def extract_geometry_block(content, start_pos):
    lines = content[start_pos:].split('\n')
    
    # Find the number of atoms line
    i = 0
    while i < len(lines) and not lines[i].strip().isdigit():
        i += 1
    
    if i >= len(lines) or not lines[i].strip().isdigit():
        return None
    
    num_atoms = int(lines[i].strip())
    i += 1
    
    # Get title line
    title_line = lines[i].strip() if i < len(lines) else "No title"
    i += 1
    
    # Get atom lines
    atom_lines = []
    for j in range(num_atoms):
        if i + j < len(lines):
            atom_lines.append(lines[i + j].strip())
    
    if len(atom_lines) == num_atoms:
        # Return the full geometry block as text
        geom_text = f"{num_atoms}\n{title_line}\n"
        for atom_line in atom_lines:
            geom_text += f"{atom_line}\n"
        return geom_text.strip()
    
    return None

def blocking(filename):
    blocks = []
    with open(filename, 'r') as file:
        content = file.read()
        lines = content.split("\n")
        block = []
        line_count = 0
        block_size = int(lines[0])+2

        for line in lines:
            block.append(line)
            line_count += 1

            # When a full block of 11 lines is collected
            if line_count % block_size == 0:
                # Break down the block into individual lines (all 11 lines)
                blocks.append(block)
                block = []  # Reset for next block

def reorder_geometry(outfile):
    # Split the input into lines
    lines = outfile.strip().split('\n')
    
    # Extract header (first two lines) and atom coordinates
    header = lines[:2]
    atom_lines = lines[2:]
    
    # Parse atom coordinates into a list of tuples (atom_type, x, y, z)
    atoms = []
    for line in atom_lines:
        parts = line.split()
        if len(parts) == 4:  # Ensure it's a valid atom line
            atom_type, x, y, z = parts
            atoms.append((atom_type, x, y, z))
    
    # Group atoms by type (e.g., H, C, O, Cl)
    grouped_atoms = {}
    for atom in atoms:
        atom_type = atom[0]
        if atom_type not in grouped_atoms:
            grouped_atoms[atom_type] = []
        grouped_atoms[atom_type].append(atom)
    
    # Define the desired order of atom types (e.g., H, Cl, C, O)
    atom_order = ['H', 'C', 'O', 'Cl']
    
    # Reconstruct the atom lines in the desired order
    ordered_atoms = []
    for atom_type in atom_order:
        if atom_type in grouped_atoms:
            ordered_atoms.extend(grouped_atoms[atom_type])
    
    # Format the output
    output_lines = header[:]
    for atom in ordered_atoms:
        # Reformat each atom line to match the original spacing
        line = f"{atom[0]:<2} {float(atom[1]):>14.10f} {float(atom[2]):>14.10f} {float(atom[3]):>14.10f}"
        output_lines.append(line)
    
    return '\n'.join(output_lines)

def greeting(name):
    print(f"Hello {name}")