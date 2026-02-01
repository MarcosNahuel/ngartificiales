"""
Verificacion de datos: Tienda Nube API vs Dashboard
Periodo: 2025 y 2026
"""

import requests
import json
from datetime import datetime

# Configuracion API
API_BASE = "https://api.tiendanube.com/v1"
USER_ID = "2590356"
ACCESS_TOKEN = "ef6b2de9459410120bd24f9ef631aebbe00405f5"

HEADERS = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "NG Artificiales Dashboard (support@ngartificiales.com)",
    "Content-Type": "application/json"
}

def fetch_orders_2025_2026():
    """Obtener ordenes desde 2025-01-01"""
    all_orders = []
    page = 1

    while True:
        url = f"{API_BASE}/{USER_ID}/orders"
        params = {
            "page": page,
            "per_page": 200,
            "created_at_min": "2025-01-01"
        }

        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        orders = response.json()
        if not orders:
            break

        all_orders.extend(orders)
        print(f"  Pagina {page}: {len(orders)} ordenes")

        if len(orders) < 200:
            break
        page += 1

    return all_orders

def fetch_all_orders():
    """Obtener TODAS las ordenes (sin filtro)"""
    all_orders = []
    page = 1

    while True:
        url = f"{API_BASE}/{USER_ID}/orders"
        params = {"page": page, "per_page": 200}

        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        orders = response.json()
        if not orders:
            break

        all_orders.extend(orders)
        print(f"  Pagina {page}: {len(orders)} ordenes")

        if len(orders) < 200:
            break
        page += 1

    return all_orders

def fetch_products():
    """Obtener productos"""
    url = f"{API_BASE}/{USER_ID}/products"
    params = {"per_page": 200}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json() if response.status_code == 200 else []

def fetch_customers():
    """Obtener clientes"""
    url = f"{API_BASE}/{USER_ID}/customers"
    params = {"per_page": 200}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json() if response.status_code == 200 else []

def analyze_orders(orders, label=""):
    """Analizar ordenes"""
    total = 0
    by_month = {}
    by_status = {}

    for o in orders:
        # Total
        order_total = float(o.get('total', 0) or 0)
        total += order_total

        # Por mes
        created = o.get('created_at', '')
        if created:
            month = created[:7]  # YYYY-MM
            if month not in by_month:
                by_month[month] = {'orders': 0, 'total': 0}
            by_month[month]['orders'] += 1
            by_month[month]['total'] += order_total

        # Por estado
        status = o.get('payment_status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1

    return {
        'count': len(orders),
        'total': total,
        'by_month': by_month,
        'by_status': by_status
    }

def main():
    print("=" * 70)
    print("VERIFICACION DE DATOS: TIENDA NUBE API vs DASHBOARD")
    print("=" * 70)

    # 1. Obtener TODAS las ordenes
    print("\n[1] TODAS LAS ORDENES (historico completo)")
    print("-" * 50)
    all_orders = fetch_all_orders()
    all_analysis = analyze_orders(all_orders, "TODAS")

    print(f"\n  Total ordenes: {all_analysis['count']}")
    print(f"  Total ventas: ${all_analysis['total']:,.2f}")

    # 2. Obtener ordenes 2025+2026
    print("\n[2] ORDENES 2025 + 2026")
    print("-" * 50)
    orders_2025 = fetch_orders_2025_2026()
    analysis_2025 = analyze_orders(orders_2025, "2025+")

    print(f"\n  Total ordenes 2025+: {analysis_2025['count']}")
    print(f"  Total ventas 2025+: ${analysis_2025['total']:,.2f}")

    # 3. Desglose por mes
    print("\n[3] DESGLOSE POR MES (2025+2026)")
    print("-" * 50)
    for month in sorted(analysis_2025['by_month'].keys()):
        data = analysis_2025['by_month'][month]
        print(f"  {month}: {data['orders']} ordenes, ${data['total']:,.2f}")

    # 4. Productos y Clientes
    print("\n[4] PRODUCTOS Y CLIENTES")
    print("-" * 50)
    products = fetch_products()
    customers = fetch_customers()
    print(f"  Productos: {len(products)}")
    print(f"  Clientes: {len(customers)}")

    # 5. Estados de pago
    print("\n[5] ORDENES POR ESTADO DE PAGO (2025+2026)")
    print("-" * 50)
    for status, count in analysis_2025['by_status'].items():
        print(f"  {status}: {count}")

    # 6. Comparacion con Dashboard
    print("\n" + "=" * 70)
    print("COMPARACION CON DASHBOARD (data.json)")
    print("=" * 70)

    # Leer data.json
    try:
        with open('../dashboard/public/data.json', 'r', encoding='utf-8') as f:
            dashboard_data = json.load(f)

        dash_orders = dashboard_data['data_summary']['orders_count']
        dash_products = dashboard_data['data_summary']['products_count']
        dash_customers = dashboard_data['data_summary']['customers_count']
        dash_revenue = dashboard_data['descriptive']['kpis']['total_revenue']

        print(f"\n{'Metrica':<20} {'Dashboard':<20} {'API (todas)':<20} {'Match'}")
        print("-" * 70)
        print(f"{'Ordenes':<20} {dash_orders:<20} {all_analysis['count']:<20} {'OK' if dash_orders == all_analysis['count'] else 'DIFF'}")
        print(f"{'Productos':<20} {dash_products:<20} {len(products):<20} {'OK' if dash_products == len(products) else 'DIFF'}")
        print(f"{'Clientes':<20} {dash_customers:<20} {len(customers):<20} {'OK' if dash_customers == len(customers) else 'DIFF'}")
        print(f"{'Total Ventas':<20} ${dash_revenue:,.0f} ${all_analysis['total']:,.0f} {'OK' if abs(dash_revenue - all_analysis['total']) < 1 else 'DIFF'}")

    except Exception as e:
        print(f"Error leyendo data.json: {e}")

    print("\n" + "=" * 70)
    print("VERIFICACION COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    main()
