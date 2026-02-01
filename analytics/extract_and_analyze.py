"""
NG Artificiales - Extracción de datos y análisis completo
Autor: Traid Business
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configuración API Tienda Nube
API_BASE = "https://api.tiendanube.com/v1"
USER_ID = "2590356"
ACCESS_TOKEN = "ef6b2de9459410120bd24f9ef631aebbe00405f5"

HEADERS = {
    "Authentication": f"bearer {ACCESS_TOKEN}",
    "User-Agent": "NG Artificiales Dashboard (support@ngartificiales.com)",
    "Content-Type": "application/json"
}

def fetch_orders(page=1, per_page=200):
    """Obtener órdenes de Tienda Nube"""
    url = f"{API_BASE}/{USER_ID}/orders"
    params = {"page": page, "per_page": per_page}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders: {e}")
        return []

def fetch_products(page=1, per_page=200):
    """Obtener productos de Tienda Nube"""
    url = f"{API_BASE}/{USER_ID}/products"
    params = {"page": page, "per_page": per_page}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []

def fetch_customers(page=1, per_page=200):
    """Obtener clientes de Tienda Nube"""
    url = f"{API_BASE}/{USER_ID}/customers"
    params = {"page": page, "per_page": per_page}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching customers: {e}")
        return []

def fetch_all_data():
    """Obtener todos los datos paginados"""
    all_orders = []
    all_products = []
    all_customers = []

    # Obtener todas las órdenes
    print("Obteniendo órdenes...")
    page = 1
    while True:
        orders = fetch_orders(page=page)
        if not orders:
            break
        all_orders.extend(orders)
        print(f"  Página {page}: {len(orders)} órdenes")
        if len(orders) < 200:
            break
        page += 1

    # Obtener todos los productos
    print("\nObteniendo productos...")
    page = 1
    while True:
        products = fetch_products(page=page)
        if not products:
            break
        all_products.extend(products)
        print(f"  Página {page}: {len(products)} productos")
        if len(products) < 200:
            break
        page += 1

    # Obtener todos los clientes
    print("\nObteniendo clientes...")
    page = 1
    while True:
        customers = fetch_customers(page=page)
        if not customers:
            break
        all_customers.extend(customers)
        print(f"  Página {page}: {len(customers)} clientes")
        if len(customers) < 200:
            break
        page += 1

    print(f"\n[OK] Total: {len(all_orders)} ordenes, {len(all_products)} productos, {len(all_customers)} clientes")

    return all_orders, all_products, all_customers

def generate_sample_data():
    """Generar datos de muestra realistas para NG Artificiales"""
    np.random.seed(42)

    # Productos basados en el catálogo real
    products = [
        {"id": 1, "name": "Combo Baitcast Premium", "category": "Señuelos", "subcategory": "Combos", "price": 19900, "stock": 45, "cost": 12000},
        {"id": 2, "name": "Combo Trolling Pro", "category": "Señuelos", "subcategory": "Combos", "price": 18500, "stock": 38, "cost": 11000},
        {"id": 3, "name": "Combo Spinning Elite", "category": "Señuelos", "subcategory": "Combos", "price": 17800, "stock": 52, "cost": 10500},
        {"id": 4, "name": "Señuelo Mojarra Natural", "category": "Señuelos", "subcategory": "Mojarra", "price": 14500, "stock": 120, "cost": 8500},
        {"id": 5, "name": "Señuelo Mojarra Gold", "category": "Señuelos", "subcategory": "Mojarra", "price": 15200, "stock": 98, "cost": 9000},
        {"id": 6, "name": "Señuelo Canibal Red", "category": "Señuelos", "subcategory": "Canibal", "price": 15800, "stock": 85, "cost": 9300},
        {"id": 7, "name": "Señuelo Canibal Black", "category": "Señuelos", "subcategory": "Canibal", "price": 15800, "stock": 72, "cost": 9300},
        {"id": 8, "name": "Señuelo TNT Explosive", "category": "Señuelos", "subcategory": "TNT", "price": 16500, "stock": 65, "cost": 9800},
        {"id": 9, "name": "Señuelo Extreme Hunter", "category": "Señuelos", "subcategory": "Extreme", "price": 17200, "stock": 48, "cost": 10200},
        {"id": 10, "name": "Señuelo Turbo Fast", "category": "Señuelos", "subcategory": "Turbo", "price": 14800, "stock": 110, "cost": 8700},
        {"id": 11, "name": "Señuelo Morena Classic", "category": "Señuelos", "subcategory": "Morena", "price": 13700, "stock": 95, "cost": 8000},
        {"id": 12, "name": "Señuelo Cascarudo Pro", "category": "Señuelos", "subcategory": "Cascarudo", "price": 14200, "stock": 88, "cost": 8300},
        {"id": 13, "name": "Señuelo Tabano Strike", "category": "Señuelos", "subcategory": "Tabano", "price": 15500, "stock": 76, "cost": 9100},
        {"id": 14, "name": "Señuelo Caimán Monster", "category": "Señuelos", "subcategory": "Caimán", "price": 18900, "stock": 35, "cost": 11200},
        {"id": 15, "name": "Termo Stanley 1L", "category": "Outdoor", "subcategory": "Térmicos", "price": 19500, "stock": 60, "cost": 11500},
        {"id": 16, "name": "Termo Stanley 750ml", "category": "Outdoor", "subcategory": "Térmicos", "price": 17800, "stock": 75, "cost": 10500},
        {"id": 17, "name": "Vaso Térmico NG", "category": "Outdoor", "subcategory": "Térmicos", "price": 13900, "stock": 150, "cost": 8200},
        {"id": 18, "name": "Cuchillo Pesca Pro", "category": "Outdoor", "subcategory": "Cuchillos", "price": 16500, "stock": 42, "cost": 9700},
        {"id": 19, "name": "Cuchillo Táctico NG", "category": "Outdoor", "subcategory": "Cuchillos", "price": 18200, "stock": 28, "cost": 10800},
        {"id": 20, "name": "Cuchillo Bowie Classic", "category": "Outdoor", "subcategory": "Cuchillos", "price": 19800, "stock": 22, "cost": 11700},
        {"id": 21, "name": "Linterna Eco LED", "category": "Outdoor", "subcategory": "Linternas", "price": 13700, "stock": 85, "cost": 8000},
        {"id": 22, "name": "Linterna D3 Tactical", "category": "Outdoor", "subcategory": "Linternas", "price": 15900, "stock": 55, "cost": 9400},
        {"id": 23, "name": "Linterna A1 Pro", "category": "Outdoor", "subcategory": "Linternas", "price": 17500, "stock": 40, "cost": 10300},
        {"id": 24, "name": "Linterna Scubaglow", "category": "Outdoor", "subcategory": "Linternas", "price": 19200, "stock": 25, "cost": 11300},
        {"id": 25, "name": "Linterna Campglow", "category": "Outdoor", "subcategory": "Linternas", "price": 14500, "stock": 68, "cost": 8500},
        {"id": 26, "name": "Linterna Carglow USB", "category": "Outdoor", "subcategory": "Linternas", "price": 16200, "stock": 48, "cost": 9500},
        {"id": 27, "name": "Kit Pesca Principiante", "category": "Señuelos", "subcategory": "Kits", "price": 24500, "stock": 30, "cost": 14500},
        {"id": 28, "name": "Kit Pesca Profesional", "category": "Señuelos", "subcategory": "Kits", "price": 45000, "stock": 15, "cost": 27000},
        {"id": 29, "name": "Caja Organizadora XL", "category": "Outdoor", "subcategory": "Accesorios", "price": 8500, "stock": 95, "cost": 5000},
        {"id": 30, "name": "Bolso Pesca Impermeable", "category": "Outdoor", "subcategory": "Accesorios", "price": 22000, "stock": 35, "cost": 13000},
        {"id": 31, "name": "Red de Pesca Premium", "category": "Outdoor", "subcategory": "Accesorios", "price": 12500, "stock": 50, "cost": 7400},
        {"id": 32, "name": "Anzuelos Variados Pack", "category": "Señuelos", "subcategory": "Accesorios", "price": 4500, "stock": 200, "cost": 2600},
    ]

    # Provincias de Argentina con pesos basados en población y actividad de pesca
    provinces = [
        ("Buenos Aires", 0.35), ("CABA", 0.12), ("Córdoba", 0.10), ("Santa Fe", 0.08),
        ("Mendoza", 0.06), ("Entre Ríos", 0.05), ("Corrientes", 0.04), ("Chaco", 0.03),
        ("Misiones", 0.03), ("Neuquén", 0.03), ("Río Negro", 0.02), ("Chubut", 0.02),
        ("Santa Cruz", 0.01), ("Tierra del Fuego", 0.01), ("La Pampa", 0.02),
        ("San Luis", 0.01), ("San Juan", 0.01), ("Tucumán", 0.01)
    ]

    # Métodos de pago
    payment_methods = ["Mercado Pago", "Transferencia", "Tarjeta Crédito", "Tarjeta Débito", "Efectivo"]
    payment_weights = [0.45, 0.25, 0.15, 0.10, 0.05]

    # Estados de orden
    order_statuses = ["completed", "pending", "cancelled", "processing", "shipped"]
    status_weights = [0.65, 0.15, 0.05, 0.08, 0.07]

    # Generar 18 meses de datos (desde Jul 2023 a Dic 2024)
    start_date = datetime(2023, 7, 1)
    end_date = datetime(2024, 12, 31)

    orders = []
    customers_data = []
    order_id = 1000
    customer_id = 1

    # Patrones estacionales (pesca más activa en primavera/verano argentino)
    seasonal_multiplier = {
        1: 1.3, 2: 1.2, 3: 1.1, 4: 0.9, 5: 0.7, 6: 0.6,
        7: 0.65, 8: 0.7, 9: 0.85, 10: 1.0, 11: 1.2, 12: 1.4
    }

    # Tendencia de crecimiento mensual
    growth_rate = 1.02  # 2% mensual

    current_date = start_date
    base_daily_orders = 3

    while current_date <= end_date:
        # Calcular órdenes del día con estacionalidad y crecimiento
        months_elapsed = (current_date.year - start_date.year) * 12 + (current_date.month - start_date.month)
        growth_factor = growth_rate ** months_elapsed
        seasonal_factor = seasonal_multiplier[current_date.month]

        # Más ventas los fines de semana
        weekend_factor = 1.4 if current_date.weekday() >= 5 else 1.0

        # Eventos especiales (Black Friday, Hot Sale, etc.)
        special_factor = 1.0
        if current_date.month == 11 and 20 <= current_date.day <= 30:  # Black Friday
            special_factor = 2.5
        elif current_date.month == 5 and 10 <= current_date.day <= 15:  # Hot Sale
            special_factor = 2.0
        elif current_date.month == 12 and 15 <= current_date.day <= 24:  # Navidad
            special_factor = 1.8

        expected_orders = base_daily_orders * growth_factor * seasonal_factor * weekend_factor * special_factor
        daily_orders = max(0, int(np.random.poisson(expected_orders)))

        for _ in range(daily_orders):
            # Seleccionar productos (1-4 productos por orden)
            num_products = np.random.choice([1, 2, 3, 4], p=[0.45, 0.35, 0.15, 0.05])
            order_products = np.random.choice(products, size=num_products, replace=False)

            # Calcular total
            quantities = [np.random.randint(1, 3) for _ in range(num_products)]
            subtotal = sum(p["price"] * q for p, q in zip(order_products, quantities))

            # Descuentos (10% probabilidad de descuento)
            discount = 0
            if np.random.random() < 0.10:
                discount = subtotal * np.random.choice([0.05, 0.10, 0.15, 0.20])

            # Envío (gratis > $30000)
            shipping = 0 if subtotal > 30000 else np.random.choice([2500, 3500, 4500])

            total = subtotal - discount + shipping

            # Cliente
            province, _ = provinces[np.random.choice(len(provinces), p=[p[1] for p in provinces])]
            is_new_customer = np.random.random() < 0.4  # 40% nuevos

            if is_new_customer:
                cust = {
                    "id": customer_id,
                    "email": f"cliente{customer_id}@email.com",
                    "name": f"Cliente {customer_id}",
                    "province": province,
                    "first_order": current_date.isoformat(),
                    "total_orders": 1,
                    "total_spent": total
                }
                customers_data.append(cust)
                customer_id += 1
            else:
                # Cliente existente
                if customers_data:
                    existing = np.random.choice(customers_data)
                    existing["total_orders"] += 1
                    existing["total_spent"] += total
                    cust = existing
                else:
                    continue

            # Hora de compra (picos 10-12 y 20-22)
            hour = np.random.choice(range(24), p=[
                0.01, 0.005, 0.005, 0.005, 0.005, 0.01,  # 0-5
                0.02, 0.03, 0.05, 0.08, 0.09, 0.08,      # 6-11
                0.06, 0.05, 0.04, 0.04, 0.05, 0.06,      # 12-17
                0.07, 0.08, 0.10, 0.09, 0.05, 0.03       # 18-23
            ])
            order_datetime = current_date.replace(hour=hour, minute=np.random.randint(0, 60))

            order = {
                "id": order_id,
                "created_at": order_datetime.isoformat(),
                "customer_id": cust["id"],
                "customer_name": cust["name"],
                "customer_province": province,
                "products": [{"id": p["id"], "name": p["name"], "category": p["category"],
                             "price": p["price"], "quantity": q, "cost": p["cost"]}
                            for p, q in zip(order_products, quantities)],
                "subtotal": subtotal,
                "discount": discount,
                "shipping": shipping,
                "total": total,
                "payment_method": np.random.choice(payment_methods, p=payment_weights),
                "status": np.random.choice(order_statuses, p=status_weights),
                "items_count": sum(quantities)
            }
            orders.append(order)
            order_id += 1

        current_date += timedelta(days=1)

    print(f"[OK] Generados {len(orders)} ordenes y {len(customers_data)} clientes")

    return orders, products, customers_data

def save_data(orders, products, customers, output_dir):
    """Guardar datos en archivos JSON"""
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    with open(f"{output_dir}/products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    with open(f"{output_dir}/customers.json", "w", encoding="utf-8") as f:
        json.dump(customers, f, ensure_ascii=False, indent=2)

    print(f"[OK] Datos guardados en {output_dir}/")

if __name__ == "__main__":
    print("=" * 60)
    print("NG Artificiales - Extracción de Datos")
    print("=" * 60)

    # Intentar obtener datos reales
    print("\n[API] Intentando conectar con Tienda Nube API...")
    orders, products, customers = fetch_all_data()

    # Si no hay datos reales, generar datos de muestra
    if not orders:
        print("\n[WARN] No se pudieron obtener datos de la API")
        print("[DATA] Generando datos de muestra realistas...")
        orders, products, customers = generate_sample_data()

    # Guardar datos
    output_dir = os.path.dirname(os.path.abspath(__file__)) + "/data"
    save_data(orders, products, customers, output_dir)

    print("\n[OK] Extraccion completada!")
