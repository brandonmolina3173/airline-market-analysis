import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
lax_sea = pd.read_csv("LAX_SEA.csv")
lga_ord = pd.read_csv("LGA_ORD.csv")

# Better market labels for graphs
lax_sea["Market"] = "LAX-SEA: Los Angeles to Seattle"
lga_ord["Market"] = "LGA-ORD: New York LaGuardia to Chicago O'Hare"

# Combine datasets
df = pd.concat([lax_sea, lga_ord])

# Create time variable
df["Time"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)

# -----------------------------
# Question 2: Passengers Over Time
# -----------------------------
passenger_time = df.groupby(["Time", "Market"])["Passengers"].sum().reset_index()

plt.figure(figsize=(12,6))

for market in passenger_time["Market"].unique():
    temp = passenger_time[passenger_time["Market"] == market]
    plt.plot(temp["Time"], temp["Passengers"], marker="o", label=market)

plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Passengers")
plt.title("Passengers Over Time by Market")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Question 3: Average Fare Over Time
# -----------------------------
fare_time = df.groupby(["Time", "Market"])["MktFare"].mean().reset_index()

plt.figure(figsize=(12,6))

for market in fare_time["Market"].unique():
    temp = fare_time[fare_time["Market"] == market]
    plt.plot(temp["Time"], temp["MktFare"], marker="o", label=market)

plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Average Fare")
plt.title("Average Fare Over Time by Market")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Question 4: Market Share
# -----------------------------
carrier_passengers = df.groupby(
    ["Time", "Market", "TkCarrier"]
)["Passengers"].sum().reset_index()

carrier_passengers["TotalPassengers"] = carrier_passengers.groupby(
    ["Time", "Market"]
)["Passengers"].transform("sum")

carrier_passengers["MarketShare"] = (
    carrier_passengers["Passengers"] /
    carrier_passengers["TotalPassengers"]
)

print(carrier_passengers)

# Plot market share graphs
for market in carrier_passengers["Market"].unique():

    temp_market = carrier_passengers[
        carrier_passengers["Market"] == market
    ]

    plt.figure(figsize=(12,6))

    for carrier in temp_market["TkCarrier"].unique():

        temp = temp_market[
            temp_market["TkCarrier"] == carrier
        ]

        plt.plot(
            temp["Time"],
            temp["MarketShare"],
            marker="o",
            label=carrier
        )

    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Market Share")
    plt.title(f"Airline Market Share Over Time: {market}")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# Question 5: HHI Competition Measure
# -----------------------------
hhi = carrier_passengers.groupby(
    ["Time", "Market"]
).apply(
    lambda x: ((x["MarketShare"] * 100) ** 2).sum()
).reset_index(name="HHI")

print("\nHHI by Market and Time:")
print(hhi)

avg_hhi = hhi.groupby("Market")["HHI"].mean().reset_index()

print("\nAverage HHI by Market:")
print(avg_hhi)
print(avg_hhi)