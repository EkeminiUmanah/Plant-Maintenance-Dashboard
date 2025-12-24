import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================
# EQUIPMENT MASTER DATA
# ============================================

equipment_types = [
    "Centrifugal Pump", "Gas Compressor", "Heat Exchanger",
    "Pressure Vessel", "Control Valve", "Electric Motor",
    "Turbine", "Separator", "Storage Tank", "Cooling Tower",
    "Diesel Generator", "Gas Turbine", "Boiler", "Reactor"
]

equipment_data = []
equipment_id = 100

for i in range(30):
    eq_type = random.choice(equipment_types)
    criticality = random.choices(
        ["Critical", "High", "Medium", "Low"],
        weights=[0.2, 0.3, 0.3, 0.2]
    )[0]

    equipment_data.append({
        "Equipment_ID": f"EQ-{equipment_id + i}",
        "Equipment_Name": f"{eq_type} {chr(65 + i // 10)}-{100 + i}",
        "Equipment_Type": eq_type,
        "Criticality": criticality,
        "Location": random.choice(["Platform A", "Platform B", "Onshore Facility", "Processing Unit"]),
        "Installed_Date": (datetime.now() - timedelta(days=random.randint(365 * 2, 365 * 10))).strftime("%Y-%m-%d"),
        "Status": random.choices(["Operational", "Under Maintenance", "Standby"], weights=[0.85, 0.10, 0.05])[0]
    })

equipment_df = pd.DataFrame(equipment_data)

# ============================================
# WORK ORDERS / MAINTENANCE RECORDS
# ============================================

maintenance_types = ["Preventive", "Corrective", "Breakdown", "Inspection", "Overhaul"]
work_order_status = ["Completed", "In Progress", "Planned", "Cancelled"]
failure_types = [
    "Mechanical Seal Failure", "Bearing Wear", "Corrosion", "Vibration",
    "Overheating", "Leakage", "Electrical Fault", "Control System Error",
    "Normal Wear", "Calibration Drift", "Lubrication Issue", "No Failure"
]

work_orders = []
wo_id = 1000

# Generate 12 months of maintenance history
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

for equipment in equipment_data:
    eq_id = equipment["Equipment_ID"]
    eq_criticality = equipment["Criticality"]

    # More critical equipment gets more frequent maintenance
    if eq_criticality == "Critical":
        num_maintenance = random.randint(15, 25)
    elif eq_criticality == "High":
        num_maintenance = random.randint(10, 18)
    elif eq_criticality == "Medium":
        num_maintenance = random.randint(6, 12)
    else:
        num_maintenance = random.randint(3, 8)

    for _ in range(num_maintenance):
        maint_type = random.choices(
            maintenance_types,
            weights=[0.5, 0.2, 0.15, 0.1, 0.05]
        )[0]

        # Breakdown maintenance has higher costs and longer downtime
        if maint_type == "Breakdown":
            cost_range = (200000, 800000)
            downtime_range = (8, 48)
            failure = random.choice([f for f in failure_types if f != "No Failure"])
        elif maint_type == "Overhaul":
            cost_range = (500000, 1500000)
            downtime_range = (24, 120)
            failure = "Normal Wear"
        elif maint_type == "Preventive":
            cost_range = (50000, 300000)
            downtime_range = (2, 12)
            failure = "No Failure"
        elif maint_type == "Inspection":
            cost_range = (20000, 100000)
            downtime_range = (1, 4)
            failure = "No Failure"
        else:  # Corrective
            cost_range = (100000, 500000)
            downtime_range = (4, 24)
            failure = random.choice(failure_types)

        wo_date = start_date + timedelta(days=random.randint(0, 365))
        completion_date = wo_date + timedelta(hours=random.uniform(*downtime_range))

        status = random.choices(
            work_order_status,
            weights=[0.85, 0.08, 0.05, 0.02]
        )[0]

        work_orders.append({
            "WO_Number": f"WO-{wo_id}",
            "Equipment_ID": eq_id,
            "Equipment_Name": equipment["Equipment_Name"],
            "Maintenance_Type": maint_type,
            "Priority": random.choices(
                ["Critical", "High", "Medium", "Low"],
                weights=[0.15, 0.25, 0.40, 0.20]
            )[0],
            "Status": status,
            "Created_Date": wo_date.strftime("%Y-%m-%d"),
            "Scheduled_Start": wo_date.strftime("%Y-%m-%d %H:%M"),
            "Actual_Start": wo_date.strftime("%Y-%m-%d %H:%M") if status == "Completed" else "",
            "Completion_Date": completion_date.strftime("%Y-%m-%d %H:%M") if status == "Completed" else "",
            "Downtime_Hours": round(random.uniform(*downtime_range), 1) if status == "Completed" else 0,
            "Cost_NGN": round(random.uniform(*cost_range), 2) if status == "Completed" else 0,
            "Failure_Type": failure if status == "Completed" else "",
            "Technician": random.choice([
                "John Okafor", "Amina Ibrahim", "Chidi Eze", "Fatima Bello",
                "Emeka Okonkwo", "Aisha Mohammed", "Tunde Adeleke", "Zainab Yusuf"
            ]),
            "Description": f"{maint_type} maintenance on {equipment['Equipment_Name']}"
        })

        wo_id += 1

