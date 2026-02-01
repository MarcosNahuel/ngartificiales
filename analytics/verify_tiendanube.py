"""
Verificación de datos: Tienda Nube API vs Dashboard
Período: 2025-01-01 hasta hoy (2026-01-09)
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

# Configuración API Tienda Nube
API_BASE = "https://api.tiendanube.com/v1"
USER_ID = "2590356"
ACCESS_TOKEN = "ef6b2de9459410120bd24f9ef631aebbe00405f5"

HEADERS = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "NG Artificiales Dashboard (support@ngartificiales.com)",
    "Content-Type": "application/json"
}

def fetch_orders_filtered(created_at_min=None, page=1, per_page=200):
    """Obtener órdenes con filtro de fecha"""
    url = f"{API_BASE}/{USER_ID}/orders"
    params = {"page": page, "per_page": per_page}

    if created_at_min:
        params["created_at_min"] = created_at_min

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        print(f"  Status: {response.status_code}")

        if response.status_code == 401:
            print("  [ERROR] Token inválido o expirado")
            return [], False
        elif response.status_code == 404:
            print("  [ERROR] Tienda no encontrada")
            return [], False

        response.raise_for_status()
        return response.json(), True
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] {e}")
        return [], False

def fetch_all_orders_2025_2026():
    """Obtener todas las órdenes desde 2025-01-01"""
    all_orders = []
    page = 1
    created_at_min = "2025-01-01"

    print(f"\n[API] Obteniendo órdenes desde {created_at_min}...")

    while True:
        orders, success = fetch_orders_filtered(created_at_min=created_at_min, page=page)

        if not success:
            print("\n[WARN] No se pudo conectar a la API")
            return None

        if not orders:
            break

        all_orders.extend(orders)
        print(f"  Página {page}: {len(orders)} órdenes")

        if len(orders) < 200:
            break
        page += 1

    return all_orders

def fetch_all_orders_complete():
    """Obtener TODAS las órdenes sin filtro"""
    all_orders = []
    page = 1

    print(f"\n[API] Obteniendo TODAS las órdenes...")

    while True:
        orders, success = fetch_orders_filtered(page=page)

        if not success:
            return None

        if not orders:
            break

        all_orders.extend(orders)
        print(f"  Página {page}: {len(orders)} órdenes")

        if len(orders) < 200:
            break
        page += 1

    return all_orders

def fetch_products():
    """Obtener productos"""
    url = f"{API_BASE}/{USER_ID}/products"
    all_products = []
    page = 1

    print("\n[API] Obteniendo productos...")

    while True:
        try:
            response = requests.get(url, headers=HEADERS, params={"page": page, "per_page": 200})
            if response.status_code != 200:
                break
            products = response.json()
            if not products:
                break
            all_products.extend(products)
            print(f"  Página {page}: {len(products)} productos")
            if len(products) < 200:
                break
            page += 1
        except:
            break

    return all_products

def fetch_customers():
    """Obtener clientes"""
    url = f"{API_BASE}/{USER_ID}/customers"
    all_customers = []
    page = 1

    print("\n[API] Obteniendo clientes...")

    while True:
        try:
            response = requests.get(url, headers=HEADERS, params={"page": page, "per_page": 200})
            if response.status_code != 200:
                break
            customers = response.json()
            if not customers:
                break
            all_customers.extend(customers)
            print(f"  Página {page}: {len(customers)} clientes")
            if len(customers) < 200:
                break
            page += 1
        except:
            break

    return all_customers

def analyze_orders(orders, period_label):
    """Analizar órdenes obtenidas"""
    if not orders:
        return None

    total_ventas = 0
    by_month = defaultdict(float)
    by_status = defaultdict(int)

    for order in orders:
        # Total
        order_total = float(order.get('total', 0) or 0)
        total_ventas += order_total

        # Por mes
        created_at = order.get('created_at', '')
        if created_at:
            try:
                if 'T' in created_at:
                    date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                else:
                    date = datetime.strptime(created_at[:10], '%Y-%m-%d')
                month_key = date.strftime('%Y-%m')
                by_month[month_key] += order_total
            except:
                pass

        # Por status
        status = order.get('status', 'unknown')
        by_status[status] += 1

    return {
        'period': period_label,
        'total_orders': len(orders),
        'total_ventas': total_ventas,
        'by_month': dict(sorted(by_month.items())),
        'by_status': dict(by_status)
    }

def main():
    print("=" * 70)
    print("VERIFICACIÓN: Tienda Nube API vs Dashboard")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Tienda ID: {USER_ID}")

    # 1. Obtener órdenes 2025-2026
    orders_2025 = fetch_all_orders_2025_2026()

    # 2. Si falla, intentar obtener todas las órdenes
    if orders_2025 is None:
        print("\n[INFO] Intentando obtener todas las órdenes sin filtro...")
        orders_all = fetch_all_orders_complete()

        if orders_all is None:
            print("\n" + "=" * 70)
            print("RESULTADO: No se pudo conectar a la API de Tienda Nube")
            print("=" * 70)
            print("\nPosibles causas:")
            print("  1. Token de acceso expirado o inválido")
            print("  2. Problemas de conexión")
            print("  3. La tienda no existe o fue desactivada")
            print("\nRecomendación: Verificar token en panel de Tienda Nube")
            return

        # Filtrar 2025 manualmente
        orders_2025 = []
        for order in orders_all:
            created_at = order.get('created_at', '')
            if created_at and created_at[:4] in ['2025', '2026']:
                orders_2025.append(order)

    # 3. Analizar resultados
    analysis = analyze_orders(orders_2025, "2025-2026")

    if not analysis:
        print("\n[WARN] No hay órdenes en el período 2025-2026")
        return

    # 4. Obtener productos y clientes
    products = fetch_products()
    customers = fetch_customers()

    # 5. Mostrar resultados
    print("\n" + "=" * 70)
    print("RESULTADOS DE LA API (DATOS REALES)")
    print("=" * 70)

    print(f"\nMETRICAS GENERALES:")
    print(f"   Periodo: 2025-01-01 a 2026-01-09")
    print(f"   Total Ordenes: {analysis['total_orders']}")
    print(f"   Total Ventas: ${analysis['total_ventas']:,.0f}")
    print(f"   Ticket Promedio: ${analysis['total_ventas']/max(1, analysis['total_orders']):,.0f}")

    if products:
        print(f"   Total Productos: {len(products)}")
    if customers:
        print(f"   Total Clientes: {len(customers)}")

    print(f"\nVENTAS POR MES:")
    for month, total in analysis['by_month'].items():
        print(f"   {month}: ${total:,.0f}")

    print(f"\nORDENES POR ESTADO:")
    for status, count in analysis['by_status'].items():
        print(f"   {status}: {count}")

    # 6. Guardar resultados
    output = {
        'timestamp': datetime.now().isoformat(),
        'period': '2025-01-01 to 2026-01-09',
        'metrics': {
            'total_orders': analysis['total_orders'],
            'total_sales': analysis['total_ventas'],
            'avg_ticket': analysis['total_ventas']/max(1, analysis['total_orders']),
            'total_products': len(products) if products else 0,
            'total_customers': len(customers) if customers else 0
        },
        'by_month': analysis['by_month'],
        'by_status': analysis['by_status']
    }

    with open('data/api_verification.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n[OK] Resultados guardados en data/api_verification.json")

    print("\n" + "=" * 70)
    print("COMPARACIÓN CON DASHBOARD")
    print("=" * 70)
    print("\nPara comparar:")
    print("  1. Revisar el dashboard en localhost:3000")
    print("  2. Comparar las métricas mostradas con estos valores")
    print("  3. Verificar que coincidan órdenes, ventas y clientes")

if __name__ == "__main__":
    main()
