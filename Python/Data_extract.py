import os 
import re

energy_pattern = re.compile(r"(?:[U]?CCSD\(T\)-F12B/aug-cc-pV[D-T-Q]Z energy|UMP2/aug-cc-pVDZ energy)\s*=\s*([-]?\d+\.\d+)", re.IGNORECASE)
zpe_pattern = re.compile(r"Zero point energy:\s*(\d+\.\d+)\s*\[H\]", re.IGNORECASE)

folder_path=os.getcwdb() #ez a current folder
file_data={} #ide fogja berakni a fileok a adatait egy dictionarybe 

for filename in os.listdir(folder_path):
    if isinstance(filename, bytes): #valamiért a fileneveket byteoknak érzékeli nem stringnek, az isinstance megvizsgálja, hogy a filename byte-e
        filename = filename.decode('utf-8') #ha igen akkor átalakítja stringé a decode syntaxxal
    if isinstance(folder_path, bytes):
        folder_path=folder_path.decode('utf-8')
    if filename.endswith(".out"): #megvizsgálja, hogy a file .out-ra végződik-e
        file_path = os.path.join(folder_path, filename)
        energy = None
        zpe_value = None
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                content = file.read()
                # Search for UCCSD(T)-F12B energy
                energy_match = energy_pattern.search(content)
                if energy_match:
                    energy = energy_match.group(1)
                # Search for ZPE
                zpe_match = zpe_pattern.search(content)
                if zpe_match:
                    zpe_value = zpe_match.group(1)
                # Store in dictionary
                file_data[filename] = {"Energy": energy, "ZPE": zpe_value}
        except Exception as e:
            print(f"Error reading {filename}: {e}")
# Save to summary file
with open("summary.csv", "w") as summary_file:
    summary_file.write(f"Filename\tEnergy\tZPE\n\n")
    for filename, data in sorted(file_data.items()):
        energy = data["Energy"] if data["Energy"] is not None else "Not found"
        zpe = data["ZPE"] if data["ZPE"] is not None else "Not found"
        summary_file.write(f"{filename}\t{energy}\t{zpe}\n\n")