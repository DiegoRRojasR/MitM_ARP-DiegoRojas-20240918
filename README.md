# Informe Técnico: Ataque de Interceptación Man-in-the-Middle (MitM)

## Video (máx. 8 minutos)

[![Ver video en YouTube](https://img.youtube.com/vi/1FxaVcs4J8Y/0.jpg)](https://youtu.be/1FxaVcs4J8Y)


## I-) Introducción y Objetivos del Script.
El presente documento detalla el funcionamiento y la implementación del script ATAQUE.py, el cual es un script desarrollado en Python utilizando la librería Scapy para realizar un envenenamiento de tablas ARP (ARP Spoofing). El objetivo principal de esta herramienta es interceptar el tráfico de red entre un dispositivo víctima y su puerta de enlace predeterminada, actuando como un intermediario invisible. Al enviar respuestas ARP falsificadas, el script logra que la víctima asocie la dirección IP del router con la dirección MAC del atacante, permitiendo que toda la información enviada hacia internet pase primero por la interfaz del atacante para su análisis y registro.
<img width="829" height="600" alt="Screenshot 2026-02-05 220720" src="https://github.com/user-attachments/assets/68b01035-cf7b-46e4-8303-09590c1c0a71" />

## II-) Análisis de la Topología y Direccionamiento.
La infraestructura de red utilizada para esta demostración consta de un segmento de red local bajo el direccionamiento 10.24.9.0/24, donde todos los dispositivos están interconectados a través de un Switch de acceso. El nodo central es el Router (R1) con la IP 10.24.9.1, el cual sirve como Gateway para la salida de datos.
<img width="1070" height="780" alt="Screenshot 2026-02-05 220800" src="https://github.com/user-attachments/assets/7a9962cd-6473-4207-9049-d93c9155b515" />

El equipo atacante, operando con **Kali Linux**, ha sido configurado estáticamente con la IP **10.24.9.18** y posee la dirección física real **50:0a:1e:00:03:00**.
<img width="827" height="599" alt="Screenshot 2026-02-05 220849" src="https://github.com/user-attachments/assets/1336edf1-8692-4b84-9343-6ee05cd05076" />

Por último, la víctima, identificada en el sistema como **"POBRE ALMA EN PENA"**, utiliza un sistema **Windows 7** con la IP **10.24.9.20** y una dirección física **50-bb-52-00-04-00**.
<img width="854" height="723" alt="Screenshot 2026-02-05 221022" src="https://github.com/user-attachments/assets/c968c1cc-3d52-47b6-bc0c-8d96fcc9abc9" />

### Resumen de direccionamiento
| Equipo | SO | IP | MAC | Rol |
|---|---|---|---|---|
| Router (R1) | Router | 10.24.9.1 | (MAC del router) | Gateway |
| Atacante | Kali Linux | 10.24.9.18 | 50:0a:1e:00:03:00 | MITM |
| Víctima | Windows 7 | 10.24.9.20 | 50-bb-52-00-04-00 | Host |

## III-) Parámetros del Ataque y Funcionamiento.
El script **ATAQUE.py** se basa en la generación de paquetes ARP (con un código de operación **op=2**) que se mandan cada **dos segundos** para impedir que el sistema operativo modifique o expire la caché de los dispositivos. Los parámetros importantes son el **hwsrc**, que es donde se inserta la dirección MAC auténtica del atacante (**50:0a:1e:00:03:00**) para obligar al conmutador a desviar las tramas hacia su puerto físico; el **psrc** (IP que el atacante quiere reemplazar); y el **pdst** (IP de destino del paquete).

<img width="281" height="92" alt="Screenshot 2026-02-11 100022" src="https://github.com/user-attachments/assets/b5df90c2-59b0-4a84-a738-d66be740f0db" />

<img width="280" height="88" alt="Screenshot 2026-02-05 221442" src="https://github.com/user-attachments/assets/80c115aa-de1a-44cd-9b17-b154082759c2" />

El **try** ejecuta un ataque en ambas direcciones, mandando paquetes al mismo tiempo a la víctima y al router para garantizar que el tráfico de subida y bajada sea capturado completamente.

## IV-) Requisitos de Ejecución y Validación.
Para que el ataque sea efectivo y no resulte en una simple denegación de servicio (DoS), es indispensable que el sistema atacante tenga activado el **IP Forwarding** en el kernel de Linux. Esto se logra mediante el comando:

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```
<img width="535" height="83" alt="Screenshot 2026-02-05 221610" src="https://github.com/user-attachments/assets/ad3286ab-6d19-4056-a0e3-29a802c8d5d3" />

Lo que permite que el Kali Linux reenvíe los paquetes capturados a su destino real después de haberlos inspeccionado. El éxito del ataque se valida visualmente en la máquina víctima ejecutando el comando arp -a, donde se debe observar que la dirección IP del Gateway (10.24.9.1) ahora aparece vinculada a la dirección física del atacante en lugar de la original del router.

<img width="866" height="718" alt="Screenshot 2026-02-05 222040" src="https://github.com/user-attachments/assets/159198f1-29e1-4762-a7de-72ea421c1e67" />

### V-) Medidas de Mitigación y Recomendaciones.
Para protegerse contra este tipo de ataques de capa 2, es necesario aplicar medidas de seguridad activa en los aparatos de red. En contextos con switches administrables, el Dynamic ARP Inspection (DAI) es el método más eficaz. 
Este procedimiento intercepta y verifica cada paquete ARP para asociarlos una base de datos confiable, que suele ser creada por DHCP Snooping. Otras acciones incluyen la implementación de Port Security para restringir las direcciones MAC permitidas por puerto, y sobre todo, el empleo extendido de protocolos cifrados (SSH, HTTPS, TLS), los cuales aseguran que aún en caso de que un atacante consiga interceptar los paquetes, el contenido del intercambio siga estando cifrado y no pueda ser leído por terceros



