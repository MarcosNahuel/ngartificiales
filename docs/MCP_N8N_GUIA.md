# Guía de Integración del MCP de n8n

## Descripción

Esta guía explica cómo configurar y utilizar el Model Context Protocol (MCP) de n8n en tu repositorio para automatizar workflows, gestionar credenciales y administrar tu instancia de n8n mediante Claude Code.

## ¿Qué es el MCP de n8n?

El MCP (Model Context Protocol) de n8n es una interfaz que permite a Claude Code interactuar directamente con tu instancia de n8n para:

- Crear, actualizar y gestionar workflows
- Administrar credenciales de forma segura
- Ejecutar y monitorear procesos
- Gestionar proyectos y usuarios
- Configurar variables de entorno
- Generar auditorías de seguridad

## Prerrequisitos

1. **Instancia de n8n activa**
   - n8n Cloud o n8n self-hosted
   - URL de acceso a la instancia
   - API key con permisos adecuados

2. **Claude Code instalado**
   - Con soporte para MCP servers

3. **Credenciales de n8n**
   - API Key generada desde tu instancia

## Configuración Inicial

### 1. Generar API Key en n8n

1. Accede a tu instancia de n8n
2. Ve a **Settings** → **API**
3. Genera una nueva API Key
4. Guarda la key de forma segura (no la compartas en repositorios)

### 2. Configurar MCP en tu Proyecto

Crea o actualiza el archivo de configuración del MCP (usualmente `.clauderc` o configuración de MCP):

```json
{
  "mcpServers": {
    "n8n-manager": {
      "command": "npx",
      "args": ["-y", "@n8n/mcp-server"],
      "env": {
        "N8N_API_KEY": "tu-api-key-aqui",
        "N8N_BASE_URL": "https://tu-instancia.n8n.cloud"
      }
    }
  }
}
```

### 3. Variables de Entorno (Recomendado)

Para mayor seguridad, utiliza variables de entorno:

```bash
# .env (NO COMMITAR ESTE ARCHIVO)
N8N_API_KEY=n8n_api_xxxxxxxxxxxxxxxxx
N8N_BASE_URL=https://tu-instancia.n8n.cloud
```

Actualiza la configuración MCP:

```json
{
  "mcpServers": {
    "n8n-manager": {
      "command": "npx",
      "args": ["-y", "@n8n/mcp-server"]
    }
  }
}
```

## Uso Básico

### Inicializar Conexión

Una vez configurado el MCP, Claude Code puede conectarse automáticamente. Si necesitas inicializar manualmente:

```
Inicializa la conexión con n8n usando la URL [tu-url] y la API key [tu-key]
```

### Operaciones con Workflows

#### Listar Workflows

```
Lista todos los workflows disponibles en mi instancia de n8n
```

#### Obtener Detalles de un Workflow

```
Muéstrame los detalles del workflow con ID [workflow-id]
```

#### Crear un Nuevo Workflow

```
Crea un workflow en n8n llamado "Proceso de Ventas" con los siguientes nodos:
- Webhook trigger
- HTTP Request para obtener datos
- Set para transformar datos
```

#### Actualizar un Workflow

```
Actualiza el workflow [workflow-id] para agregar un nodo de Email
```

#### Activar/Desactivar Workflows

```
Activa el workflow [workflow-id]
Desactiva el workflow [workflow-id]
```

### Gestión de Credenciales

#### Ver Esquema de Credenciales

```
Muéstrame qué campos necesito para crear credenciales de tipo "githubApi"
```

#### Crear Credenciales

```
Crea credenciales de tipo "slackOAuth2Api" con los siguientes datos:
- name: "Slack Production"
- clientId: [tu-client-id]
- clientSecret: [tu-secret]
```

**IMPORTANTE**: Nunca incluyas credenciales sensibles directamente en el código o documentación. Usa variables de entorno.

### Gestión de Proyectos (Enterprise)

```
Lista todos los proyectos en n8n
Crea un nuevo proyecto llamado "Marketing Automation"
```

### Gestión de Usuarios

```
Lista todos los usuarios de la instancia
Crea un nuevo usuario con email usuario@ejemplo.com y rol global:member
```

### Variables de Entorno (Enterprise)

```
Lista todas las variables configuradas
Crea una variable con key "API_ENDPOINT" y value "https://api.ejemplo.com"
```