work_orders_df = pd.DataFrame(work_orders)

# ============================================
# CALCULATE KPIs FOR SUMMARY SHEET
# ============================================

completed_wo = work_orders_df[work_orders_df["Status"] == "Completed"]

kpi_summary = {
    "Total_Equipment": len(equipment_df),
    "Total_Work_Orders": len(work_orders_df),
    "Completed_WO": len(completed_wo),
    "In_Progress_WO": len(work_orders_df[work_orders_df["Status"] == "In Progress"]),
    "Planned_WO": len(work_orders_df[work_orders_df["Status"] == "Planned"]),
    "Total_Downtime_Hours": completed_wo["Downtime_Hours"].sum(),
    "Total_Maintenance_Cost_NGN": completed_wo["Cost_NGN"].sum(),
    "Avg_Downtime_Hours": completed_wo["Downtime_Hours"].mean(),
    "Avg_Cost_Per_WO_NGN": completed_wo["Cost_NGN"].mean(),
    "Preventive_Maintenance_Pct": (
                len(completed_wo[completed_wo["Maintenance_Type"] == "Preventive"]) / len(completed_wo) * 100),
    "Breakdown_Maintenance_Pct": (
                len(completed_wo[completed_wo["Maintenance_Type"] == "Breakdown"]) / len(completed_wo) * 100),
}

# Calculate MTBF and MTTR for each equipment
equipment_metrics = []

for eq_id in equipment_df["Equipment_ID"]:
    eq_work_orders = completed_wo[completed_wo["Equipment_ID"] == eq_id]
    breakdowns = eq_work_orders[eq_work_orders["Maintenance_Type"] == "Breakdown"]

    if len(breakdowns) > 1:
        # MTBF = operating time between failures
        mtbf = 365 * 24 / len(breakdowns)  # Simplified calculation
    else:
        mtbf = 365 * 24  # No breakdowns = high MTBF

    if len(eq_work_orders) > 0:
        mttr = eq_work_orders["Downtime_Hours"].mean()
    else:
        mttr = 0

    equipment_metrics.append({
        "Equipment_ID": eq_id,
        "Total_Work_Orders": len(eq_work_orders),
        "Total_Downtime_Hours": eq_work_orders["Downtime_Hours"].sum(),
        "Total_Cost_NGN": eq_work_orders["Cost_NGN"].sum(),
        "MTBF_Hours": round(mtbf, 1),
        "MTTR_Hours": round(mttr, 1),
        "Availability_Pct": round((1 - eq_work_orders["Downtime_Hours"].sum() / (365 * 24)) * 100, 2)
    })

equipment_metrics_df = pd.DataFrame(equipment_metrics)

# ============================================
# EXPORT TO EXCEL
# ============================================

# Create Excel writer
output_file = "CMMS_Maintenance_Data.xlsx"

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    # Write dataframes
    equipment_df.to_excel(writer, sheet_name='Equipment_Master', index=False)
    work_orders_df.to_excel(writer, sheet_name='Work_Orders', index=False)
    equipment_metrics_df.to_excel(writer, sheet_name='Equipment_Metrics', index=False)

    # Write KPI Summary
    kpi_df = pd.DataFrame([kpi_summary])
    kpi_df.to_excel(writer, sheet_name='KPI_Summary', index=False)

    # Format columns
    workbook = writer.book

    # Number formats
    money_fmt = workbook.add_format({'num_format': '₦#,##0.00'})
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    number_fmt = workbook.add_format({'num_format': '#,##0.0'})

    # Apply formatting to Work Orders sheet
    worksheet = writer.sheets['Work_Orders']
    worksheet.set_column('K:K', 15, number_fmt)  # Downtime_Hours
    worksheet.set_column('L:L', 18, money_fmt)  # Cost_NGN

    # Apply formatting to Equipment Metrics sheet
    worksheet = writer.sheets['Equipment_Metrics']
    worksheet.set_column('D:D', 18, money_fmt)  # Total_Cost_NGN
    worksheet.set_column('E:F', 12, number_fmt)  # MTBF, MTTR

    # Apply formatting to KPI Summary sheet
    worksheet = writer.sheets['KPI_Summary']
    worksheet.set_column('G:H', 20, money_fmt)  # Cost columns
    worksheet.set_column('F:F', 18, number_fmt)  # Downtime

print(f"✅ Successfully generated {output_file}")
print(f"\n📊 Summary Statistics:")
print(f"   - Equipment Items: {len(equipment_df)}")
print(f"   - Work Orders: {len(work_orders_df)}")
print(f"   - Completed Work Orders: {len(completed_wo)}")
print(f"   - Total Maintenance Cost: ₦{kpi_summary['Total_Maintenance_Cost_NGN']:,.2f}")
print(f"   - Total Downtime: {kpi_summary['Total_Downtime_Hours']:,.1f} hours")
print(f"   - Preventive Maintenance: {kpi_summary['Preventive_Maintenance_Pct']:.1f}%")
print(f"\n✨ Data ready for Excel and Power BI!")
print(f"\nNext Steps:")
print(f"1. Open {output_file} in Excel")
print(f"2. Create pivot tables and charts from the data")
print(f"3. Import into Power BI for interactive dashboards")
print(f"4. Customize as needed for your portfolio")