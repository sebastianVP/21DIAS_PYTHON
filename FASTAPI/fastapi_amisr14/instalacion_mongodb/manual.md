🧠 MANUAL DE INSTALACIÓN DE MONGODB EN UBUNTU 22.04 (JAMMY)
🧹 1. Eliminar versiones antiguas (si existen)

Si tu sistema ya tenía versiones previas de MongoDB, elimínalas para evitar conflictos:

sudo apt-get purge mongodb mongodb-clients mongodb-server mongodb-server-core mongodb-org*
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb


(Si no habías instalado MongoDB antes, puedes saltarte este paso.)

🔑 2. Importar la clave pública GPG del repositorio oficial de MongoDB
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor


Esto descarga y registra la firma que garantiza que los paquetes provienen del repositorio oficial.

📦 3. Agregar el repositorio de MongoDB 7.0

Crea el archivo de lista del repositorio:

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

⚙️ 4. Actualizar e instalar MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org


Esto instalará los siguientes paquetes:

mongod → el servicio principal de base de datos

mongos → router de base de datos (usado en clusters)

mongosh → shell moderno de MongoDB

Herramientas administrativas (mongostat, mongotop, etc.)

▶️ 5. Iniciar y habilitar el servicio MongoDB

Inicia el servicio:

sudo systemctl start mongod


Habilita el inicio automático al encender el sistema:

sudo systemctl enable mongod


Comprueba que esté corriendo correctamente:

sudo systemctl status mongod


Deberías ver algo como:

Active: active (running)

🧪 6. Verificar la instalación

Abre el shell de MongoDB:

mongosh


Si ves un prompt así:

test>


✅ ¡MongoDB está funcionando correctamente!

Para salir, escribe:

exit

🗃️ 7. Rutas importantes

Archivos de configuración: /etc/mongod.conf

Datos almacenados: /var/lib/mongodb

Logs: /var/log/mongodb/mongod.log

🧭 8. (Opcional) Instalar MongoDB Compass (Interfaz gráfica)

Si deseas ver tus bases de datos y colecciones de forma visual:

sudo snap install mongodb-compass


Luego ejecútalo con:

mongodb-compass


Y conéctate usando:

mongodb://localhost:27017