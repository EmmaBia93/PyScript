from colorama import Fore, Style, init, Back
from log_symbols import LogSymbols
import subprocess
import shutil
import re
import time
import paramiko
from halo import Halo

class Main:
    
    def __init__(self) -> None:
        init()
        self.running = True
        size = shutil.get_terminal_size()
        self.columnas = size.columns
        

    def menu_principal(self):
        dic_functions = {
            1: self.ping,
            2: self.marcar_desmarcar,
            3: self.cargar_backup,
            4: self.establecer_hora,
            5: self.compliance
        }
        while self.running:
            subprocess.call("clear", shell=True)
            
            txt_tecnicos = " TECNICOS "
            txt_menu = "( MENU PRINCIPAL )"
            print('\r'+ Style.DIM + f"{txt_tecnicos:#^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            print('\r' +Fore.BLACK+Back.RED+f"{txt_menu:-^{self.columnas}}"+Style.RESET_ALL+"\n")
            print('\r'+Style.BRIGHT + Fore.BLUE)
            print(f"{'1 - PING': ^{self.columnas}}\n")
            print(f"{'2 - MARCAR O DESMARCAR LA TARJETA': ^{self.columnas}}\n")
            print(f"{'3 - CARGAR BACKUP': ^{self.columnas}}\n")
            print(f"{'4 - ESTABLECER HORA': ^{self.columnas}}\n")
            print(f"{'5 - COMPLIANCE': ^{self.columnas}}\n")
            print(f"{'6 - SALIR': ^{self.columnas}}\n")
            print(Style.RESET_ALL+"\n")

            try:
                choice = input(Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " ")
                if choice.strip().isdigit():
                    choice = int(choice)
                    if choice in dic_functions:
                        dic_functions[choice]()
                    elif choice == 6:
                        self.running = False
                    else:
                        print(LogSymbols.WARNING.value + Fore.YELLOW+" POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL) 
                        time.sleep(1)
                else:
                    print(LogSymbols.WARNING.value + Fore.YELLOW+" POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL) 
                    time.sleep(1)
                        
            except EOFError:
                pass    



  
  

    def ping(self):

        self.ping_running = True
        
        while True:
            subprocess.call("clear", shell=True)
            ips = {1:'192.168.1.20',2:'192.168.88.1',3:'192.168.1.100'}
            print('\r' +Fore.BLACK+Back.RED+f"{" PING ":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            print('\r'+Style.BRIGHT + Fore.BLUE)
            print(f"{'1 - ANTENA': ^{self.columnas}}")
            print(f"{'2 - UBIQUITI': ^{self.columnas}}")
            print(f"{'3 - FW': ^{self.columnas}}")
            print(f"{'4 - CUSTOM': ^{self.columnas}}")
            print(f"{'5 - VOLVER AL MENU PRINCIPAL': ^{self.columnas}}")

            print(Style.RESET_ALL+"\n")
            
            try:
                choice = input(Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " ")

                if choice in ips:
                   proceso = subprocess.Popen(['ping', ips[choice], '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
                   if proceso:
                    subprocess.call("cls", shell=True)
                    while self.ping_running:
                        output = proceso.stdout.readline()
                        if output:
                            print(output.strip())
                        
                elif choice == 4:
                    subprocess.call("cls", shell=True)
                    ip = input(LogSymbols.SUCCESS.value+" INGRESE LA IP PARA REALIZAR EL PING: ")
                    proceso = subprocess.Popen(['ping', ip, '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
                    if proceso:
                        subprocess.call("cls", shell=True)
                        while self.ping_running:
                            output = proceso.stdout.readline()
                            if output:
                                print(output.strip())
                    
                elif choice == 5:
                
                    return
                
                else:
                    print(choice)
                    print(LogSymbols.WARNING.value + Fore.YELLOW+" POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)
                    time.sleep(1) 
            
                
            
            except ValueError as e:
                    print(LogSymbols.WARNING.value +Fore.YELLOW+" POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL) 
                    time.sleep(1)
            except KeyboardInterrupt:
                self.ping_running = False
            finally:
                if not self.ping_running:
                    proceso.terminate()  # Asegurarse de terminar el proceso de ping
                    proceso.wait()       # Esperar a que el proceso termine completamente
                    spinner = Halo(text="Saliendo...", spinner="dots",color="red")
                    print("\n\nPresione ENTER para volver al menu principal")
                    spinner.start()
                   
                    input()
                    spinner.stop()
                    return  # Regresar al menú principal
            
    
       

    def marcar_desmarcar(self):

        while True:
            subprocess.call("cls", shell=True)
            print('\r' +Fore.BLACK+Back.RED+f"{" TARJETA DE RED ":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            print('\r'+Style.BRIGHT + Fore.BLUE)
            print(f"{'1 - FIJAR/DESMARCAR': ^{self.columnas}}")
            print(f"{'2 - IP PARA FIJAR': ^{self.columnas}}")
            print(f"{'3 - VOLVER AL MENU PRINCIPAL': ^{self.columnas}}")
            print(Style.RESET_ALL+"\n")
            
            try:
                    choice = int(input("INGRESE UNA OPCIÓN: "))

                    if choice == 1:
            
                        pattern = r"Adaptador de Ethernet Ethernet:"
                        
                        output = subprocess.check_output('ipconfig /all', encoding='oem')
                        
                        matches = list((re.finditer(pattern, output)))
                       
                        match = matches[0]
                        
                        start_index = match.end()
                        lines = output.splitlines()
                        
                        start_line = output[:start_index].count('\n')
                        desired_line_index = start_line + 7 - 1 

                        result_text = lines[desired_line_index]
                        
                        if result_text[-2:] == "no":
                            
                            self.enable_dhcp()
                            print("SE HA DESMARCADO LA TARJETA EXITOSAMENTE!!!")
                            time.sleep(2)
                            return
                        else:
                            
                            self.set_static_ip()
                            print("SE HA FIJADO LA TARJETA EXITOSAMENTE!!!")
                            time.sleep(2)
                            return
                    
                    elif choice == 2:
                        subprocess.call("cls", shell=True)
                        ip = input("Ingrese la ip que desea fijar: ")
                        netmask = self.get_netmask(ip)

                        if netmask:
                            self.set_static_ip(ip,netmask)
                            print("SE HA FIJADO LA TARJETA EXITOSAMENTE!!!")
                            time.sleep(2)
                            return

                    elif choice == 3:
                        return
                    
                        
            except Exception as e:
                    print("POR FAVOR INGRESE UNA OPCIÓN CORRECTA") 
                    time.sleep(1)   
                        

    def enable_dhcp(self):
        try:
            command = [
                "netsh", "interface", "ip", "set", "address",
                "Ethernet", "dhcp"
            ]
            subprocess.run(command, capture_output=True, text=True, check=True)
            print("DHCP habilitado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al habilitar DHCP, EL PUERTO ESTA DESCONECTADO")


    def get_netmask(self,ip):
        if not self.is_valid_ip(ip):
            return None

        
        if ip.startswith("192.168."):
            return "255.255.255.0"
        elif ip.startswith("10."):
            second_octet = int(ip.split('.')[1])
            if 104 <= second_octet <= 110:
                return "255.255.252.0"
            else:
                return None 
        else:
            return None
        

    def is_valid_ip(self,ip):
        
        ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
        
        match = ip_pattern.match(ip)
        if match:
            octets = list(map(int, match.groups()))
            return all(0 <= octet <= 255 for octet in octets)
        return False
                  

    def set_static_ip(self,ip = "192.168.1.53", mask = "255.255.255.0"):
        
        try:
            command = [
                "netsh", "interface", "ipv4", "set", "address",
                f"name=Ethernet", "static", ip, mask
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"Error al configurar la IP estática: {e}")
            print(f"Salida de error: {e.stderr}")



    def wait_for_device(ip, initial_wait=60, check_interval=10, timeout=300):
    
        print(f"Esperando {initial_wait} segundos para que el reinicio se complete...")
        time.sleep(initial_wait)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Comprobar conectividad usando ping
                if subprocess.call(['ping', '-c', '1', ip]) == 0:
                    print("Dispositivo está en línea.")
                    return True
            except Exception as e:
                print(f"Error al hacer ping: {e}")
            time.sleep(check_interval)  # Esperar entre intentos de comprobación
        print("Tiempo de espera agotado. El dispositivo no responde.")
        return False


    def cargar_backup(self):
        pass

    def establecer_hora(self):
        pass

    def compliance(self):
        pass

if __name__ == '__main__':
    script = Main()
    script.menu_principal()
