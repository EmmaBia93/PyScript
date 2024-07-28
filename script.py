from colorama import Fore, Style, init, Back
import subprocess
import shutil
import re
import time
from icmplib import ping
from scp import SCPClient
from halo import Halo
import easygui
from dotenv import load_dotenv
import os
import paramiko

class Main:
    
    def __init__(self) -> None:
        init(autoreset=True)

        self.f_clock = [
                        '\U0001F550',  # 🕐 - Reloj a las 12:00
                        '\U0001F551',  # 🕑 - Reloj a la 1:00
                        '\U0001F552',  # 🕒 - Reloj a las 2:00
                        '\U0001F553',  # 🕓 - Reloj a las 3:00
                        '\U0001F554',  # 🕔 - Reloj a las 4:00
                        '\U0001F555',  # 🕕 - Reloj a las 5:00
                        '\U0001F556',  # 🕖 - Reloj a las 6:00
                        '\U0001F557',  # 🕗 - Reloj a las 7:00
                        '\U0001F558',  # 🕘 - Reloj a las 8:00
                        '\U0001F559',  # 🕙 - Reloj a las 9:00
                        '\U0001F55A',  # 🕚 - Reloj a las 10:00
                        '\U0001F55B',  # 🕛 - Reloj a las 11:00
                    ]



        self.f_moon = [
                    '\U0001F311',
                    '\U0001F312',
                    '\U0001F313',
                    '\U0001F314',
                    '\U0001F315',
                    '\U0001F316',
                    '\U0001F317',
                    '\U0001F318'
                    ]
        self.running = True
        size = shutil.get_terminal_size()
        self.columnas = size.columns
        # Emojis en Unicode
        self.advertencia = '\u26A0'  # ⚠️
        self.error = '\u274C'        # ❌
        self.exito = '\u2705'        # ✅
        self.lapiz = '\U0001F4DD'    #  
        self.burbuja = '\U0001F5E8'
        self.reloj = '\U000023F3'

    def menu_principal(self):
        dic_functions = {
            1: self.ping,
            2: self.marcar_desmarcar,
            3: self.cargar_backup,
            4: self.establecer_hora,
            5: self.compliance
        }
        while self.running:
            subprocess.call('cls',shell=True)
            
            txt_menu = "( MENU PRINCIPAL )"
            print('\r' + Fore.BLACK + Back.RED + f"{txt_menu:-^{self.columnas}}" + Style.RESET_ALL + "\n")

            options = [
            "[1] PING",
            "[2] MARCAR O DESMARCAR LA TARJETA",
            "[3] CARGAR BACKUP",
            "[4] ESTABLECER HORA",
            "[5] COMPLIANCE",
            "[6] SALIR"
                        ]

            # Encuentra el largo máximo de las opciones
            max_length = max(len(option) for option in options)

            # Calcula el espacio adicional necesario para centrar las opciones
            padding = ((self.columnas+10) - max_length) // 2
            color = Fore.BLUE
            for option in options:
                print(f"{color}{' ' * padding}{option}\n")
           
            try:
                choice = input(" "+self.lapiz+" "+Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " "+Fore.RED)
                if choice.strip().isdigit():
                    choice = int(choice)
                    if choice in dic_functions:
                        dic_functions[choice]()
                    elif choice == 6:
                        self.running = False
                    else:
                        
                        print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)
                        time.sleep(1)
                else:
                    print('\n'+ self.advertencia+ Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL) 
                    time.sleep(1)
                        
            except EOFError:
                pass    



  
  

    def ping(self):

        self.ping_running = True
        
        while True:
            subprocess.call("cls", shell=True)
            ips = {1:'192.168.1.20',2:'192.168.88.1',3:'192.168.1.100'}
            print('\r' +Fore.BLACK+Back.RED+f"{"( PING )":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            
            options = [
            "[1] ANTENA",
            "[2] UBIQUITI",
            "[3] FW",
            "[4] OTRA IP",
            "[5] VOLVER AL MENU PRINCIPAL"
            
                        ]


            max_length = max(len(option) for option in options)

            
            padding = (self.columnas+10 - max_length) // 2

            color = Fore.BLUE
            for option in options:
                print(f"{color}{' ' * padding}{option}\n")

           
            
            try:
                choice = int(input(" "+self.lapiz+" "+Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " "+Fore.RED))

                if choice in ips:
                   proceso = subprocess.Popen(['ping', ips[choice], '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True,encoding='oem')
                   if proceso:
                    subprocess.call("cls", shell=True)
                    while self.ping_running:
                        output = proceso.stdout.readline()
                        if output:
                            print(Fore.GREEN + output.strip()+Style.RESET_ALL)
                        
                elif choice == 4:
                        subprocess.call("cls", shell=True)
                        print('\r' +Fore.BLACK+Back.RED+f"{"( PING )":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
                        ip = input(" "+self.burbuja+" "+Fore.GREEN+" INGRESE LA IP PARA REALIZAR EL PING: " + Style.RESET_ALL)
                        proceso = subprocess.Popen(['ping', ip, '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True,encoding='oem')
                        if proceso:
                            subprocess.call("cls", shell=True)
                            while self.ping_running:
                                output = proceso.stdout.readline()
                                if output:
                                    print(Fore.GREEN + output.strip()+Style.RESET_ALL)
                    
                elif choice == 5:
                
                        return
                
                else:
                   
                    print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)
                    time.sleep(1) 
            
                
            
            except ValueError as e:
                    print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL) 
                    time.sleep(1)
            except KeyboardInterrupt:
                self.ping_running = False
            finally:
                if not self.ping_running:
                    proceso.terminate()  # Asegurarse de terminar el proceso de ping
                    proceso.wait()       # Esperar a que el proceso termine completamente
                    spinner = Halo(text=Fore.CYAN+"Esperando..."+Style.RESET_ALL,
                                    spinner={
                                        'interval':100,
                                        'frames':self.f_clock
                                    },
                                    color="red")
                    print("\n\n"+self.advertencia+" "+ Fore.YELLOW +" Presione ENTER para volver al menu principal"+Style.RESET_ALL)
                    spinner.start()
                   
                    input()
                    spinner.stop()
                    return  # Regresar al menú principal
            
    
       

    def marcar_desmarcar(self):

        while True:
            subprocess.call("cls", shell=True)
            print('\r' +Fore.BLACK+Back.RED+f"{"( TARJETA DE RED )":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            
            options = [
                "[1] FIJAR/DESMARCAR",
                "[2] IP PARA FIJAR",
                "[3] VOLVER AL MENU PRINCIPAL"
                
                ]
            
            max_length = max(len(option) for option in options)

            
            padding = (self.columnas+10 - max_length) // 2

            color = Fore.BLUE
            for option in options:
                print(f"{color}{' ' * padding}{option}\n")    
        
            
            try:
                    choice = int(input(" "+self.lapiz+" "+Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " "+Fore.RED))

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
                            time.sleep(2)
                            return
                        else:
                            
                            if self.set_static_ip():
                                print("\n\n"+self.exito+" "+Fore.GREEN+" SE HA FIJADO LA TARJETA EXITOSAMENTE!!!"+Style.RESET_ALL)
                                time.sleep(2)
                                return
                    
                    elif choice == 2:
                        subprocess.call("cls", shell=True)
                        ip=input(" "+self.burbuja+" "+Fore.GREEN+" INGRESE LA IP CON LA QUE DESEA FIJAR LA TARJETA DE RED: " + Style.RESET_ALL)
                        netmask = self.get_netmask(ip)

                        if netmask:
                            if self.set_static_ip(ip,netmask):
                                print("\n\n"+self.exito+" "+Fore.GREEN+" SE HA FIJADO LA TARJETA EXITOSAMENTE!!!"+Style.RESET_ALL)
                                time.sleep(2)
                                return
                            

                    elif choice == 3:
                        return
                    
                    else:
                        print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)  
                        time.sleep(1)

            except Exception as e:
                    print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)
                    time.sleep(1)   
                        

    def enable_dhcp(self):
        try:
            command = [
                "netsh", "interface", "ip", "set", "address",
                "Ethernet", "dhcp"
            ]
            subprocess.run(command, capture_output=True, text=True, check=True)
            print("\n"+self.exito+" "+Fore.GREEN+" EL DHCP FUE HABILITADO CORRECTAMENTE"+Style.RESET_ALL)
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            print("\n"+self.error+Fore.RED+" ERROR AL HABILITAR EL DHCP, VERIFIQUE LA CONEXION")
            time.sleep(1)

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
            subprocess.run(command, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print("\n"+self.error+Fore.RED+" ERROR AL ESTABLECER LA IP ESTÁTICA")
            time.sleep(1)
            return False



    def wait_for_device(self,ip='192.168.1.20', initial_wait=15, check_interval=10, timeout=30):
        subprocess.call('cls', shell=True)
        print("\n")
        segundos  = initial_wait

        spinner = Halo(text=Fore.YELLOW+f"Esperando {initial_wait} segundos para intentar conexión...",
                       spinner={
                           'interval':100,
                           'frames':self.f_moon
                       })
        spinner.start()
        while segundos >= 0:
        # Actualizar el texto del spinner con el tiempo restante
            spinner.text = Fore.YELLOW+f"Esperando {segundos} segundos para intentar conexión..."
            time.sleep(1)  # Esperar 1 segundo
            segundos -= 1  # Decrementar el tiempo
        
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Comprobar conectividad usando ping
                request = ping(ip,timeout=1,count=1)
                
                if request.is_alive:
                    print("\n"+self.exito+" "+Fore.GREEN+"Dispositivo está en línea.")
                    spinner.stop()
                    return True
            except Exception as e:
                print(f"Error al hacer ping: {e}")
            segundos=check_interval  
            print("\n"+self.error+ " " +Fore.RED+ "NO HUBO RESPUESTA AL PING...")
            while segundos >= 0:
             # Actualizar el texto del spinner con el tiempo restante
                spinner.text = Fore.YELLOW+f"Esperando {segundos} segundos"
                time.sleep(1)  # Esperar 1 segundo
                segundos -= 1 

        spinner.stop()
        print("\n"+self.error + " "+ Fore.RED +"Tiempo de espera agotado. El dispositivo no responde.")
        input(Fore.RED +"Presione ENTER para continuar...")
        return False

    def execute_commands(self,ip, port, username, password, commands:list):
        
        try:
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Aceptar la clave del host automáticamente
            ssh.connect(ip, port=port, username=username, password=password)

            for command in commands:
                stdin, stdout, stderr = ssh.exec_command(command)
                
            ssh.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


    def select_file(self):
        archivo_path = easygui.fileopenbox(
            title="Seleccionar archivo",
            filetypes=["*.cfg"]
        )
        
        return archivo_path


    def transfer_file(self,ip, local_path,username="ubnt",password="ubnt"):
        remote_path='/var/tmp/system.cfg'
        load_dotenv()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(local_path, remote_path)
            
            print("\n"+self.exito+Fore.GREEN+"ARCHIVO TRANSFERIDO CON EXITO!!!.")
            ssh.close()
            return True
        except Exception as e:
            print("\n"+self.error+Fore.GREEN+f"Error al transferir el archivo: {e}")
            return False


    def transfer_file_if_possible(self):
        path = self.select_file()
        if path:
            print('\U00002709'+"  "+Fore.MAGENTA + "SE VA A TRANSFERIR EL ARCHIVO SELECCIONADO...")
            if self.transfer_file():
                print(self.exito+" "+Fore.GREEN, "SE HA TRANSFERIDO EL ARCHIVO CON EXITO!!!")
                return True
        return False

    def restart_device(self,ip, port, username, password):
        print(Fore.YELLOW, "SE VA A REINICIAR EL DISPOSITIVO PARA APLICAR LOS CAMBIOS")
        request = self.execute_commands(
            ip=ip,
            port=port,
            username=username,
            password=password,
            commands=['/tmp/system.cfg -w -p /etc/', '/usr/etc/rc.d/rc.softrestart save']
        )
        return request

    def cargar_backup(self):
        while True:
            subprocess.call("cls", shell=True)
            print('\r' +Fore.BLACK+Back.RED+f"{"( BACKUP )":-^{self.columnas}}"+Style.RESET_ALL+"\n\n")
            options = [
                "[1] ANTENAS AIRMAX",
                "[2] ANTENAS AC",
                "[3] VOLVER AL MENU PRINCIPAL"
                
                ]
            max_length = max(len(option) for option in options)

            
            padding = (self.columnas+10 - max_length) // 2

            color = Fore.BLUE
            for option in options:
                print(f"{color}{' ' * padding}{option}\n")
            
            try:
                    choice = int(input(" "+self.lapiz+" "+Back.BLUE+ Fore.BLACK +" INGRESE UNA OPCIÓN:"+ Style.RESET_ALL + " "+Fore.RED))
                    if choice in [1,2]:
                        print(Fore.BLUE +"PROBANDO LA CONEXIÓN CON EL DISPOSITIVO...")
                        if self.wait_for_device():
                            if self.transfer_file_if_possible():
                                password ='ubnt'
                                ip = '192.168.1.20'
                                port = 22
                                username = 'ubnt'
                                if self.restart_device(ip, port, username, password):
                                    print('\U0001F513'+" "+Fore.CYAN+"SE PASARA HACER EL COMPLIANCE...")                   

                            else:
                                print("Se salio sin dar el path")
                                time.sleep(2)

                    elif choice==3:
                        return
                    else:
                        print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)  
                        time.sleep(1)

            except Exception as e:
                    print('\n'+self.advertencia + Fore.YELLOW+"  POR FAVOR INGRESE UNA OPCIÓN CORRECTA"+Style.RESET_ALL)
                    time.sleep(1)  



    


    def sync_time(self):
        try:
            subprocess.run('w32tm /resync', check=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            return False




    def is_w32tm_service_running(self):
        try:
            result = subprocess.run(['sc', 'query', 'w32time'], capture_output=True, text=True, check=True)
            output = result.stdout

            if "RUNNING" in output:
                return True
            else:
                return False
        except:
            return False


    def start_w32tm_service(self):
        try:
            subprocess.run(['net', 'start', 'w32time'], check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            
        except subprocess.CalledProcessError as e:
            
            pass


    def establecer_hora(self):
        subprocess.call("cls", shell=True)
        print('\r' +Fore.BLACK+Back.RED+f"{" HORA ":-^{self.columnas}}"+Style.RESET_ALL+"\n")
        spinner = Halo(text=Fore.CYAN+" SE ESTABLECERÁ LA HORA",
                       spinner={
                           'interval':100,
                           'frames':self.f_clock
                       })
        spinner.start()
        if self.is_w32tm_service_running():
            if self.sync_time():
                spinner.stop()
                print(self.exito+" "+Fore.GREEN+"SE ESTABLECIÓ CORRECTAMENTE LA HORA, PRESIONE ENTER PARA CONTINUAR")
            else:
                spinner.stop()
                print(self.error+ " " +Fore.RED+"NO SE PUDO ESTABLECER LA HORA, PRESIONE ENTER PARA CONTINUAR")
        else:
            self.start_w32tm_service()
            if self.sync_time():
                spinner.stop()
                print(self.exito+" "+Fore.GREEN+"SE ESTABLECIÓ CORRECTAMENTE LA HORA, PRESIONE ENTER PARA CONTINUAR")
            else:
                spinner.stop()
                print(self.error+ " " +Fore.RED+"NO SE PUDO ESTABLECER LA HORA, PRESIONE ENTER PARA CONTINUAR")
        

        input()


    def compliance(self):
        pass

if __name__ == '__main__':
    script = Main()
    script.menu_principal()
