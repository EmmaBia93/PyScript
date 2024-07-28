import subprocess

def is_w32tm_service_running():
    try:
        result = subprocess.run(['sc', 'query', 'w32time'], capture_output=True, text=True, check=True)
        output = result.stdout

        if "RUNNING" in output:
            return True
        else:
            return False
    except:
        return False

# Uso:
if is_w32tm_service_running():
    print("El servicio w32tm está en funcionamiento.")
else:
    print("El servicio w32tm no está en funcionamiento.")
