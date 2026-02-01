"""
NG Artificiales - Analisis Completo de Datos
Incluye: Descriptivo, ML, Regresion, Forecasting
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Cargar datos
def load_data():
    with open('data/orders.json', 'r', encoding='utf-8') as f:
        orders = json.load(f)
    with open('data/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    with open('data/customers.json', 'r', encoding='utf-8') as f:
        customers = json.load(f)
    return orders, products, customers

# ============================================
# 1. ANALISIS DESCRIPTIVO
# ============================================
def descriptive_analysis(orders, products, customers):
    print("\n" + "="*60)
    print("1. ANALISIS DESCRIPTIVO")
    print("="*60)

    # Convertir ordenes a DataFrame
    orders_data = []
    for o in orders:
        try:
            created = o.get('created_at', '')
            if created:
                if 'T' in created:
                    dt = datetime.fromisoformat(created.replace('+0000', '+00:00').replace('Z', '+00:00'))
                else:
                    dt = datetime.strptime(created, '%Y-%m-%d')
            else:
                continue

            total = float(o.get('total', 0) or 0)
            subtotal = float(o.get('subtotal', 0) or 0)
            shipping = float(o.get('shipping_cost_customer', 0) or 0)
            discount = float(o.get('discount', 0) or 0)

            customer = o.get('customer', {}) or {}
            province = o.get('billing_province', '') or customer.get('default_address', {}).get('province', 'Desconocido')

            products_in_order = o.get('products', []) or []
            items_count = sum(p.get('quantity', 1) for p in products_in_order)

            orders_data.append({
                'id': o.get('id'),
                'date': dt.date(),
                'datetime': dt,
                'hour': dt.hour,
                'day_of_week': dt.weekday(),
                'month': dt.month,
                'year': dt.year,
                'total': total,
                'subtotal': subtotal,
                'shipping': shipping,
                'discount': discount,
                'payment_status': o.get('payment_status', 'unknown'),
                'gateway': o.get('gateway_name', o.get('gateway', 'unknown')),
                'province': province,
                'items_count': items_count,
                'customer_id': customer.get('id'),
                'storefront': o.get('storefront', 'unknown')
            })
        except Exception as e:
            continue

    df_orders = pd.DataFrame(orders_data)

    if df_orders.empty:
        print("[WARN] No hay ordenes para analizar")
        return {}

    # KPIs Generales
    total_revenue = df_orders['total'].sum()
    total_orders = len(df_orders)
    avg_ticket = df_orders['total'].mean()
    total_customers = len(customers)
    unique_customers = df_orders['customer_id'].nunique()

    print(f"\n[KPIs GENERALES]")
    print(f"  Ingresos Totales: ${total_revenue:,.0f} ARS")
    print(f"  Total Ordenes: {total_orders}")
    print(f"  Ticket Promedio: ${avg_ticket:,.0f} ARS")
    print(f"  Clientes Unicos: {unique_customers}")
    print(f"  Clientes Registrados: {total_customers}")

    # Ventas por mes
    df_orders['month_year'] = df_orders['datetime'].dt.to_period('M')
    monthly_sales = df_orders.groupby('month_year').agg({
        'total': 'sum',
        'id': 'count'
    }).rename(columns={'id': 'orders'})

    print(f"\n[VENTAS POR MES]")
    for idx, row in monthly_sales.iterrows():
        print(f"  {idx}: ${row['total']:,.0f} ({int(row['orders'])} ordenes)")

    # Top productos
    products_sold = defaultdict(lambda: {'quantity': 0, 'revenue': 0, 'name': ''})
    for o in orders:
        for p in o.get('products', []) or []:
            pid = p.get('product_id') or p.get('id')
            qty = p.get('quantity', 1)
            price = float(p.get('price', 0) or 0)
            name = p.get('name', f'Producto {pid}')

            if isinstance(name, dict):
                name = name.get('es', name.get('en', str(name)))

            products_sold[pid]['quantity'] += qty
            products_sold[pid]['revenue'] += price * qty
            products_sold[pid]['name'] = name

    # Ordenar por revenue
    top_products = sorted(products_sold.items(), key=lambda x: x[1]['revenue'], reverse=True)[:10]

    print(f"\n[TOP 10 PRODUCTOS]")
    for i, (pid, data) in enumerate(top_products, 1):
        name = data['name'][:40] if len(data['name']) > 40 else data['name']
        print(f"  {i}. {name}: ${data['revenue']:,.0f} ({data['quantity']} uds)")

    # Ventas por provincia
    province_sales = df_orders.groupby('province')['total'].sum().sort_values(ascending=False).head(10)
    print(f"\n[VENTAS POR PROVINCIA]")
    for prov, total in province_sales.items():
        print(f"  {prov}: ${total:,.0f}")

    # Metodos de pago
    payment_methods = df_orders.groupby('gateway')['total'].sum().sort_values(ascending=False)
    print(f"\n[METODOS DE PAGO]")
    for method, total in payment_methods.items():
        pct = (total / total_revenue) * 100
        print(f"  {method}: ${total:,.0f} ({pct:.1f}%)")

    # Ventas por dia de la semana
    days = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    weekday_sales = df_orders.groupby('day_of_week')['total'].sum()
    print(f"\n[VENTAS POR DIA]")
    for dow, total in weekday_sales.items():
        print(f"  {days[dow]}: ${total:,.0f}")

    # Horas pico
    hourly_sales = df_orders.groupby('hour')['id'].count().sort_values(ascending=False).head(5)
    print(f"\n[HORAS PICO]")
    for hour, count in hourly_sales.items():
        print(f"  {hour}:00 - {hour+1}:00: {count} ordenes")

    # Guardar resultados
    results = {
        'kpis': {
            'total_revenue': float(total_revenue),
            'total_orders': int(total_orders),
            'avg_ticket': float(avg_ticket),
            'unique_customers': int(unique_customers),
            'total_customers': int(total_customers)
        },
        'monthly_sales': [
            {'month': str(idx), 'revenue': float(row['total']), 'orders': int(row['orders'])}
            for idx, row in monthly_sales.iterrows()
        ],
        'top_products': [
            {'id': pid, 'name': data['name'], 'revenue': float(data['revenue']), 'quantity': int(data['quantity'])}
            for pid, data in top_products
        ],
        'province_sales': [
            {'province': prov, 'revenue': float(total)}
            for prov, total in province_sales.items()
        ],
        'payment_methods': [
            {'method': method, 'revenue': float(total), 'percentage': float((total/total_revenue)*100)}
            for method, total in payment_methods.items()
        ],
        'weekday_sales': [
            {'day': days[dow], 'day_index': int(dow), 'revenue': float(total)}
            for dow, total in weekday_sales.items()
        ],
        'hourly_distribution': [
            {'hour': int(hour), 'orders': int(count)}
            for hour, count in df_orders.groupby('hour')['id'].count().items()
        ]
    }

    return results, df_orders

# ============================================
# 2. ANALISIS DE REGRESION
# ============================================
def regression_analysis(df_orders):
    print("\n" + "="*60)
    print("2. ANALISIS DE REGRESION")
    print("="*60)

    if df_orders.empty or len(df_orders) < 5:
        print("[WARN] Datos insuficientes para regresion")
        return {}

    # Preparar datos diarios
    daily = df_orders.groupby('date').agg({
        'total': 'sum',
        'id': 'count',
        'items_count': 'sum'
    }).rename(columns={'id': 'orders'})
    daily = daily.reset_index()
    daily['date'] = pd.to_datetime(daily['date'])
    daily['day_num'] = (daily['date'] - daily['date'].min()).dt.days

    # Regresion lineal simple
    X = daily['day_num'].values
    y = daily['total'].values

    n = len(X)
    if n < 2:
        print("[WARN] Necesito al menos 2 puntos para regresion")
        return {}

    sum_x = np.sum(X)
    sum_y = np.sum(y)
    sum_xy = np.sum(X * y)
    sum_x2 = np.sum(X ** 2)

    # y = mx + b
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2 + 1e-10)
    b = (sum_y - m * sum_x) / n

    # Predicciones
    y_pred = m * X + b

    # R-squared
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / (ss_tot + 1e-10))

    print(f"\n[REGRESION LINEAL - Ventas Diarias]")
    print(f"  Ecuacion: y = {m:.2f}x + {b:.2f}")
    print(f"  R-squared: {r_squared:.4f}")
    print(f"  Tendencia: {'CRECIENTE' if m > 0 else 'DECRECIENTE'} (${abs(m):.0f}/dia)")

    # Prediccion proximos 30 dias
    last_day = X.max()
    future_days = np.arange(last_day + 1, last_day + 31)
    future_predictions = m * future_days + b

    print(f"\n[PREDICCION 30 DIAS]")
    print(f"  Ventas proyectadas: ${future_predictions.sum():,.0f}")
    print(f"  Promedio diario: ${future_predictions.mean():,.0f}")

    # Regresion por cantidad de items vs total
    if 'items_count' in df_orders.columns:
        X_items = df_orders['items_count'].values
        y_total = df_orders['total'].values

        m_items = np.polyfit(X_items, y_total, 1)[0]
        print(f"\n[CORRELACION ITEMS vs TOTAL]")
        print(f"  Incremento por item adicional: ${m_items:.0f}")

    results = {
        'linear_regression': {
            'slope': float(m),
            'intercept': float(b),
            'r_squared': float(r_squared),
            'trend': 'growing' if m > 0 else 'declining',
            'daily_change': float(abs(m))
        },
        'predictions_30d': {
            'total': float(future_predictions.sum()),
            'daily_avg': float(future_predictions.mean()),
            'values': [float(v) for v in future_predictions]
        },
        'daily_data': [
            {'date': str(row['date'].date()), 'actual': float(row['total']), 'predicted': float(m * row['day_num'] + b)}
            for _, row in daily.iterrows()
        ]
    }

    return results

# ============================================
# 3. ANALISIS DE ML (Segmentacion)
# ============================================
def ml_analysis(df_orders, customers):
    print("\n" + "="*60)
    print("3. ANALISIS ML - SEGMENTACION")
    print("="*60)

    if df_orders.empty:
        print("[WARN] Sin datos para ML")
        return {}

    # Crear perfil de clientes (RFM)
    today = df_orders['datetime'].max()
    customer_stats = df_orders.groupby('customer_id').agg({
        'datetime': lambda x: (today - x.max()).days,  # Recency
        'id': 'count',  # Frequency
        'total': 'sum'  # Monetary
    }).rename(columns={'datetime': 'recency', 'id': 'frequency', 'total': 'monetary'})

    # Normalizar
    for col in ['recency', 'frequency', 'monetary']:
        min_val = customer_stats[col].min()
        max_val = customer_stats[col].max()
        if max_val > min_val:
            customer_stats[f'{col}_norm'] = (customer_stats[col] - min_val) / (max_val - min_val)
        else:
            customer_stats[f'{col}_norm'] = 0.5

    # Invertir recency (menor es mejor)
    customer_stats['recency_norm'] = 1 - customer_stats['recency_norm']

    # Score RFM
    customer_stats['rfm_score'] = (
        customer_stats['recency_norm'] * 0.3 +
        customer_stats['frequency_norm'] * 0.3 +
        customer_stats['monetary_norm'] * 0.4
    )

    # Segmentos
    def segment(score):
        if score >= 0.7:
            return 'Champions'
        elif score >= 0.5:
            return 'Loyal'
        elif score >= 0.3:
            return 'Potential'
        elif score >= 0.15:
            return 'At Risk'
        else:
            return 'Lost'

    customer_stats['segment'] = customer_stats['rfm_score'].apply(segment)

    segment_counts = customer_stats['segment'].value_counts()
    segment_revenue = customer_stats.groupby('segment')['monetary'].sum()

    print(f"\n[SEGMENTACION RFM]")
    segments_data = []
    for seg in ['Champions', 'Loyal', 'Potential', 'At Risk', 'Lost']:
        count = segment_counts.get(seg, 0)
        revenue = segment_revenue.get(seg, 0)
        pct = (count / len(customer_stats)) * 100 if len(customer_stats) > 0 else 0
        print(f"  {seg}: {count} clientes ({pct:.1f}%) - ${revenue:,.0f}")
        segments_data.append({
            'segment': seg,
            'count': int(count),
            'percentage': float(pct),
            'revenue': float(revenue)
        })

    # Analisis de cohortes (simplificado)
    df_orders['cohort_month'] = df_orders['datetime'].dt.to_period('M')
    first_purchase = df_orders.groupby('customer_id')['cohort_month'].min().reset_index()
    first_purchase.columns = ['customer_id', 'cohort']

    df_orders = df_orders.merge(first_purchase, on='customer_id', how='left')

    cohort_data = df_orders.groupby(['cohort', 'cohort_month']).agg({
        'customer_id': 'nunique'
    }).reset_index()

    print(f"\n[METRICAS DE CLIENTES]")
    print(f"  Clientes analizados: {len(customer_stats)}")
    print(f"  Ticket promedio: ${customer_stats['monetary'].mean():,.0f}")
    print(f"  Frecuencia promedio: {customer_stats['frequency'].mean():.1f} ordenes")
    print(f"  Recencia promedio: {customer_stats['recency'].mean():.0f} dias")

    # Calcular LTV aproximado
    avg_order_value = customer_stats['monetary'].mean() / customer_stats['frequency'].mean()
    avg_frequency = customer_stats['frequency'].mean()
    estimated_ltv = avg_order_value * avg_frequency * 2  # Factor de retencion

    print(f"\n[VALOR DE VIDA (LTV)]")
    print(f"  LTV Estimado: ${estimated_ltv:,.0f}")

    results = {
        'segments': segments_data,
        'metrics': {
            'total_customers': int(len(customer_stats)),
            'avg_ticket': float(customer_stats['monetary'].mean()),
            'avg_frequency': float(customer_stats['frequency'].mean()),
            'avg_recency': float(customer_stats['recency'].mean()),
            'estimated_ltv': float(estimated_ltv)
        },
        'customer_details': [
            {
                'customer_id': int(idx),
                'recency': int(row['recency']),
                'frequency': int(row['frequency']),
                'monetary': float(row['monetary']),
                'segment': row['segment'],
                'score': float(row['rfm_score'])
            }
            for idx, row in customer_stats.iterrows()
        ]
    }

    return results

# ============================================
# 4. FORECASTING
# ============================================
def forecasting_analysis(df_orders):
    print("\n" + "="*60)
    print("4. FORECASTING - PREDICCION DE VENTAS")
    print("="*60)

    if df_orders.empty or len(df_orders) < 7:
        print("[WARN] Datos insuficientes para forecasting")
        return {}

    # Preparar serie temporal diaria
    daily = df_orders.groupby('date')['total'].sum().reset_index()
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.set_index('date').asfreq('D', fill_value=0)

    # Media movil simple (SMA)
    daily['sma_7'] = daily['total'].rolling(window=7, min_periods=1).mean()
    daily['sma_14'] = daily['total'].rolling(window=14, min_periods=1).mean()

    # Media movil exponencial (EMA)
    daily['ema_7'] = daily['total'].ewm(span=7, adjust=False).mean()

    print(f"\n[ESTADISTICAS BASE]")
    print(f"  Dias con datos: {len(daily)}")
    print(f"  Ventas diarias promedio: ${daily['total'].mean():,.0f}")
    print(f"  Desviacion estandar: ${daily['total'].std():,.0f}")
    print(f"  Dia maximo: ${daily['total'].max():,.0f}")

    # Descomposicion de tendencia
    if len(daily) >= 14:
        # Tendencia (media movil larga)
        trend = daily['total'].rolling(window=min(14, len(daily)), center=True, min_periods=1).mean()

        # Estacionalidad (patron semanal)
        daily['day_of_week'] = daily.index.dayofweek
        seasonal_pattern = daily.groupby('day_of_week')['total'].mean()

        print(f"\n[PATRON SEMANAL]")
        days = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
        for dow, avg in seasonal_pattern.items():
            print(f"  {days[dow]}: ${avg:,.0f}")

    # Forecasting con promedio movil ponderado
    last_values = daily['total'].tail(7).values
    weights = np.array([0.05, 0.05, 0.10, 0.10, 0.15, 0.20, 0.35])

    if len(last_values) >= 7:
        weighted_forecast = np.sum(last_values * weights)
    else:
        weighted_forecast = daily['total'].mean()

    # Generar predicciones para 30 dias
    forecasts = []
    last_date = daily.index.max()

    for i in range(1, 31):
        future_date = last_date + timedelta(days=i)
        dow = future_date.dayofweek

        # Base forecast
        base = weighted_forecast

        # Ajuste por dia de semana
        if len(daily) >= 14:
            dow_factor = seasonal_pattern.get(dow, daily['total'].mean()) / daily['total'].mean()
            adjusted = base * dow_factor
        else:
            adjusted = base

        # Agregar ruido aleatorio (simulacion)
        noise = np.random.normal(1, 0.15)
        final = max(0, adjusted * noise)

        forecasts.append({
            'date': str(future_date.date()),
            'forecast': float(final),
            'lower_bound': float(final * 0.7),
            'upper_bound': float(final * 1.3)
        })

    total_forecast = sum(f['forecast'] for f in forecasts)

    print(f"\n[FORECAST 30 DIAS]")
    print(f"  Total proyectado: ${total_forecast:,.0f}")
    print(f"  Promedio diario: ${total_forecast/30:,.0f}")
    print(f"  Rango: ${sum(f['lower_bound'] for f in forecasts):,.0f} - ${sum(f['upper_bound'] for f in forecasts):,.0f}")

    # Proyeccion mensual
    monthly_forecast = total_forecast
    quarterly_forecast = monthly_forecast * 3

    print(f"\n[PROYECCIONES]")
    print(f"  Proximo mes: ${monthly_forecast:,.0f}")
    print(f"  Proximo trimestre: ${quarterly_forecast:,.0f}")

    # Detectar tendencia
    if len(daily) >= 14:
        first_half = daily['total'].head(len(daily)//2).mean()
        second_half = daily['total'].tail(len(daily)//2).mean()
        trend_pct = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0

        print(f"\n[TENDENCIA]")
        print(f"  Cambio periodo: {trend_pct:+.1f}%")
        print(f"  Direccion: {'CRECIMIENTO' if trend_pct > 0 else 'DECRECIMIENTO'}")
    else:
        trend_pct = 0

    results = {
        'historical': [
            {'date': str(idx.date()), 'actual': float(row['total']), 'sma_7': float(row['sma_7'])}
            for idx, row in daily.iterrows()
        ],
        'forecasts': forecasts,
        'summary': {
            'daily_avg': float(daily['total'].mean()),
            'daily_std': float(daily['total'].std()),
            'forecast_30d_total': float(total_forecast),
            'forecast_30d_avg': float(total_forecast / 30),
            'monthly_projection': float(monthly_forecast),
            'quarterly_projection': float(quarterly_forecast),
            'trend_percentage': float(trend_pct)
        }
    }

    if len(daily) >= 14:
        results['weekly_pattern'] = [
            {'day': ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'][dow], 'avg_sales': float(avg)}
            for dow, avg in seasonal_pattern.items()
        ]

    return results

# ============================================
# MAIN
# ============================================
def main():
    print("="*60)
    print("NG ARTIFICIALES - ANALISIS COMPLETO DE DATOS")
    print("="*60)

    # Cargar datos
    print("\n[CARGANDO DATOS...]")
    orders, products, customers = load_data()
    print(f"  Ordenes: {len(orders)}")
    print(f"  Productos: {len(products)}")
    print(f"  Clientes: {len(customers)}")

    # Ejecutar analisis
    descriptive_results, df_orders = descriptive_analysis(orders, products, customers)

    if df_orders is not None and not df_orders.empty:
        regression_results = regression_analysis(df_orders)
        ml_results = ml_analysis(df_orders, customers)
        forecast_results = forecasting_analysis(df_orders)
    else:
        regression_results = {}
        ml_results = {}
        forecast_results = {}

    # Consolidar resultados
    all_results = {
        'generated_at': datetime.now().isoformat(),
        'data_summary': {
            'orders_count': len(orders),
            'products_count': len(products),
            'customers_count': len(customers)
        },
        'descriptive': descriptive_results,
        'regression': regression_results,
        'segmentation': ml_results,
        'forecasting': forecast_results,
        'products': [
            {
                'id': p.get('id'),
                'name': p.get('name', {}).get('es', str(p.get('name', ''))) if isinstance(p.get('name'), dict) else p.get('name', ''),
                'price': float(p.get('price', 0) or 0) if p.get('price') else 0,
                'stock': int(p.get('stock', 0) or 0) if p.get('stock') else 0,
                'variants': len(p.get('variants', []))
            }
            for p in products[:50]  # Limitar a 50 productos
        ]
    }

    # Guardar resultados
    with open('data/analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("[OK] ANALISIS COMPLETADO")
    print("="*60)
    print(f"Resultados guardados en: data/analysis_results.json")

    return all_results

if __name__ == "__main__":
    main()
