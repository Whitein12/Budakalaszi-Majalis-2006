import os
import re

ccsdtq_pattern = re.compile(r'!\s*CCSDT\(Q\)\s*STATE\s*1\.1\s*Energy\s+([-]?\d+\.\d+)', re.IGNORECASE)
ccsdt_pattern = re.compile(r'!\s*CCSDT\s*STATE\s*1\.1\s*Energy\s+([-]?\d+\.\d+)', re.IGNORECASE)
ccsd_t_pattern = re.compile(r'!\s*CCSD\(T\)\s*STATE\s*1\.1\s*Energy\s+([-]?\d+\.\d+)', re.IGNORECASE)

folder_path = os.getcwd()
file_data = {}

for filename in os.listdir(folder_path):
    if isinstance(filename, bytes):
        filename = filename.decode('utf-8')
    if filename.__contains__('uccsd_q_vdz') and filename.endswith(".out"):
        file_path = os.path.join(folder_path, filename)
        ccsdt = None
        ccsd_t = None
        ccsdtq = None
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                content = file.read()
                ccsdt_match = ccsdt_pattern.search(content)
                if ccsdt_match:
                    ccsdt = ccsdt_match.group(1)
                ccsd_t_match = ccsd_t_pattern.search(content)
                if ccsd_t_match:
                    ccsd_t = ccsd_t_match.group(1)
                ccsdtq_match = ccsdtq_pattern.search(content)
                if ccsdtq_match:
                    ccsdtq = ccsdtq_match.group(1)
            # Store in dictionary
            file_data[filename] = {"CCSDT": ccsdt, "CCSD(T)": ccsd_t, "CCSDT(Q)": ccsdtq}
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Save to summary file
with open("summary_mrcc.csv", "w") as summary_file:
    summary_file.write("Filename,\t CCSDT,\t CCSD(T),\t CCSDT(Q)\n")
    for filename, data in sorted(file_data.items()):
        ccsdt = data["CCSDT"] if data["CCSDT"] is not None else "Not found"
        ccsd_t = data["CCSD(T)"] if data["CCSD(T)"] is not None else "Not found"
        ccsdtq = data["CCSDT(Q)"] if data["CCSDT(Q)"] is not None else "Not found"
        summary_file.write(f"{filename},\t {ccsdt},\t {ccsd_t},\t {ccsdtq}\n")