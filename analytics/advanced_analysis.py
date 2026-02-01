"""
NG Artificiales - Analisis Avanzado
- Series semanales con identificacion de ciclos
- Forecasting semanal
- Analisis Pareto 80/20 de productos
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

def load_orders():
    """Cargar ordenes desde JSON"""
    with open('data/orders.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# ============================================
# 1. SERIES DE TIEMPO SEMANALES
# ============================================
def weekly_time_series(orders):
    print("\n" + "="*70)
    print("1. ANALISIS DE SERIES DE TIEMPO SEMANALES")
    print("="*70)

    # Convertir a datos diarios primero
    daily_sales = defaultdict(float)
    daily_orders = defaultdict(int)

    for o in orders:
        created = o.get('created_at', '')
        if not created:
            continue

        try:
            if 'T' in created:
                dt = datetime.fromisoformat(created.replace('+0000', '+00:00').replace('Z', '+00:00'))
            else:
                dt = datetime.strptime(created, '%Y-%m-%d')

            date_key = dt.date()
            total = float(o.get('total', 0) or 0)
            daily_sales[date_key] += total
            daily_orders[date_key] += 1
        except:
            continue

    if not daily_sales:
        print("[WARN] No hay datos de ventas")
        return {}

    # Crear DataFrame diario
    df_daily = pd.DataFrame([
        {'date': k, 'sales': v, 'orders': daily_orders[k]}
        for k, v in daily_sales.items()
    ])
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df_daily = df_daily.sort_values('date')

    # Rellenar dias sin ventas
    date_range = pd.date_range(df_daily['date'].min(), df_daily['date'].max())
    df_full = pd.DataFrame({'date': date_range})
    df_full = df_full.merge(df_daily, on='date', how='left').fillna(0)

    # Agregar semana ISO
    df_full['week'] = df_full['date'].dt.isocalendar().week
    df_full['year'] = df_full['date'].dt.year
    df_full['year_week'] = df_full['date'].dt.strftime('%Y-W%W')

    # Agrupar por semana
    weekly = df_full.groupby('year_week').agg({
        'sales': 'sum',
        'orders': 'sum',
        'date': 'min'
    }).reset_index()
    weekly = weekly.sort_values('date')
    weekly['week_num'] = range(1, len(weekly) + 1)

    print(f"\n[RESUMEN SERIE SEMANAL]")
    print(f"  Semanas totales: {len(weekly)}")
    print(f"  Rango: {weekly['date'].min().strftime('%Y-%m-%d')} a {weekly['date'].max().strftime('%Y-%m-%d')}")
    print(f"  Ventas promedio/semana: ${weekly['sales'].mean():,.0f}")
    print(f"  Desviacion estandar: ${weekly['sales'].std():,.0f}")
    print(f"  Coef. Variacion: {(weekly['sales'].std() / weekly['sales'].mean() * 100):.1f}%")

    # Estadisticas descriptivas
    print(f"\n[ESTADISTICAS DESCRIPTIVAS]")
    print(f"  Minimo: ${weekly['sales'].min():,.0f}")
    print(f"  Q1 (25%): ${weekly['sales'].quantile(0.25):,.0f}")
    print(f"  Mediana: ${weekly['sales'].median():,.0f}")
    print(f"  Q3 (75%): ${weekly['sales'].quantile(0.75):,.0f}")
    print(f"  Maximo: ${weekly['sales'].max():,.0f}")

    # Semanas con ventas vs sin ventas
    weeks_with_sales = (weekly['sales'] > 0).sum()
    print(f"\n[ACTIVIDAD]")
    print(f"  Semanas con ventas: {weeks_with_sales} ({weeks_with_sales/len(weekly)*100:.1f}%)")
    print(f"  Semanas sin ventas: {len(weekly) - weeks_with_sales}")

    # Top 5 semanas
    top_weeks = weekly.nlargest(5, 'sales')
    print(f"\n[TOP 5 SEMANAS]")
    for _, row in top_weeks.iterrows():
        print(f"  {row['year_week']}: ${row['sales']:,.0f} ({int(row['orders'])} ordenes)")

    return {
        'weekly_data': weekly.to_dict('records'),
        'stats': {
            'total_weeks': len(weekly),
            'avg_weekly_sales': float(weekly['sales'].mean()),
            'std_weekly_sales': float(weekly['sales'].std()),
            'cv': float(weekly['sales'].std() / weekly['sales'].mean() * 100),
            'min': float(weekly['sales'].min()),
            'max': float(weekly['sales'].max()),
            'median': float(weekly['sales'].median()),
            'weeks_with_sales': int(weeks_with_sales)
        }
    }, weekly

# ============================================
# 2. IDENTIFICACION DE CICLOS
# ============================================
def identify_cycles(weekly_df):
    print("\n" + "="*70)
    print("2. IDENTIFICACION DE CICLOS Y PATRONES")
    print("="*70)

    if len(weekly_df) < 4:
        print("[WARN] Serie muy corta para analisis de ciclos")
        return {}

    sales = weekly_df['sales'].values

    # Analisis de autocorrelacion manual
    def autocorrelation(series, lag):
        n = len(series)
        if lag >= n:
            return 0
        mean = np.mean(series)
        var = np.var(series)
        if var == 0:
            return 0
        cov = np.mean((series[:-lag] - mean) * (series[lag:] - mean))
        return cov / var

    # Calcular autocorrelacion para diferentes lags
    max_lag = min(20, len(sales) // 2)
    autocorr = []
    for lag in range(1, max_lag + 1):
        ac = autocorrelation(sales, lag)
        autocorr.append({'lag': lag, 'correlation': ac})

    print(f"\n[AUTOCORRELACION]")
    print(f"  Lag (semanas) | Correlacion")
    print(f"  " + "-"*30)
    for item in autocorr[:10]:
        bar = "*" * int(abs(item['correlation']) * 20)
        sign = "+" if item['correlation'] > 0 else "-"
        print(f"  {item['lag']:2d} semanas    | {item['correlation']:+.3f} {sign}{bar}")

    # Encontrar ciclos significativos (correlacion > 0.3)
    significant_cycles = [a for a in autocorr if abs(a['correlation']) > 0.3]

    if significant_cycles:
        print(f"\n[CICLOS DETECTADOS]")
        for cycle in significant_cycles[:5]:
            print(f"  Ciclo de {cycle['lag']} semanas (r={cycle['correlation']:.3f})")
    else:
        print(f"\n[CICLOS DETECTADOS]")
        print(f"  No se detectaron ciclos significativos (r > 0.3)")

    # Analisis de tendencia
    x = np.arange(len(sales))
    if len(sales) > 1:
        slope, intercept = np.polyfit(x, sales, 1)
        trend = "CRECIENTE" if slope > 0 else "DECRECIENTE"
        print(f"\n[TENDENCIA]")
        print(f"  Direccion: {trend}")
        print(f"  Cambio semanal: ${slope:,.0f}")
    else:
        slope = 0

    # Estacionalidad mensual
    weekly_df['month'] = pd.to_datetime(weekly_df['date']).dt.month
    monthly_pattern = weekly_df.groupby('month')['sales'].mean()

    print(f"\n[PATRON MENSUAL]")
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    for month, avg in monthly_pattern.items():
        print(f"  {months[month-1]}: ${avg:,.0f}")

    # Detectar picos (ventas > media + 1.5*std)
    threshold_high = weekly_df['sales'].mean() + 1.5 * weekly_df['sales'].std()
    threshold_low = weekly_df['sales'].mean() - 1.5 * weekly_df['sales'].std()
    peaks = weekly_df[weekly_df['sales'] > threshold_high]
    valleys = weekly_df[weekly_df['sales'] < max(0, threshold_low)]

    print(f"\n[ANOMALIAS]")
    print(f"  Picos detectados (> ${threshold_high:,.0f}): {len(peaks)}")
    print(f"  Valles detectados: {len(valleys)}")

    return {
        'autocorrelation': autocorr,
        'significant_cycles': significant_cycles,
        'trend_slope': float(slope),
        'trend_direction': "growing" if slope > 0 else "declining",
        'monthly_pattern': {int(k): float(v) for k, v in monthly_pattern.items()},
        'peaks_count': len(peaks),
        'valleys_count': len(valleys)
    }

# ============================================
# 3. FORECASTING SEMANAL
# ============================================
def weekly_forecasting(weekly_df, periods=12):
    print("\n" + "="*70)
    print("3. FORECASTING SEMANAL (12 semanas)")
    print("="*70)

    sales = weekly_df['sales'].values

    if len(sales) < 4:
        print("[WARN] Serie muy corta para forecasting")
        return {}

    # Metodo 1: Media movil simple (SMA)
    window = min(4, len(sales))
    sma = np.convolve(sales, np.ones(window)/window, mode='valid')
    last_sma = sma[-1] if len(sma) > 0 else np.mean(sales)

    # Metodo 2: Media movil exponencial (EMA)
    alpha = 0.3
    ema = [sales[0]]
    for i in range(1, len(sales)):
        ema.append(alpha * sales[i] + (1 - alpha) * ema[-1])
    last_ema = ema[-1]

    # Metodo 3: Regresion lineal
    x = np.arange(len(sales))
    slope, intercept = np.polyfit(x, sales, 1)

    # Metodo 4: Holt-Winters simplificado (tendencia + nivel)
    level = sales[-1]
    trend = slope

    # Generar predicciones
    forecasts = []
    last_date = pd.to_datetime(weekly_df['date'].max())

    for i in range(1, periods + 1):
        future_date = last_date + timedelta(weeks=i)

        # Prediccion por regresion
        pred_regression = slope * (len(sales) + i - 1) + intercept

        # Prediccion por EMA
        pred_ema = last_ema

        # Prediccion Holt-Winters
        pred_hw = level + trend * i

        # Prediccion combinada (promedio ponderado)
        pred_combined = 0.4 * pred_regression + 0.3 * pred_ema + 0.3 * pred_hw
        pred_combined = max(0, pred_combined)  # No negativos

        # Bandas de confianza
        std = weekly_df['sales'].std()
        lower = max(0, pred_combined - 1.5 * std)
        upper = pred_combined + 1.5 * std

        forecasts.append({
            'week': i,
            'date': future_date.strftime('%Y-%m-%d'),
            'forecast': float(pred_combined),
            'lower_bound': float(lower),
            'upper_bound': float(upper),
            'regression': float(max(0, pred_regression)),
            'ema': float(pred_ema),
            'holt_winters': float(max(0, pred_hw))
        })

    print(f"\n[PREDICCIONES PROXIMAS 12 SEMANAS]")
    print(f"  {'Semana':<10} {'Fecha':<12} {'Forecast':<15} {'Rango'}")
    print(f"  " + "-"*55)
    for f in forecasts:
        print(f"  {f['week']:<10} {f['date']:<12} ${f['forecast']:>12,.0f} [${f['lower_bound']:,.0f} - ${f['upper_bound']:,.0f}]")

    total_forecast = sum(f['forecast'] for f in forecasts)
    print(f"\n[RESUMEN FORECAST]")
    print(f"  Total 12 semanas: ${total_forecast:,.0f}")
    print(f"  Promedio semanal: ${total_forecast/12:,.0f}")

    # Agregar historico con SMA
    historical = []
    sma_full = np.concatenate([np.full(window-1, np.nan), sma])
    for i, row in weekly_df.iterrows():
        idx = weekly_df.index.get_loc(i)
        historical.append({
            'date': row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']),
            'year_week': row['year_week'],
            'sales': float(row['sales']),
            'orders': int(row['orders']),
            'sma_4': float(sma_full[idx]) if idx < len(sma_full) and not np.isnan(sma_full[idx]) else None
        })

    return {
        'historical': historical,
        'forecasts': forecasts,
        'summary': {
            'total_12w': float(total_forecast),
            'avg_weekly': float(total_forecast / 12),
            'method': 'Combined (Regression + EMA + Holt-Winters)'
        }
    }

# ============================================
# 4. ANALISIS PARETO 80/20 DE PRODUCTOS
# ============================================
def pareto_analysis(orders, cost_pct=0.60):
    print("\n" + "="*70)
    print("4. ANALISIS PARETO 80/20 DE PRODUCTOS")
    print(f"   (Asumiendo costo = {cost_pct*100:.0f}% del precio)")
    print("="*70)

    # Agregar ventas por producto
    product_sales = defaultdict(lambda: {
        'name': '',
        'quantity': 0,
        'revenue': 0,
        'orders_count': 0
    })

    for o in orders:
        for p in o.get('products', []) or []:
            pid = p.get('product_id') or p.get('id')
            if not pid:
                continue

            name = p.get('name', f'Producto {pid}')
            if isinstance(name, dict):
                name = name.get('es', name.get('en', str(name)))

            qty = int(p.get('quantity', 1) or 1)
            price = float(p.get('price', 0) or 0)
            revenue = price * qty

            product_sales[pid]['name'] = name
            product_sales[pid]['quantity'] += qty
            product_sales[pid]['revenue'] += revenue
            product_sales[pid]['orders_count'] += 1

    if not product_sales:
        print("[WARN] No hay datos de productos")
        return {}

    # Convertir a lista y ordenar por revenue
    products = []
    for pid, data in product_sales.items():
        # Calcular margen estimado
        estimated_cost = data['revenue'] * cost_pct
        estimated_margin = data['revenue'] - estimated_cost

        products.append({
            'id': pid,
            'name': data['name'],
            'quantity': data['quantity'],
            'revenue': data['revenue'],
            'orders_count': data['orders_count'],
            'avg_price': data['revenue'] / data['quantity'] if data['quantity'] > 0 else 0,
            'estimated_cost': estimated_cost,
            'estimated_margin': estimated_margin,
            'margin_pct': (1 - cost_pct) * 100
        })

    # Ordenar por revenue descendente
    products.sort(key=lambda x: x['revenue'], reverse=True)

    # Calcular totales
    total_revenue = sum(p['revenue'] for p in products)
    total_quantity = sum(p['quantity'] for p in products)
    total_margin = sum(p['estimated_margin'] for p in products)

    # Calcular porcentajes acumulados
    cumulative_revenue = 0
    cumulative_pct = 0

    for i, p in enumerate(products):
        cumulative_revenue += p['revenue']
        cumulative_pct = (cumulative_revenue / total_revenue) * 100
        p['revenue_pct'] = (p['revenue'] / total_revenue) * 100
        p['cumulative_pct'] = cumulative_pct
        p['rank'] = i + 1

    # Identificar productos 80/20
    products_80 = [p for p in products if p['cumulative_pct'] <= 80]
    products_20 = [p for p in products if p['cumulative_pct'] > 80]

    # Si no hay suficientes para 80%, tomar los que hay
    if not products_80:
        threshold_idx = max(1, int(len(products) * 0.2))
        products_80 = products[:threshold_idx]
        products_20 = products[threshold_idx:]

    pct_products_80 = (len(products_80) / len(products)) * 100

    print(f"\n[RESUMEN GENERAL]")
    print(f"  Total productos: {len(products)}")
    print(f"  Total revenue: ${total_revenue:,.0f}")
    print(f"  Total unidades: {total_quantity}")
    print(f"  Margen estimado: ${total_margin:,.0f} ({(1-cost_pct)*100:.0f}%)")

    print(f"\n[ANALISIS PARETO]")
    print(f"  Productos que generan 80% revenue: {len(products_80)} ({pct_products_80:.1f}% del catalogo)")
    print(f"  Productos restantes (20% revenue): {len(products_20)}")

    print(f"\n[TOP 10 PRODUCTOS (80% del revenue)]")
    print(f"  {'#':<3} {'Producto':<35} {'Qty':<6} {'Revenue':<15} {'%':<6} {'Acum%'}")
    print(f"  " + "-"*80)
    for p in products_80[:10]:
        name = p['name'][:32] + "..." if len(p['name']) > 35 else p['name']
        print(f"  {p['rank']:<3} {name:<35} {p['quantity']:<6} ${p['revenue']:>12,.0f} {p['revenue_pct']:>5.1f}% {p['cumulative_pct']:>5.1f}%")

    print(f"\n[PRODUCTOS QUE COMPLETAN EL 20% RESTANTE]")
    print(f"  Cantidad: {len(products_20)}")
    if products_20:
        revenue_20 = sum(p['revenue'] for p in products_20)
        print(f"  Revenue total: ${revenue_20:,.0f}")
        print(f"  Revenue promedio: ${revenue_20/len(products_20):,.0f}")

    # Analisis de concentracion
    top_1_pct = products[0]['revenue_pct'] if products else 0
    top_3_pct = sum(p['revenue_pct'] for p in products[:3]) if len(products) >= 3 else 0
    top_5_pct = sum(p['revenue_pct'] for p in products[:5]) if len(products) >= 5 else 0

    print(f"\n[CONCENTRACION DE VENTAS]")
    print(f"  Top 1 producto: {top_1_pct:.1f}% del revenue")
    print(f"  Top 3 productos: {top_3_pct:.1f}% del revenue")
    print(f"  Top 5 productos: {top_5_pct:.1f}% del revenue")

    # Indice Herfindahl-Hirschman (concentracion)
    hhi = sum((p['revenue_pct'])**2 for p in products)
    concentration = "ALTA" if hhi > 2500 else "MODERADA" if hhi > 1500 else "BAJA"

    print(f"\n[INDICE DE CONCENTRACION (HHI)]")
    print(f"  HHI: {hhi:.0f}")
    print(f"  Nivel: {concentration}")

    return {
        'products': products,
        'pareto_80': [{'id': p['id'], 'name': p['name'], 'revenue': p['revenue'], 'cumulative_pct': p['cumulative_pct']} for p in products_80],
        'pareto_20': [{'id': p['id'], 'name': p['name'], 'revenue': p['revenue']} for p in products_20],
        'summary': {
            'total_products': len(products),
            'total_revenue': float(total_revenue),
            'total_quantity': int(total_quantity),
            'total_margin': float(total_margin),
            'products_80_count': len(products_80),
            'products_80_pct': float(pct_products_80),
            'top_1_pct': float(top_1_pct),
            'top_3_pct': float(top_3_pct),
            'top_5_pct': float(top_5_pct),
            'hhi': float(hhi),
            'concentration': concentration,
            'cost_assumption': float(cost_pct)
        }
    }

# ============================================
# MAIN
# ============================================
def main():
    print("="*70)
    print("NG ARTIFICIALES - ANALISIS AVANZADO")
    print("="*70)

    # Cargar datos
    print("\n[CARGANDO DATOS...]")
    orders = load_orders()
    print(f"  Ordenes cargadas: {len(orders)}")

    # 1. Serie semanal
    weekly_results, weekly_df = weekly_time_series(orders)

    # 2. Ciclos
    cycle_results = identify_cycles(weekly_df)

    # 3. Forecasting
    forecast_results = weekly_forecasting(weekly_df)

    # 4. Pareto
    pareto_results = pareto_analysis(orders)

    # Consolidar resultados
    all_results = {
        'generated_at': datetime.now().isoformat(),
        'weekly_analysis': weekly_results,
        'cycles': cycle_results,
        'forecasting': forecast_results,
        'pareto': pareto_results
    }

    # Guardar
    with open('data/advanced_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)

    print("\n" + "="*70)
    print("[OK] ANALISIS AVANZADO COMPLETADO")
    print("="*70)
    print(f"Resultados guardados en: data/advanced_analysis.json")

    return all_results

if __name__ == "__main__":
    main()
