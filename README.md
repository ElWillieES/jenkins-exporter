# Jenkins Exporter

[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)

## Introducción

Jenkins Exporter es un proyecto desarrollado con Python y PyCharm, con el objetivo de poder descargar datos de **Jenkins**, como por ejemplo los datos de usuarios y pipelines.

Estos datos pueden posteriormente importarse en una base de datos para su análisis, pudiendo utilizarse para diferentes propósitos, como el inventariado, el análisis de uso, o la obtención de diferentes métricas.

Este repo se ha creado para complementar el Post [Jenkins - Exportando datos de Jenkins con jenkins-exporter](https://elwillie.es/2022/12/06/python-exportando-datos-de-jenkins-con-jenkins-exporter/) del Blog [El Willie - The Geeks invaders](https://elwillie.es). También tiene fines didácticos, en temas como Python, Docker, y Jenkins.

Para la ejecución sobre MiniKube te puede interesar leer los Posts [Introducción a MiniKube e instalación en Windows 11](https://elwillie.es/2022/11/15/kubernetes-introduccion-a-minikube-e-instalacion-en-windows-11/) y [Administración fácil y rápida con K9s](https://elwillie.es/2022/11/15/kubernetes-administracion-facil-y-rapida-con-k9s/).

Si quieres saber cómo instalar Jenkins puedes leer el Post [Jenkins – Instalar y configurar Jenkins sobre Ubuntu 22](https://elwillie.es/2022/12/04/jenkins-instalar-y-configurar-sobre-ubuntu-22/).

**Puedes apoyar mi trabajo haciendo "☆ Star" en el repo o nominarme a "GitHub Star"**. Muchas gracias :-) 

[![GitHub Star](https://img.shields.io/badge/GitHub-Nominar_a_star-yellow?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://stars.github.com/nominate/)


## Arquitectura de la Solución

Se trata de un programa de línea de comandos en Python, que accede a la API de Jenkins, para descargar los datos que necesita, generando ficheros CSV en la carpeta ./export/ para que puedan ser utilizados para un posterior análisis y tratamiento.

### Información que se desea obtener

Se desea obtener la siguiente información de la API de Jenkins:

* Usuarios
* Jobs (Pipelines) e histórico de ejecuciones  (Builds) con su resultado
* Roles (Global Roles y Project Roles) y pertenencia de usuarios a Roles (Plugin Role-Based Authentication Strategy)


### Ejemplos de configuración y ejecución

Es un programa de línea de comandos, que espera recibir dos parámetros:

* **Acción que se desea realizar**. Básicamente es indicar qué datos deseamos exportar, que se generarán en la **carpeta ./export/**. En función de qué datos necesitemos, y de qué Plugins tengamos instalados (ej: Role-Based Authentication Strategy), seleccionaremos las acciones que necesitemos. Si queremos exportar varios datos (ej: usuarios y pipelines) bastará con ejecutarlo dos veces, en cada una especificando una acción.
* **Fichero de configuración**. Proporciona los datos de conexión en un fichero JSON con un formato determinado ubicado en la **carpeta ./config/** (datos de conexión a Jenkins).

El fichero JSON de configuración para la conexión a Jenkins (ej: **./config/jenkins_conn_elwillie.json**) será similar al siguiente, en el que especificaremos la URL de nuestro Jenkins, un usuario (con permisos suficientes) y su API Token. 
```
{
  "jenkins-site": "elwillie",
  "jenkins-protocol": "http",
  "jenkins-domain-name": "jenkins.willie.lan",
  "jenkins-user": "elwillie",
  "jenkins-token": "1216da6c750471fa731b13510e335at51f"
}
```

**Las carpetas ./config/ y ./export/ están añadidas al fichero .gitignore**, para evitar que se puedan subir tanto credenciales como datos a los repos remotos de Git, por privacidad, como por intentar mantener el repo limpio (evitar subir exportaciones de diferentes pruebas, que no aportan valor en el repo remoto). Sin embargo, si se incluiran al construir nuestra imagen Docker en local, lo que nos permitirá utilizar nuestras configuraciones tanto para ejecutar en local con Python como en local con Docker, Docker Compose, o Kubernetes.

Si tenemos varias granjas de Jenkins, podemos crear múltiples ficheros de configuración (los que necesitemos) y ejecutar varias veces el programa (ej: Jenkins de Test y Jenkins de Prod).

A continuación se muestra un ejemplo de uso.

```
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_users
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_plugins
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_jobs
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_rbas_global_roles
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_rbas_project_roles
```


## Otros detalles de interés

Si te interesa aprender Python, tienes disponibles los siguientes [cursos gratuitos de Python en Edube - OpenEDG](https://edube.org/):

* Python Essentials 1
* Python Essentials 2
* Python Advanced 1 – OOP
* Python Advanced 2 – Best Practices and Standardization
* Python Advanced 3 – GUI Programming
* Python Advanced 4 – RESTful APIs
* Python Advanced 5 – File Processing

Otro recurso muy interesante es [Real Python](https://realpython.com/), donde podrás encontrar tutoriales, baterías de preguntas para ponerte a prueba (quizzes), etc.

En mi Blog personal ([El Willie - The Geeks invaders](https://elwillie.es)) y en mi perfil de GitHub, encontrarás más información sobre mi, y sobre los contenidos de tecnología que comparto con la comunidad.

[![Web](https://img.shields.io/badge/GitHub-ElWillieES-14a1f0?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/ElWillieES)

# Git

## Repositorio

Este repo se puede clonar desde GitHub utilizando este [enlace HTTP](https://github.com/ElWillieES/jenkins-exporter.git). 

A continuación se muestra el comando git clone usando SSH en lugar de HTTP.

```sh
git clone git@github.com:ElWillieES/jenkins-exporter.git
```

## Estructura de Ramas: Trunk Based Development (TBD)

* **Ramas permanentes**. Utilizaremos **master** como rama principal.
* **Ramas temporales o efímeras**. Utilizaremos **feature/xxx** (nueva característica) y/o **hotfix/xxx** (corregir un bug crítico urgente), que nacen de la rama principal y mezclan de nuevo sobre ella mediante Merge Request.
* **Gestión de Releases**. Para cada Release generaremos una etiqueta (tag) del tipo **release/a.b.c**.

En la descripción de las ramas de feature y hotfix, se especificará el ID de la tarea o issue asociada, por ejemplo:

```git
feature/3813
hotfix/2262
```

Si necesitáramos varias ramas para una misma tarea, añadiremos un número secuencial para evitar la colisión:

```git
feature/3813-1
feature/3813-2
```

## Commits Semanticos: icónos y prefijos

Como recomendación y buena práctica, el título para los Commits y de las Merge Request, pueden empezar con un icono y un prefijo, seguido de dos puntos y de un mensaje corto que comience por un verbo imperativo (ej: add, change, fix, remove, etc.). Por ejemplo:

```git
✨ feat(backend): add support for users having multiple suscriptions
```

Prefijos:

```git
feat: Nueva característica
fix: Corrección a un error
doc: Documentación
style: Cambios de formato (guía de estilo)
refactor: Renombrar una variable, simplificar un método, etc…
test: Añadir o modificar tests
chore: Rareas rutinarias, como modificar el .gitignore, etc…
```

Iconos:

```git
💄 Cosmetic
🎨 Improve format / structure
🛠/🐛 Fix
✨ Feature
🚑 Hotfix
📝 Doc
🚀 Release
♻ Refactor
🐳 Devops
☸ Kubernetes
🧪 Arquitectura de tests
✅ Añadir un Test
✔ Hacer que un test pase
💩 Ñapas
🏗 Architectural changes
🤡 Mocks
💚 Fixing Build
📈 Analiltycs
🌐 Localizations
😒 Chore
💫 Animations & Transitions
♿ Accesibility
🚧 Feature work in progress
🚀 Launch a new build
```

# Docker - Ejecución en local

## Con Docker

Se puede ejecutar la aplicación en local con Docker. 

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran:
* Cómo **crear una imagen** en local con docker build. Antes de construir la imagen, borramos el contenido de app/export/, por si tuviéramos ficheros de pruebas de ejecución, para no engordar y ensuciar la imagen.
* Cómo listar las imágenes que tenemos disponibles en local. Deberá aparecer la que acabamos de crear.
* **Cómo ejecutar un contenedor con nuestra imagen, con el comando deseado**. Como nuestra aplicación es de línea de comandos, se incluyen varios ejemplos, en cada uno de los cuales se indica como parámetro el fichero de configuración que necesita (debe existir en la carpeta /usr/src/app/config/ del contenedor) y la acción a realizar (hay varias posibles, según los datos que queramos exportar, que dependerá de los Plugins que tengamos instalados). Como se van a generar los ficheros de exportación en la carpeta del contenedor /usr/src/app/export, y los contenedores son efímeros, **utilizamos un volumen sobre /usr/src/app/export para que los datos persistan** y además podamos acceder a los ficheros que hemos generado. Es necesario especificar la ruta absoluta del host (ajustarla con la de cada uno).  

```shell
rm app/export/*

docker build -t jenkins-exporter .
docker images

docker run -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export --rm jenkins-exporter python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_users
docker run -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export --rm jenkins-exporter python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_plugins
docker run -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export --rm jenkins-exporter python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_jobs
docker run -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export --rm jenkins-exporter python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_rbas_global_roles
docker run -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export --rm jenkins-exporter python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_rbas_project_roles

```

Podemos arrancar una sesión interativa de Bash sobre un Contendor con nuestra imagen Docker, para de este modo, analizar mejor incidencias y problemas que nos puedan surgir, depurar, etc. Suele ser bastante útil.

En el siguiente ejemplo, arrancamos una sesión bash sobre un contenedor con nuestra imagen y un volumen mapeando la carpeta export de nuestro portátil con la del contenedor, ejecutamos jenkins-exporter, y salimos del contenedor.

```shell
docker run --rm -v d:/code/elwillie/jenkins-exporter/app/export:/usr/src/app/export -it jenkins-exporter /bin/bash
python jenkins-exporter.py -c jenkins_conn_elwillie.json -a export_all_jenkins_users
exit
```


## Con Docker Compose

El siguiente comando ejecutado en la raíz del Proyecto, muestra cómo compilar (es decir, construir la imagen Docker) y ejecutar jenkins-exporter con Docker Compose, así como la forma de poder comprobar los logs de su ejecución.

Si observamos el fichero **docker-compose.yml**, podemos ver que incluye varias ejecuciones de jenkins-exporter, para las diferentes exportaciones que queremos realizar. Además, utiliza un volumen mapeando la carpeta export de nuestro portátil con la del contenedor, para así poder acceder a los datos generados desde nuestro portátil, después de su ejecución. 

```shell
docker-compose -f docker-compose.yml up --build -d
docker-compose -f docker-compose.yml logs
```


# Kubernetes - Ejecución en local (MiniKube)

Se puede ejecutar la aplicación en local con Kubernetes, si tienes instalado MiniKube. Para ampliar información te puede interesar leer [Introducción a MiniKube e instalación en Windows 11](https://elwillie.es/2022/11/15/kubernetes-introduccion-a-minikube-e-instalacion-en-windows-11/)

Los manifiestos de Kubernetes, están en la carpeta kube, y son los siguientes:

* **exporter-ns.yml**. Para la creación del namespace exporter, donde desplegaremos nuestra aplicación.
* **jenkins-exporter-conf.vol**. Permite crear un Volumen, es decir, un PersistentVolume de tipo hostPath y un PersistentVolumeClaim, que mapearemos a nuestro Job para tener persistencia entre ejecuciones. Los datos persistirán dentro del almacenamiento de MiniKube (nos podemos conectar con minikube ssh para verlos). 
* **jenkins-exporter-conf.yml**. Permite crear un ConfigMap, que contiene los ficheros JSON de configuración que necesitamos para conectarnos a Jenkins. Los mapearemos a los contenedores sobre el directorio /usr/src/app/config sobrescribiendo los ficheros que pudiera haber en la imagen original.
* **jenkins-exporter-job.yml**. Consiste en un Job que incluye un contenedor para cada comando que queremos ejecutar, y mapea tanto el ConfigMap anterior como el volumen persistente.

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran cómo tagear la Imagen Docker para subirla al Registry local de MiniKube.

```shell
docker tag jenkins-exporter localhost:5000/jenkins-exporter
docker push localhost:5000/jenkins-exporter
```

Realizado esto, en la ventana Terminal de PyCharm, podemos ejecutar los siguientes comandos para aplicar los manifiestos en nuestro Cluster de MiniKube (namespace y Job), y consultar el Log de ejecución del Job que acabamos de crear y ejecutar (la salida del Log, será igual a cuando lo ejecutamos en Docker o directamente en PyCharm).

```shell
cd kube
kubectl apply -f exporter-ns.yml
kubectl apply -f jenkins-exporter-vol.yml
kubectl get PersistentVolume -n exporter -o wide
kubectl get PersistentVolumeClaim -n exporter -o wide

kubectl apply -f jenkins-exporter-conf.yml
kubectl apply -f jenkins-exporter-job.yml

kubectl get jobs -n exporter
kubectl describe jobs jenkins-exporter -n exporter

kubectl logs job/jenkins-exporter -c jenkins-exporter-jenkins-users -n exporter
kubectl logs job/jenkins-exporter -c jenkins-exporter-jenkins-plugins -n exporter
kubectl logs job/jenkins-exporter -c jenkins-exporter-jenkins-jobs -n exporter
kubectl logs job/jenkins-exporter -c jenkins-exporter-jenkins-rbas-global-roles -n exporter
kubectl logs job/jenkins-exporter -c jenkins-exporter-jenkins-rbas-project-roles -n exporter
```

Si queremos ver o incluso editar el ConfigMap, podemos utilizar el siguiente comando.

```shell
kubectl edit configmap jenkins-exporter-conf -n exporter
```

También podemos crear un nuevo contenedor al vuelo, con nuestra imagen, con una sesión bash a la que conectarnos para poder depurar y hacer pruebas.

```shell
kubectl run -it --rm jenkins-exporter --image=localhost:5000/jenkins-exporter -n exporter -- /bin/bash
```

Si necesitamos volver a crear el Job, tendremos que eliminarlo antes, para lo cual podemos utilizar un comando como el siguiente.

```shell
kubectl delete job jenkins-exporter -n exporter
```

Al finalizar podemos eliminar el namespace de Kubernetes, para eliminar todos los recursos y dejar "la casa limpia".

```shell
kubectl delete ns exporter
```


# Contactos

| Nombre        | Posición en el Proyecto | Email                                                |
|---------------|-------------------------|------------------------------------------------------|
| **El Willie** | Brownie Manager         | [elwillieES@gmail.com](mailto:elwillieES@gmail.com)  |
