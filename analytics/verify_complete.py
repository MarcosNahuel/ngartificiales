"""
Verificacion COMPLETA: Tienda Nube API vs Dashboard
Incluye 2024 + 2025
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

# Configuracion API Tienda Nube
API_BASE = "https://api.tiendanube.com/v1"
USER_ID = "2590356"
ACCESS_TOKEN = "ef6b2de9459410120bd24f9ef631aebbe00405f5"

HEADERS = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "NG Artificiales Dashboard",
    "Content-Type": "application/json"
}

def fetch_all_orders():
    """Obtener TODAS las ordenes sin filtro"""
    all_orders = []
    page = 1

    print("\n[API] Obteniendo TODAS las ordenes...")

    while True:
        url = f"{API_BASE}/{USER_ID}/orders"
        params = {"page": page, "per_page": 200}

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code != 200:
                print(f"  Error: {response.status_code}")
                break
            orders = response.json()
            if not orders:
                break
            all_orders.extend(orders)
            print(f"  Pagina {page}: {len(orders)} ordenes")
            if len(orders) < 200:
                break
            page += 1
        except Exception as e:
            print(f"  Error: {e}")
            break

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
            print(f"  Pagina {page}: {len(products)} productos")
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
            print(f"  Pagina {page}: {len(customers)} clientes")
            if len(customers) < 200:
                break
            page += 1
        except:
            break

    return all_customers

def analyze_orders(orders):
    """Analizar ordenes detalladamente"""
    total_ventas = 0
    by_month = defaultdict(lambda: {"revenue": 0, "orders": 0})
    by_status = defaultdict(int)
    by_year = defaultdict(lambda: {"revenue": 0, "orders": 0})

    order_details = []

    for order in orders:
        # Total de la orden
        order_total = float(order.get('total', 0) or 0)
        total_ventas += order_total

        # Fecha
        created_at = order.get('created_at', '')
        order_id = order.get('id', 'N/A')
        status = order.get('status', 'unknown')

        by_status[status] += 1

        if created_at:
            try:
                if 'T' in created_at:
                    date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                else:
                    date = datetime.strptime(created_at[:10], '%Y-%m-%d')

                month_key = date.strftime('%Y-%m')
                year_key = date.strftime('%Y')

                by_month[month_key]["revenue"] += order_total
                by_month[month_key]["orders"] += 1

                by_year[year_key]["revenue"] += order_total
                by_year[year_key]["orders"] += 1

                order_details.append({
                    "id": order_id,
                    "date": date.strftime('%Y-%m-%d'),
                    "total": order_total,
                    "status": status
                })
            except Exception as e:
                print(f"  Error parseando fecha: {created_at} - {e}")

    return {
        'total_orders': len(orders),
        'total_ventas': total_ventas,
        'by_month': dict(sorted(by_month.items())),
        'by_year': dict(sorted(by_year.items())),
        'by_status': dict(by_status),
        'order_details': sorted(order_details, key=lambda x: x['date'])
    }

def load_dashboard_data():
    """Cargar datos del dashboard"""
    try:
        with open('../dashboard/public/data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        try:
            with open('D:/OneDrive/GitHub/ngartificiales/dashboard/public/data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando dashboard data: {e}")
            return None

def main():
    print("=" * 70)
    print("VERIFICACION COMPLETA: Tienda Nube API vs Dashboard")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # 1. Obtener datos de API
    orders = fetch_all_orders()
    products = fetch_products()
    customers = fetch_customers()

    if not orders:
        print("\n[ERROR] No se pudieron obtener ordenes de la API")
        return

    # 2. Analizar ordenes de API
    api_analysis = analyze_orders(orders)

    # 3. Cargar datos del dashboard
    dashboard_data = load_dashboard_data()

    print("\n" + "=" * 70)
    print("DATOS DE LA API (TIENDA NUBE)")
    print("=" * 70)

    print(f"\nMETRICAS GENERALES:")
    print(f"   Total Ordenes: {api_analysis['total_orders']}")
    print(f"   Total Ventas:  ${api_analysis['total_ventas']:,.2f}")
    print(f"   Ticket Prom:   ${api_analysis['total_ventas']/max(1, api_analysis['total_orders']):,.2f}")
    print(f"   Productos:     {len(products)}")
    print(f"   Clientes:      {len(customers)}")

    print(f"\nVENTAS POR ANO:")
    for year, data in api_analysis['by_year'].items():
        print(f"   {year}: ${data['revenue']:,.2f} ({data['orders']} ordenes)")

    print(f"\nVENTAS POR MES:")
    for month, data in api_analysis['by_month'].items():
        print(f"   {month}: ${data['revenue']:,.2f} ({data['orders']} ordenes)")

    print(f"\nORDENES POR ESTADO:")
    for status, count in api_analysis['by_status'].items():
        print(f"   {status}: {count}")

    # 4. Comparar con dashboard
    if dashboard_data:
        print("\n" + "=" * 70)
        print("COMPARACION CON DASHBOARD")
        print("=" * 70)

        dash_kpis = dashboard_data.get('descriptive', {}).get('kpis', {})
        dash_monthly = dashboard_data.get('descriptive', {}).get('monthly_sales', [])

        print(f"\n{'Metrica':<20} {'API':>15} {'Dashboard':>15} {'Diferencia':>15} {'Match?':>8}")
        print("-" * 75)

        # Ordenes
        api_orders = api_analysis['total_orders']
        dash_orders = dash_kpis.get('total_orders', 0)
        diff_orders = api_orders - dash_orders
        match_orders = "SI" if diff_orders == 0 else "NO"
        print(f"{'Ordenes':<20} {api_orders:>15} {dash_orders:>15} {diff_orders:>15} {match_orders:>8}")

        # Ventas
        api_ventas = api_analysis['total_ventas']
        dash_ventas = dash_kpis.get('total_revenue', 0)
        diff_ventas = api_ventas - dash_ventas
        match_ventas = "SI" if abs(diff_ventas) < 1 else "NO"
        print(f"{'Ventas Totales':<20} ${api_ventas:>13,.2f} ${dash_ventas:>13,.2f} ${diff_ventas:>13,.2f} {match_ventas:>8}")

        # Ticket promedio
        api_ticket = api_ventas / max(1, api_orders)
        dash_ticket = dash_kpis.get('avg_ticket', 0)
        diff_ticket = api_ticket - dash_ticket
        match_ticket = "SI" if abs(diff_ticket) < 1 else "NO"
        print(f"{'Ticket Promedio':<20} ${api_ticket:>13,.2f} ${dash_ticket:>13,.2f} ${diff_ticket:>13,.2f} {match_ticket:>8}")

        # Productos
        api_prods = len(products)
        dash_prods = dashboard_data.get('data_summary', {}).get('products_count', 0)
        diff_prods = api_prods - dash_prods
        match_prods = "SI" if diff_prods == 0 else "NO"
        print(f"{'Productos':<20} {api_prods:>15} {dash_prods:>15} {diff_prods:>15} {match_prods:>8}")

        # Clientes
        api_custs = len(customers)
        dash_custs = dashboard_data.get('data_summary', {}).get('customers_count', 0)
        diff_custs = api_custs - dash_custs
        match_custs = "SI" if diff_custs == 0 else "NO"
        print(f"{'Clientes':<20} {api_custs:>15} {dash_custs:>15} {diff_custs:>15} {match_custs:>8}")

        # Comparar por mes
        print(f"\nCOMPARACION POR MES:")
        print(f"{'Mes':<10} {'API Revenue':>15} {'Dashboard':>15} {'Diferencia':>15} {'Match?':>8}")
        print("-" * 65)

        dash_monthly_dict = {m['month']: m['revenue'] for m in dash_monthly}
        all_months = sorted(set(list(api_analysis['by_month'].keys()) + list(dash_monthly_dict.keys())))

        total_diff = 0
        for month in all_months:
            api_rev = api_analysis['by_month'].get(month, {}).get('revenue', 0)
            dash_rev = dash_monthly_dict.get(month, 0)
            diff = api_rev - dash_rev
            total_diff += abs(diff)
            match = "SI" if abs(diff) < 1 else "NO"
            print(f"{month:<10} ${api_rev:>13,.2f} ${dash_rev:>13,.2f} ${diff:>13,.2f} {match:>8}")

        print("-" * 65)
        print(f"{'TOTAL DIFF':<10} {' ':>15} {' ':>15} ${total_diff:>13,.2f}")

        # Resumen final
        print("\n" + "=" * 70)
        print("RESUMEN DE VERIFICACION")
        print("=" * 70)

        all_match = (diff_orders == 0 and abs(diff_ventas) < 1 and
                     diff_prods == 0 and diff_custs == 0)

        if all_match:
            print("\n[OK] TODOS LOS DATOS COINCIDEN PERFECTAMENTE")
        else:
            print("\n[WARN] HAY DIFERENCIAS:")
            if diff_orders != 0:
                print(f"   - Ordenes: diferencia de {diff_orders}")
            if abs(diff_ventas) >= 1:
                print(f"   - Ventas: diferencia de ${diff_ventas:,.2f}")
            if diff_prods != 0:
                print(f"   - Productos: diferencia de {diff_prods}")
            if diff_custs != 0:
                print(f"   - Clientes: diferencia de {diff_custs}")

    # 5. Guardar resultados
    output = {
        'timestamp': datetime.now().isoformat(),
        'api_data': {
            'total_orders': api_analysis['total_orders'],
            'total_sales': api_analysis['total_ventas'],
            'products': len(products),
            'customers': len(customers),
            'by_year': api_analysis['by_year'],
            'by_month': api_analysis['by_month'],
            'by_status': api_analysis['by_status']
        },
        'order_list': api_analysis['order_details']
    }

    with open('data/api_verification_complete.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Datos guardados en data/api_verification_complete.json")

if __name__ == "__main__":
    main()