### Auditoría de Seguridad

```
Genera una auditoría de seguridad de mi instancia de n8n, enfocada en credenciales y base de datos
```

## Ejemplos Prácticos

### Ejemplo 1: Crear Workflow de Procesamiento de Emails

```
Crea un workflow en n8n llamado "Procesador de Emails" que:
1. Use un trigger de Email (IMAP)
2. Filtre emails con asunto que contenga "pedido"
3. Extraiga datos del cuerpo del email
4. Envíe los datos a una Google Sheet
5. Envíe un email de confirmación
```

### Ejemplo 2: Monitorear Ejecuciones

```
Muéstrame las últimas 20 ejecuciones del workflow [workflow-id]
Muéstrame los detalles de la ejecución [execution-id]
```

### Ejemplo 3: Gestión de Tags

```
Lista todos los tags disponibles
Crea un tag llamado "producción"
Asigna el tag "producción" al workflow [workflow-id]
```

## Estructura de un Workflow en JSON

Cuando necesites crear workflows complejos, usa esta estructura:

```json
{
  "name": "Nombre del Workflow",
  "nodes": [
    {
      "name": "Trigger",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "mi-webhook"
      }
    }
  ],
  "connections": {
    "Trigger": {
      "main": [
        [
          {
            "node": "Siguiente Nodo",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Mejores Prácticas

### Seguridad

1. **Nunca hardcodees API keys** en el código
2. Usa variables de entorno para información sensible
3. Agrega `.env` al `.gitignore`
4. Genera API keys con los permisos mínimos necesarios
5. Rota las API keys regularmente
6. Realiza auditorías periódicas

### Organización

1. Usa nombres descriptivos para workflows
2. Utiliza tags para categorizar workflows
3. Documenta la funcionalidad de cada workflow
4. Mantén los workflows modulares y reutilizables

### Desarrollo

1. Prueba workflows en un entorno de desarrollo primero
2. Usa proyectos (si tienes Enterprise) para separar ambientes
3. Haz backups de workflows importantes
4. Monitorea ejecuciones regularmente

## Troubleshooting

### Error: "Client not initialized"

**Problema**: La conexión con n8n no se ha establecido.

**Solución**:
```
Inicializa la conexión con n8n usando mi URL y API key configuradas
```

### Error: "Invalid API key"

**Problema**: La API key es incorrecta o ha expirado.

**Solución**:
1. Verifica que la API key sea correcta
2. Genera una nueva API key en n8n
3. Actualiza la configuración del MCP

### Error: "Workflow not found"

**Problema**: El ID del workflow no existe.

**Solución**:
```
Lista todos los workflows para obtener los IDs correctos
```

### Error: "Insufficient permissions"

**Problema**: La API key no tiene permisos suficientes.

**Solución**:
1. Ve a n8n Settings → API
2. Genera una nueva API key con más permisos
3. Actualiza tu configuración

## Limitaciones por Tipo de Licencia

### Features que Requieren n8n Enterprise

- Gestión de proyectos (`list-projects`, `create-project`)
- Variables de entorno (`list-variables`, `create-variable`)
- Algunas funciones avanzadas de auditoría

### Features Disponibles en Todas las Versiones

- Gestión de workflows
- Gestión de credenciales
- Listado de ejecuciones
- Gestión de tags
- Operaciones básicas de usuarios

## Referencias

- [Documentación oficial de n8n](https://docs.n8n.io)
- [n8n API Documentation](https://docs.n8n.io/api/)
- [MCP Protocol](https://modelcontextprotocol.io)
- [n8n Community](https://community.n8n.io)

## Archivo .gitignore Recomendado

Asegúrate de incluir en tu `.gitignore`:

```gitignore
# n8n credentials
.env
.env.local
.env.*.local

# MCP configuration with secrets
.clauderc.local

# n8n local data
.n8n/
```

## Siguientes Pasos

1. Configura tu instancia de n8n
2. Genera y guarda tu API key
3. Configura el MCP en tu proyecto
4. Prueba la conexión listando workflows
5. Comienza a automatizar tus procesos

---

**Nota de Seguridad**: Esta guía contiene ejemplos con placeholders. Reemplaza todos los valores de ejemplo con tus credenciales reales, pero NUNCA las commitees a git. Usa variables de entorno y herramientas de gestión de secretos.
